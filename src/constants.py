# @file: constants.py
# @author: Daniel Yuan
# @brief: Holds global constants

import os
import __main__

WORKING_DIR = os.path.abspath(os.path.dirname(__main__.__file__))

# .env file that holds private variables
ENV_FILE = os.path.join(WORKING_DIR, '.env')

# .server file that holds all server information
SERVER_FILE = os.path.join(WORKING_DIR, '.server')

# Default Screen Name
DEFAULT_SCREEN_NAME = 'DanBotServer'

# Default Logs
DEFAULT_LOG_FOLDER = os.path.join(WORKING_DIR, 'logs')
DEFAULT_LOG_FILENAME = 'DanBot'
