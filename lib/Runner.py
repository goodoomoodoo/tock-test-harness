import logging
import os
import tockloader
import toml
from pathlib import Path

TOCK_DIR = f'{Path.home()}/actions-runner/_work/tock/tock/'
CI_TEST_DIR = f'{Path.home()}/tock-test-harness/libtock-c/examples/ci-tests/'

def update_repo(path):
    """Update Git repository of the given path"""
    os.chdir(path)
    os.system('git pull')

class Runner:
    def __init__(self, **args):
        """Load TOML file in filename as the configuration"""
        self.home_dir = Path.home()
        self.config_file = f'{Path.home()}/tock-test-harness/test.config.toml'
        self.path = 'path/to/board'
        self.series = 'series'
        self.comm_proc = ''
        self.log = self.setup_logger()
        self.args = args

        with open(self.config_file, 'r') as config_toml:
            self.config = toml.load(config_toml)
            self.load_config()

        # If install not specified, run default install workflow
        if 'install' in self.config:
            self.install_config = self.config['install']
        
        # If test not specified, script should end
        if 'test' in self.config:
            self.test_config = self.config['test']

    def setup_logger(self):
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger = logging.getLogger('Runner')
        logger.setLevel('INFO')
        
        return logger
    
    def load_config(self):
        """Read configuration and assign path to 'path' member variable"""
        # TODO: parse configuration. This function should parse a static config
        #       filename and read the configuration. If the file dne, raise 
        #       error.
        self.path = TOCK_DIR + 'boards/nordic/nrf52840dk'
        self.series = 'nrf52dk'

    def tock_build(self):
        """Build the Tock OS with the given configuration"""
        self.log.info('Initiating compilation.')
        os.chdir(self.path)
        os.system('make')

    def tock_preinstall(self):
        """Check prerun sequence, run if exists."""
        if self.install_config and 'prerun' in self.install_config:
            # Execute prerun specification
            self.log.info('Initiating prerun specification.')
            os.chdir(self.path)
            os.system(self.install_config['prerun'])

    def tock_postinstall(self):
        """Check prerun sequence, run if exists."""
        if self.install_config and 'postrun' in self.install_config:
            # Execute postrun specification
            self.log.info('Initiating postrun specification.')
            os.chdir(self.path)
            os.system(self.install_config['postrun'])

    def tock_install(self):
        """Flash Tock OS bin to board with the given configuration
        
        Note: if configuration file does not specify 'install', this script will
              run the default installation, which is just 'make install'.
        """
        self.pre_run()

        self.log.info('Initiating installation.')
        
        if self.install_config and 'run' in self.install_config:
            os.chdir(self.path)
            os.system(self.install_config['run'])
        else:
            os.chdir(self.path)
            os.system('make install')

        self.post_run()

    def app_build(self, apps):
        """Lookup the APPs listed in configuration in libtock-c and compile APPs
        """
        self.log.info('Updating libtock-c repository... \n')
        update_repo(CI_TEST_DIR)

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
        for app in apps:
            if self.comm_proc != '':
                os.system((f'tockloader install --board {self.series} ' + 
                           f'--{self.comm_proc} {app}'))
            else:
                os.system(f'tockloader install --board {self.series} {app}')

    def tock_test(self):
        """Test workflow"""
        pass

    def run(self):
        """Top level run"""
        if self.args['build']:
            self.tock_build()

        if self.args['install']:
            self.tock_install()

        if self.args['test']:
            self.tock_test()
