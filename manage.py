# @file: manage.py
# @author: Daniel Yuan
# @brief: Handles all server-side configuration as well as set up for DanBot

# Internal Modules
from src import ENV_FILE, SERVER_FILE, DEFAULT_SCREEN_NAME, DEFAULT_LOG_FILENAME, DEFAULT_LOG_FOLDER, DanBot, Server

# External Modules
import os
import sys
import argparse
import pickle
import logging as log
from datetime import datetime

# Argument Parsing
arg_parser = argparse.ArgumentParser(description='Script for handling server-side configuration and set up for DanBot')
arg_parser.add_argument('command', nargs='?', default='help', help='Command that should be run')
arg_parser.add_argument('options', nargs='*', help='Additional options for the specified command')

def loadFile(filename):
    if (os.path.isfile(filename)):
        with open(filename, 'rb') as env:
            return pickle.load(env)
    else:
        return {}

def saveObj(obj, filename):
    with open (filename, 'wb') as env:
        pickle.dump(obj, env)

# Setup global private variables for communication with AWS EC2 and the discord bot
def setup():
    # Information Needed:
    private_constants = {
        'aws_access_key_id': None,
        'aws_secret_access_key': None,
        'discord_bot_token': None,
    }

    # Request
    private_constants['aws_access_key_id'] = input('aws_access_key_id: ')
    private_constants['aws_secret_access_key'] = input('aws_secret_access_key: ')
    private_constants['aws_region'] = input('AWS Region: ')
    private_constants['discord_bot_token'] = input('Discord Bot Token: ')
    private_constants['discord_allowed_role_name'] = input('Allowed Role name for bot: ')

    # Save Constants to ENV file
    saveObj(private_constants, ENV_FILE)
    print ("Saved.")

def createServer(private_constants):
    name = input('Server name: ')
    instance = input('Instance Id: ')
    description = input('Description: ')

    server = Server(name, instance, description)
    serverObj = loadFile(SERVER_FILE)
    if name in serverObj:
        log.error('Server name already exists.')
    else:
        serverObj[name] = server
        saveObj(serverObj, SERVER_FILE)

def deleteServer(name):
    serverObj = loadFile(SERVER_FILE)
    if name in serverObj:
        del serverObj[name]
        saveObj(serverObj, SERVER_FILE)
        log.info('Deleted server.')
    else:
        log.info('Server not found.')

def initializeLogs():
    # Initialize Log FIle
    date_string = datetime.now().strftime('%m-%d-%y-%H-%M')
    log_file_name = DEFAULT_LOG_FILENAME + '_' + date_string + '.log'
    log_path = os.path.join(DEFAULT_LOG_FOLDER, log_file_name)

    # Make log folder if non-existent
    if (not os.path.exists(DEFAULT_LOG_FOLDER)):
        os.mkdir(DEFAULT_LOG_FOLDER)

    # Create logging environment
    log.basicConfig(
        format='%(levelname)s - %(asctime)s| %(message)s',
        datefmt='%m/%d/%Y %H:%M:%S',
        filename=log_path,
        level=log.INFO
    )

    # Supress boto logging
    log.getLogger('boto3').setLevel(log.ERROR)
    log.getLogger('botocore').setLevel(log.ERROR)

    # Print to stdout
    log.getLogger().addHandler(log.StreamHandler())

# Main function for discord server setups
def main(args):
    cmd = args.command
    options = args.options

    if cmd == 'help':
        # Help Command lists all commands, their options, and their purpose
        print ("test")
    elif cmd == 'setup':
        # Sets up server-side configuration for the discord bot
        setup()
    elif cmd == 'createserver':
        if (not os.path.isfile(ENV_FILE)):
            print ("Run \'python manage.py setup\' before trying to create a server")
        else:
            private_constants = loadFile(ENV_FILE)
            createServer(private_constants)
    elif cmd == 'deleteserver':
            deleteServer(private_constants)
    elif cmd == 'run':
        # Run discord bot
        if (not os.path.isfile(ENV_FILE)):
            print ("Run \'python manage.py setup\' before trying to run DanBot")
        else:
            initializeLogs()
            private_constants = loadFile(ENV_FILE)
            bot = DanBot(private_constants)

if __name__ == '__main__':
    try:
        args = arg_parser.parse_args()
        main(args)
    except KeyboardInterrupt:
        print ("System Exiting...")
    finally:
        print ("Saving critical information")
