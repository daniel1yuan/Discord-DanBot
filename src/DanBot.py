import discord
import asyncio
import random
import pickle
import os

client = discord.Client()

@client.event
async def on_ready():
    print('---------------')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('---------------')

@client.event
async def on_message(message):
    if message.content.startswith('!help'):
        await client.send_message(message.channel, "Commands")

client.run('str')
