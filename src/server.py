# @file: server.python
# @author: Daniel Yuan
# @brief: Holds server and server information

import pickle

from .ec2 import EC2
from .constants import *

# Global ec2 instance
with open(ENV_FILE, 'rb') as env:
    private_constants = pickle.load(env)
ec2 = EC2(private_constants)

class Server(object):
    def __init__(self, name, instance, description):
        self.name = name
        self.instance = instance
        self.description = description

    def getName(self):
        return self.name

    def getInstance(self):
        return self.instance

    def getDescription(self):
        return self.description

    def setInstance(self, instance):
        self.instance = instance

    # Starts the server
    def start(self):
        ec2.startInstance(self.instance)

    # Stops the server
    def stop(self):
        ec2.stopInstance(self.instance)

    # Calls save on the screen with server
    def save(self):
        cmd = "screen -S " + self.name + " -p 0 -X stuff 'save-all\n'"
        ec2.sendCommand(self.instance, cmd)
