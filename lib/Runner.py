import logging
import os
import toml
from pathlib import Path

class Runner:
    def __init__(self, **args):
        """Load TOML file in filename as the configuration"""
        self.home_dir = Path.home()
        self.config_file = f'{Path.home()}/tock-test-harness/test.config.toml'
        self.path = 'path/to/board'
        self.log = self.setup_logger()
        self.args = args

        with open(self.config_file, 'r') as config_toml:
            self.config = toml.load(config_toml)
            self.load_config

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
        pass

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

    def app_install(self):
        """Lookup the APPs listed in configuration in libtock-c and install
        
        Note: libtock-c should be checked out in tock-test-harness
        """
        if 'app' in self.test_config:
            for app in self.test_config['app']:
                # TODO: finish the workflow
                continue

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
