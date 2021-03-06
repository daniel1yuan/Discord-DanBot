# @file: DanBot.py
# @author: Daniel Yuan
# @brief: Holds all code for the Discord bot DanBot

# Discord API dependencies
import discord
import asyncio

# External Modules
import logging as log
import random
import pickle
import os

# Internal Modules
from .constants import *
from .ec2 import *
from .command import *

def loadFile(filename):
    if (os.path.isfile(filename)):
        with open(filename, 'rb') as env:
            return pickle.load(env)
    else:
        return {}

def saveObj(obj, filename):
    with open (filename, 'wb') as env:
        pickle.dump(obj, env)

class DanBot(object):
    def __init__(self, private_constants):
        token = private_constants['discord_bot_token']
        self.allowedRole = private_constants['discord_allowed_role_name']
        self.ec2 = EC2(private_constants)
        client = discord.Client()
        self.client = client
        self.command = {}
        self._initCommands()

        @client.event
        async def on_ready():
            log.info('---------------')
            log.info('DanBot Initialized.')
            log.info('User: ' + client.user.name)
            log.info('Id: ' + client.user.id)
            log.info('---------------')

        @client.event
        async def on_message(message):
            content = message.content
            member = message.author
            roles = member.roles
            for key, cmd in self.command.items():
                if content.startswith(key):
                    if (self._isAllowed(roles)):
                        await cmd.run(message.channel, content)
                    else:
                        await client.send_message(message.channel, 'Nice Try buddo! I don\'t have commands for your role')

        client.run(token)

    # Initialize all commands
    def _initCommands(self):
        serverObj = loadFile(SERVER_FILE)

        # Commands
        commandHelp = CommandHelp(self.client)
        listServer = ListServer(self.client, serverObj)
        serverStatus = ServerStatus(self.client, serverObj)
        startServer = StartServer(self.client, serverObj)
        stopServer = StopServer(self.client, serverObj)

        self.command['!' + listServer.getId()] = listServer
        self.command['!' + serverStatus.getId()] = serverStatus
        self.command['!' + startServer.getId()] = startServer
        self.command['!' + stopServer.getId()] = stopServer
        self.command['!' + commandHelp.getId()] = commandHelp

    # Given roles, check if the role is allowed
    def _isAllowed(self, roles):
        for role in roles:
            if (role.name == self.allowedRole):
                return True
        return False
