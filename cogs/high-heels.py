import os
import random
import uuid

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.tree.command(
    name="save",
    description="Attach an image of your favourite high heels to save to the bot.",
)
async def save_image(interaction: discord.Interaction, attachment: discord.Attachment):
    if attachment.size < 8000000:
        # generate a name for the image
        id = uuid.uuid4()

        if os.path.exists("./images/") == False:
            os.mkdir("images")

        # save the image
        await attachment.save(f"images/{id}.jpg")

        # respond to the command with the image that was saved
        file = discord.File(f"images/{id}.jpg")
        await interaction.response.send_message(content="Image Saved.", file=file)
    else:
        await interaction.response.send_message(
            "File size too big. Please ensure it is under 8MB.", ephemeral=True
        )


@bot.tree.command(name="heels", description="See a random picture of high heels!")
async def send_image(interaction: discord.Interaction):
    # pick a random image from the folder
    images = os.listdir("images/")
    print(images)
    image = random.choice(images)
    print(image)

    # send the image in a message
    file = discord.File(f"images/{image}")
    await interaction.response.send_message(file=file)


bot.run(TOKEN)