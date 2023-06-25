import os
import random
import uuid

import discord
from discord import app_commands
from discord.ext import commands


class HighHeelsCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(
        name="save",
        description="Attach an image of your favourite high heels to save to the bot.",
    )
    async def save_image(
        self, interaction: discord.Interaction, attachment: discord.Attachment
    ) -> None:
        if attachment.size < 8000000:
            id = uuid.uuid4()

            if os.path.exists("./images/") == False:
                os.mkdir("images")

            await attachment.save(f"images/{id}.jpg")

            file = discord.File(f"images/{id}.jpg")
            await interaction.response.send_message(content="Image Saved.", file=file)
        else:
            await interaction.response.send_message(
                "File size too big. Please ensure it is under 8MB.", ephemeral=True
            )

    @app_commands.command(
        name="heels", description="See a random picture of high heels!"
    )
    async def send_image(self, interaction: discord.Interaction) -> None:
        images = os.listdir("images/")
        image = random.choice(images)

        file = discord.File(f"images/{image}")
        await interaction.response.send_message(file=file)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(HighHeelsCog(client))
