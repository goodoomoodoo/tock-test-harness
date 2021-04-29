import os
import toml
from pathlib import Path

# Parse configuration
with open(f"{Path.home()}/tock-test-harness/test.config.toml", 'r') as config_toml:
    TEST_CONFIG = toml.load(config_toml)

# Cannot run script
if 'scripts' not in TEST_CONFIG:
    raise KeyError("'scripts' does not exists in test config, cannot start test") 

SCRIPT_CONFIG = TEST_CONFIG['scripts']

# Run top level install script
if 'install' in SCRIPT_CONFIG:
    SCRIPT_INSTALL_CONFIG = SCRIPT_CONFIG['install']

    if 'prerun' in SCRIPT_INSTALL_CONFIG:
        SCRIPT_INSTALL_CONFIG['prerun'].replace('~', str(Path.home()))
        os.system(SCRIPT_INSTALL_CONFIG['prerun'])
    
    if 'run' in SCRIPT_INSTALL_CONFIG:
        print("Running")
        SCRIPT_INSTALL_CONFIG['run'].replace('~', str(Path.home()))
        os.system(SCRIPT_INSTALL_CONFIG['run'])
    
    if 'postrun' in SCRIPT_INSTALL_CONFIG:
        SCRIPT_INSTALL_CONFIG['postrun'].replace('~', str(Path.home()))
        os.system(SCRIPT_INSTALL_CONFIG['postrun'])
