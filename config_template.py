"""
Template to configure important variables and paths

Author: Darren Li
"""
from pathlib import Path

# Important Paths
WEB_ROOT_FILE = Path.home()
UA_SAVE_FILE = WEB_ROOT_FILE.joinpath('user_agent.csv')


# Important Variables
TIMEOUT = 15
MAX_RETRIES = 5