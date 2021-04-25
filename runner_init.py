import os
from pathlib import Path
from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

# Parse configuration
with open(f"{Path.home()}/tock-test-harness/test.config.yml", 'r') as config_yml:
    TEST_CONFIG = load(config_yml, Loader=Loader)

# Run top level script
if 'prerun' in TEST_CONFIG['scripts']:
    os.system(TEST_CONFIG['scripts']['prerun'])

if 'run' in TEST_CONFIG['scripts']:
    TEST_CONFIG['scripts']['run'].replace('~', str(Path.home()))
    os.system(TEST_CONFIG['scripts']['run'])

if 'postrun' in TEST_CONFIG['scripts']:
    os.system(TEST_CONFIG['scripts']['postrun'])
