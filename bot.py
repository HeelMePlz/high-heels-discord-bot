import os
import random
import discord
import uuid
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")


@bot.command(name="hello")
async def hello_user(ctx):
    sender = ctx.message.author.id
    await ctx.send(f"Hello <@{sender}>!")


@bot.command(name="save")
async def save_image(ctx):
    # get the image from the message
    for attachment in ctx.message.attachments:
        if attachment.size < 8000000:
            # generate a name for the image
            id = uuid.uuid4()

            # save the image
            await attachment.save(f"images/{id}.jpg")
            await ctx.send("Image Saved.")
        else:
            await ctx.send("File size too big. Please ensure it is under 8MB.")


@bot.command(name="heels")
async def send_image(ctx):
    # pick a random image from the folder
    images = os.listdir("images/")
    print(images)
    image = random.choice(images)
    print(image)

    # send the image in a message
    file = discord.File(f"images/{image}")
    await ctx.send(file=file)


bot.run(TOKEN)
