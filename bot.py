import os
import random
import discord
import uuid
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
SPIN_CHANNEL_ID = os.getenv("SPIN_CHANNEL_ID")

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    await bot.tree.sync()


@bot.tree.command(name="hello", description="The bot will say hello to you.")
async def hello_user(interaction: discord.Interaction):
    sender = interaction.user.mention
    await interaction.response.send_message(f"Hello {sender}!")


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
    

@bot.event
async def on_message(message: discord.Message):
    if str(message.channel.id) == SPIN_CHANNEL_ID:
        await message.add_reaction("⬆️")
        
@bot.tree.command(name="generate", description="Get the top 10 challenges.")
async def send_challenges(interaction: discord.Interaction):
    
    challenges = await get_challenges()
    
    return

async def get_challenges():
    index = 1
    challenges = []
    
    channel_id = str(SPIN_CHANNEL_ID)
    channel = bot.get_channel(int(channel_id))
    
    async for message in channel.history():
        
        count = index
        #print("count:", count)
        text = message.content
        #print("text:", text)
        reaction = discord.utils.get(message.reactions, emoji="⬆️")
        #print("reaction:", reaction)
        reaction_count = reaction.count
        #print("reaction_count:", reaction_count)
        username = message.author.name
        # print("username:", username)
        
        challenges.append({"id": count, "challenge": text, "reactions": reaction_count, "user": username})
        index += 1
        
    for challenge in challenges:
        print(challenge)
    
    return challenges


bot.run(TOKEN)
