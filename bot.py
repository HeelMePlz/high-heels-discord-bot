import os
import random
import discord
import uuid
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    await bot.tree.sync()


@bot.tree.command()
async def hello_user(interaction: discord.Interaction):
    sender = interaction.user.mention
    await interaction.response.send_message(f"Hello {sender}!")


@bot.hybrid_command(name="save", with_app_command=True)
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


@bot.hybrid_command(name="heels", with_app_command=True)
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
