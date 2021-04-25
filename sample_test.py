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

# Parse board map
with open(f"{Path.home()}/tock-test-harness/board.map.yml", 'r') as board_map_yml:
    BOARD_MAP = load(board_map_yml, Loader=Loader)

# Lookup board
if 'env' in TEST_CONFIG:
    if 'board' in TEST_CONFIG['env']:
        if TEST_CONFIG['env']['board'] in BOARD_MAP:
            # TODO: Create a subroutine to check board object
            BOARD_MODEL = TEST_CONFIG['env']['board']
            BOARD_INFO = BOARD_MAP[BOARD_MODEL]
            BOARD_PATH = f"boards/{BOARD_INFO['brand']}/{BOARD_INFO['model']}"
            TOCK_PATH = f"{Path.home()}/actions-runner/_work/tock/tock"

            # Change to the corresponding path of the board
            os.chdir(f"{TOCK_PATH}/{BOARD_PATH}")

            # Compile
            os.system('make install')

            # Install App list
            # This is not a maintainable design, TODO: redo this
            if 'app' in TEST_CONFIG['env']:
                for app in TEST_CONFIG['env']['app']:
                    if BOARD_INFO['series'] == 'nrf52dk':
                        os.system(f"echo '1' | tockloader install --board nrf52dk --jlink {app}")
