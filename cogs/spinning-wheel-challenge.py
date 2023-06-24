import os

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("GUILD_ID")


class SpinningWheelChallengeCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(
        name="generate", description="Generate the top 15 challenges."
    )
    async def generate_challenges(self, interaction: discord.Interaction):
        channel = get_spinning_wheel_channel(self.client, discord.Object(id=str(GUILD)))
        messages = await get_messages(channel)
        sorted_messages = sort_by_upvotes(messages)

        await interaction.response.send_message(
            "Generating the top 15 challenges now..."
        )

        for index, message in enumerate(sorted_messages[:15]):
            await channel.send(challenge_output(index + 1, message))


def get_spinning_wheel_channel(
    client, guild: discord.Guild
) -> discord.abc.GuildChannel | None:
    for guild in client.guilds:
        for channel in guild.channels:
            if "spinning_wheel_challenge" in channel.name:
                return channel
        print("Spinning Wheel Channel not found. Are you sure it exists?")


async def get_messages(channel: discord.TextChannel) -> list:
    return [message async for message in channel.history()]


def get_upvotes_from_message(message: discord.Message) -> int:
    try:
        return discord.utils.get(message.reactions, emoji="⬆️").count
    except AttributeError:
        return 0


def sort_by_upvotes(messages: list) -> list:
    return sorted(
        messages, key=lambda message: get_upvotes_from_message(message), reverse=True
    )


def challenge_output(index: int, message: discord.Message) -> str:
    return f"""**{index})** {(message.content[:125] + "...") if len(message.content) > 125 else message.content}
    **Upvotes**: {get_upvotes_from_message(message)}
    **Submitted by**: {message.author.display_name}
    **Link to submission**: {message.jump_url}"""


async def setup(client: commands.Bot) -> None:
    await client.add_cog(SpinningWheelChallengeCog(client))
