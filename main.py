import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())
        self.initial_extensions = ["cogs.high-heels", "cogs.spinning-wheel-challenge"]

    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)

    async def close(self):
        await super().close()
        await self.session.close()

    async def on_ready(self):
        print("Ready!")
        print(f"Synced {str(len(await self.tree.sync()))} Commands")


bot = MyBot()
bot.run(TOKEN)
