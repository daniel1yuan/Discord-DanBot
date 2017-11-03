# @file: ec2.py
# @author: Daniel Yuan
# @brief: Holds ec2 interface for DanBot

# External Modules
import boto3

class EC2(object):
    def __init__(self, private_constants):
        self.aws_access_key_id = private_constants['aws_access_key_id']
        self.aws_secret_access_key = private_constants['aws_secret_access_key']
        self.region = private_constants['aws_region']

        self.ec2 = boto3.resource('ec2', aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key, region_name=self.region)
        self.ssm = boto3.client('ssm', aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key, region_name=self.region)

    def startInstance(self, instanceId):
        instance = self.ec2.Instance(instanceId)
        instance.start()

    def stopInstance(self, instanceId):
        state,_ = self.getInstanceState(instanceId)
        instance = self.ec2.Instance(instanceId)
        instance.stop()

    def getIP(self, instanceId):
        instance = self.ec2.Instance(instanceId)
        return instance.public_ip_address

    def getInstanceState(self, instanceId):
        instance = self.ec2.Instance(instanceId)
        state = instance.state
        return state['Code'], state['Name']

    def sendCommand(self, instance, command):
        return self.ssm.send_command(InstanceIds=[instance], DocumentName='AWS-RunShellScript', Comment='Running Command',
                                     Parameters={'commands': [command]})
