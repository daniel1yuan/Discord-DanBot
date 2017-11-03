# @file: command.py
# @author: Daniel Yuan
# @brief: General class for a command for DanBot

import pickle

from .ec2 import EC2
from .constants import *

with open(ENV_FILE, 'rb') as env:
    private_constants = pickle.load(env)
ec2 = EC2(private_constants)

class Command(object):
    def __init__(self, client):
        # Help Text of this command
        self.help = None

        # String ID of the command
        self.id = None

        self.client = client

    def getHelp(self):
        return self.help

    def getId(self):
        return self.id

# Command that lists all servers
class ListServer(Command):
    def __init__(self, client, servers):
        Command.__init__(self, client)
        self.help = 'List all Servers handled by DanBot'
        self.id = 'list'
        self.servers = servers

    async def run(self, channel, message):
        for _,server in self.servers.items():
            await self.client.send_message(channel, 'Server Name: ' + server.getName() +
                                      '\nDescription: ' + server.getDescription())

class ServerStatus(Command):
    def __init__(self, client, servers):
        Command.__init__(self, client)
        self.help = 'List all Servers handled by DanBot'
        self.id = 'status'
        self.servers = servers

    async def run(self, channel, message):
        split_message = message.split()
        if (len(split_message) != 2):
            await self.client.send_message(channel, 'Invalid command format. Should be !status <server name>')
        else:
            server = split_message[1]
            if server in self.servers:
                instance = self.servers[server].getInstance()
                ip = ec2.getIP(instance)
                state = ec2.getInstanceState(instance)
                await self.client.send_message(channel, 'Server ip: ' + ip +
                                               '\nState: ' + state[1])
            else:
                await self.client.send_message(channel, 'Server not found. Try using !list')

class StartServer(Command):
    def __init__(self, client, servers):
        Command.__init__(self, client)
        self.help = 'List all Servers handled by DanBot'
        self.id = 'start'
        self.servers = servers

    async def run(self, channel, message):
        split_message = message.split()
        if (len(split_message) != 2):
            await self.client.send_message(channel, 'Invalid command format. Should be !status <server name>')
        else:
            server = split_message[1]
            if server in self.servers:
                instance = self.servers[server].getInstance()
                ip = ec2.startInstance(instance)
                await self.client.send_message(channel, 'Server Starting. \nIp: ' + ip)
            else:
                await self.client.send_message(channel, 'Server not found. Try using !list')

class StopServer(Command):
    def __init__(self, client, servers):
        Command.__init__(self, client)
        self.help = 'List all Servers handled by DanBot'
        self.id = 'stop'
        self.servers = servers

    async def run(self, channel, message):
        split_message = message.split()
        if (len(split_message) != 2):
            await self.client.send_message(channel, 'Invalid command format. Should be !status <server name>')
        else:
            server = split_message[1]
            if server in self.servers:
                instance = self.servers[server].getInstance()
                ec2.stopInstance(instance)
                await self.client.send_message(channel, 'Server Stopping.')
            else:
                await self.client.send_message(channel, 'Server not found. Try using !list')