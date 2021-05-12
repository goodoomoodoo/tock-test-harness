import os
import toml
import pathlib
import tempfile
import git
import argparse
import util_functions
from pathlib import Path
from collections import defaultdict
from tqdm import tqdm




# Boards and Harnesses information
BOARDS = ["0", "nrf52840_dongle", "nrf52840dk", "nrfdk"]
TESTS = ["blink", "gpio"]
HARNESSES = ["0", "1"]
DATA = defaultdict(lambda: defaultdict(set))

# Constants
BOARD = " "
BOARD_PATH = " "
HARNESS = " "



# Dummy Harness data structure
for board in BOARDS:
    for harness in HARNESSES:
        for test in TESTS:
            DATA[board][harness].add(test)

# Get current directory
CUR_DIR = pathlib.Path().absolute()


# Parsing Arguments
parser = argparse.ArgumentParser(description="setup script for local testing environment.")
parser.add_argument("--board", help="specify the board path", type=str)
parser.add_argument("--harness", help="specify the harness_id", type=str)
parser.add_argument("--test", help="specify test app", type=str)
parser.add_argument("--config", help="set config flag to start configuration", action="store_true")
args = parser.parse_args()

# List Information for boards, harnesses, and tests
if(str(args.board) == "list"):
    print("==============================")
    for board in DATA.keys():
        print(board)
    print("==============================")

elif(args.board and str(args.harness) == "list"):
    if(args.board not in DATA.keys()):
        print("Board ", args.board, " does not exist")
    
    else:
        print("==============================")
        for harness in DATA[args.board].keys():
            print(harness)
        print("==============================")

elif(args.board and args.harness and str(args.test) == "list"):
    if(args.board not in DATA.keys()):
        print("Board ", args.board, " does not exist")
    elif(args.harness not in DATA[args.board].keys()):
        print("Harness", args.harness, " does not exist")
        
    print("==============================")
    for test in DATA[args.board][args.harness]:
        print(test)
    print("==============================")

# Request input
if(args.config):

    while(True):
        b = input("Model for tested board (0 for private customized boards): ")
        if(b not in BOARDS):
            print("Board ", b, " is invalid")
        else:
            break

    BOARD = b
    print("\n\n\n\n\n")
    print("If you want to change the path to board directory, insert here")
    bp = input("(defeault would be the action runner directory): ")
    
    if(bp == ""):
        BOARD_PATH = util_functions.find_path(b)

    else:
        BOARD_PATH = bp
    
    print("\n\n\n\n\n")
    print("If you want to specify harness id, insert here")

    while(True): 
        h = input("(defeault would be 0 which runs all applicable tests): ")
        if (h == ""):
            h = "0"
        if(h not in DATA[BOARD].keys()):
            print("Harness_id ", h, " for board ", BOARD, " is invalid")
        else:
            break


    if(h == ""):
        HARNESS = "0"
    
    else:
        HARNESS = h

    print("Creating Toml Configuration File...")

    with (CUR_DIR / "test_config.toml").open("w") as output_toml_file:
        final_dict = {
            "title": "Test Configuration Sample",

            "env": {
                "board": BOARD,
                "path": BOARD_PATH,
                "series": util_functions.find_series(BOARD),
                "harness_id": HARNESS,
            },

            "test": {
                "app": list(DATA[BOARD][HARNESS])
            }
        }

        toml.dump(final_dict, output_toml_file)

    

    





    
        

        




