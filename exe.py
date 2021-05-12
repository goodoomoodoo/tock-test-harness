import os
import toml
import pathlib
import tempfile
import git
from pathlib import Path

# Get current directory
CUR_DIR = pathlib.Path().absolute()

# Get test.config.toml
f = open(str(CUR_DIR) + "/test.config.toml", "r")
config_toml = toml.load(f)

# Create temporary dir for boad
temp_board_dir = tempfile.mkdtemp()

# Clone the board 
repo_url = "https://github.com/jkchien/tock"
git.Repo.clone_from(repo_url, temp_board_dir, branch="master", depth=1)




