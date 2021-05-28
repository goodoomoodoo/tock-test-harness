import git
import logging
import os
import tockloader
import toml
from pathlib import Path

TOCK_BOARD_DIR = f'{Path.home()}/actions-runner/_work/tock/tock/boards/'
LIBTOCK_C_DIR = f'{Path.home()}/libtock-c/'
CI_TEST_DIR = f'{LIBTOCK_C_DIR}/examples/ci-tests/'
CONFIG_FILE = f'{Path.home()}/tock-test-harness/config.toml'
BOARD_CONFIG_FILE = 'test.config.toml'
TEST_MOD_MAP = {
    'nrf52dk': 'Nrf52840Test'
}

class Runner:
    """Runner class, container of build, flash, and test workflow
    
    board      - Board model, used to run tockloader
    comm_proc  - Communication protocol, used to run tockloader
    harness_id - Provides identity to the runner and will only execute commands
                 with corresponding harness ID in the test.config.toml
    """
    def __init__(self, **args):
        """Load TOML file in filename as the configuration"""
        self.home_dir = Path.home()
        self.path = 'path/to/board'
        self.board = 'board_model'
        self.comm_proc = ''
        self.harness_id = '' # Considered free lancer if left blank
        self.log = self.setup_logger()
        self.args = args
        self.board_config = None # Initialized in load_config()

        with open(CONFIG_FILE, 'r') as config_toml:
            self.config = toml.load(config_toml)
            self.load_config()

        # If install not specified, run default install workflow
        if 'scripts' in self.board_config:
            if 'install' in self.board_config['scripts']:
                self.install_script = self.board_config['scripts']['install']
            
            # If test not specified, script should end
            if 'test' in self.board_config['scripts']:
                self.test_script = self.board_config['scripts']['test']
        
        if 'test' in self.board_config:
            self.test_config = self.board_config['test']


    def setup_logger(self):
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger = logging.getLogger('Runner')
        logger.setLevel('INFO')
        
        return logger
    
    def load_config(self):
        """Read configuration and assign path to 'path' member variable"""
        self.path = TOCK_BOARD_DIR + self.config['env']['path'] + '/'
        self.board = self.config['env']['board']
        self.harness_id = self.config['env']['harness_id']
        self.comm_proc = self.config['env']['communication_protocol']
        
        with open(self.path + BOARD_CONFIG_FILE, 'r') as board_config_toml:
            self.board_config = toml.load(board_config_toml)

    def tock_build(self):
        """Build the Tock OS with the given configuration"""
        self.log.info('Initiating compilation.')
        os.chdir(self.path)
        os.system('make')

    def tock_preinstall(self):
        """Check prerun sequence, run if exists."""
        if self.install_script and 'prerun' in self.install_script:
            # Execute prerun specification
            self.log.info('Initiating prerun specification.')
            os.system(self.install_script['prerun'])
        else:
            self.log.info('No pre install script.')

    def tock_postinstall(self):
        """Check prerun sequence, run if exists."""
        if self.install_script and 'postrun' in self.install_script:
            # Execute postrun specification
            self.log.info('Initiating postrun specification.')
            os.system(self.install_script['postrun'])
        else:
            self.log.info('No post install script.')

    def tock_install(self):
        """Flash Tock OS bin to board with the given configuration
        
        Note: if configuration file does not specify 'install', this script will
              run the default installation, which is just 'make install'.
        """
        os.chdir(self.path)
        self.tock_preinstall()

        self.log.info('Initiating installation.')
        
        if self.install_script and 'run' in self.install_script:
            os.system(self.install_script['run'])
        else:
            os.system('make install')

        self.tock_postinstall()

        self.log.info('Installtion completed.')

    def app_build(self, apps):
        """Lookup the APPs listed in configuration in libtock-c and compile APPs
        """
        self.log.info('Compiling libtock-c APPs... \n')
        for app in apps:
            if os.path.exists(CI_TEST_DIR + app):
                os.chdir(CI_TEST_DIR + app)
                os.system('make')


    def app_install(self, apps):
        """Lookup the APPs listed in configuration in libtock-c and install to 
        the target board.

        This step depends on app_build. If build fail, then app_install should
        not be called
        """
        self.log.info('Installing libtock-c APPs... \n')
        for app in apps:
            if self.comm_proc != '':
                CMD = (f"tockloader install --board {self.board} " + 
                       f"--{self.comm_proc} " +
                       f'{CI_TEST_DIR}/{app}/build/{app}.tab')
                print('\n', CMD, '\n')
                os.system(CMD)
            else:
                os.system((f'tockloader install --board {self.board} ' + 
                           f'{CI_TEST_DIR}/{app}/build/{app}.tab'))

    def app_test(self, apps):
        """Lookup the APPs listed in configuration in libtock-c and install to 
        the target board.

        This step depends on app_build. If build fail, then app_install should
        not be called
        """
        self.log.info('Testing APPs... \n')
        for app in apps:
            os.system((f'python3 {CI_TEST_DIR}/{app}/test.py ' +
                       f'{TEST_MOD_MAP[self.board]}'))

    def tock_pretest(self):
        """Check prerun sequence, run if exists."""
        if self.test_script and 'prerun' in self.test_script:
            # Execute prerun specification
            self.log.info('Initiating prerun specification.')
            os.system(self.test_script['prerun'])
        else:
            self.log.info('No pre test script.')

    def tock_posttest(self):
        """Check prerun sequence, run if exists."""
        if self.test_script and 'postrun' in self.test_script:
            # Execute postrun specification
            self.log.info('Initiating postrun specification.')
            os.system(self.install_script['postrun'])
        else:
            self.log.info('No post test script.')

    def tock_test(self):
        """Test workflow"""
        self.log.info('Initiating test workflow. \n')

        self.tock_pretest()

        # Unpack test configuration and APPs installation
        if self.test_config != None:
            self.log.info('Updating libtock-c repository... \n')
            git.Repo(LIBTOCK_C_DIR).remotes.origin.pull() # git pull

            for harness_token in self.test_config:
                # Harness specifier for all harnesses
                if harness_token == 'all' or harness_token == self.harness_id:
                    apps = self.test_config[harness_token]['app']
                    self.app_build(apps)
                    self.app_install(apps)
                    self.app_test(apps)

        self.tock_posttest()

        self.log.info('Test workflow complete.')


    def run(self):
        """Top level run"""
        if self.args['build']:
            self.tock_build()

        if self.args['install']:
            self.tock_install()

        if self.args['test']:
            self.tock_test()
