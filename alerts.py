import os
from dotenv import load_dotenv

import discord
from discord.ext import tasks

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
TEST_CHANNEL_ID = os.getenv("TEST_CHANNEL_ID")

client = discord.Client()


@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("------")


@tasks.loop(seconds=10)
async def alert(TEST_CHANNEL_ID, event):
    # wait for the client to log in
    await client.wait_until_ready()

    # get the channel
    channel = client.get_channel(int(TEST_CHANNEL_ID))
    print("Got channel", channel.id)

    print("Sending Message")
    eventStart = f"{event} event is about to start!"
    await channel.send(eventStart)
    print("Message Sent")
    print("------")


event = "Central Park"
alert.start(TEST_CHANNEL_ID, event)

client.run(TOKEN)
