import os
from pathlib import Path
from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from lib.util import get_board_info

# Parse configuration
with open(f"{Path.home()}/tock-test-harness/test.config.yml", 'r') as config_yml:
    TEST_CONFIG = load(config_yml, Loader=Loader)

# Parse board map
with open(f"{Path.home()}/tock-test-harness/board.map.yml", 'r') as board_map_yml:
    BOARD_MAP = load(board_map_yml, Loader=Loader)

# If board exists, build the corresponding board
if BOARD_INFO := get_board_info(TEST_CONFIG, BOARD_MAP):
    BOARD_PATH = (f"boards/{BOARD_INFO['brand']}/{BOARD_INFO['model']}"
                  if 'brand' in BOARD_INFO
                  else f"boards/{BOARD_INFO['model']}")
    TOCK_PATH = f"{Path.home()}/actions-runner/_work/tock/tock"

    # Change to the corresponding path of the board
    os.chdir(f"{TOCK_PATH}/{BOARD_PATH}")

    # Compile
    os.system('make')
