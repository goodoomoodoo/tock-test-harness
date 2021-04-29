import os
import toml
from pathlib import Path
from lib.util import get_board_info

# Parse configuration
with open(f"{Path.home()}/tock-test-harness/test.config.toml", 'r') as config_toml:
    TEST_CONFIG = toml.load(config_toml)

# Parse board map
with open(f"{Path.home()}/tock-test-harness/board.map.toml", 'r') as board_map_toml:
    BOARD_MAP = toml.load(board_map_toml)

# Lookup board
if BOARD_INFO := get_board_info(TEST_CONFIG, BOARD_MAP):
    # TODO: Create a subroutine to check board object
    BOARD_PATH = BOARD_INFO['path']
    TOCK_PATH = f"{Path.home()}/actions-runner/_work/tock/tock"

    # Change to the corresponding path of the board
    os.chdir(f"{TOCK_PATH}/{BOARD_PATH}")

    # Compile
    os.system('make install')

    # Install App list
    # This is not a maintainable design, TODO: redo this
#            if 'app' in TEST_CONFIG['env']:
#                for app in TEST_CONFIG['env']['app']:
#                    if BOARD_INFO['series'] == 'nrf52dk':
#                        os.system(f"echo '1' | tockloader install --board nrf52dk --jlink {app}")
