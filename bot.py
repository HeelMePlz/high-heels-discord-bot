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
        if message.author != bot.user:
            await message.add_reaction("⬆️")


@bot.tree.command(
    name="generate", description="Get the top 10 challenges and 5 extra substitutes."
)
async def send_challenges(interaction: discord.Interaction):
    count = 1
    challenges = await sort_challenges()

    channel_id = str(SPIN_CHANNEL_ID)
    channel = bot.get_channel(int(channel_id))

    output = "# Top 10 Challenges:\n"

    for challenge in challenges[:5]:
        challenge_output = f"**{count})** {challenge.get('challenge')} - **{challenge.get('reactions')}** ⬆️ - by <@{challenge.get('user')}> -> {challenge.get('link')}\n"
        output += challenge_output
        count += 1

    # split the top 10 into 2 challenges because of 2000 character limit
    output2 = ""

    for challenge in challenges[6:11]:
        challenge_output = f"**{count})** {challenge.get('challenge')} - **{challenge.get('reactions')}** ⬆️ - by <@{challenge.get('user')}> -> {challenge.get('link')}\n"
        output2 += challenge_output
        count += 1

    subs_output = "# Next 5 Substitute Challenges:\n"

    for challenge in challenges[11:16]:
        challenge_subs = f"**{count})** {challenge.get('challenge')} - **{challenge.get('reactions')}** ⬆️ - by {challenge.get('username')} -> {challenge.get('link')}\n"
        subs_output += challenge_subs
        count += 1

    await interaction.response.send_message(output)
    await channel.send(output2)
    await channel.send(subs_output)

    return


async def get_challenges():
    challenges = []

    channel_id = str(SPIN_CHANNEL_ID)
    channel = bot.get_channel(int(channel_id))

    async for message in channel.history():
        if len(message.content) < 125:
            text = message.content
        else:
            text = message.content[:125] + "..."

        stripped_text = text.replace("\n", "")

        # print("challenge:", stripped_text)
        reaction = discord.utils.get(message.reactions, emoji="⬆️")
        # print("reaction:", reaction)
        reaction_count = reaction.count
        # print("reaction_count:", reaction_count)
        user_id = message.author.id
        username = message.author.name
        # print("username:", username)
        message_url = message.jump_url

        challenges.append(
            {
                "challenge": stripped_text,
                "reactions": reaction_count,
                "user": user_id,
                "username": username,
                "link": message_url,
            }
        )

    # for challenge in challenges:
    #     print(challenge)

    return challenges


async def sort_challenges():
    challenges = await get_challenges()

    sorted_challenges = sorted(challenges, key=lambda d: d["reactions"], reverse=True)

    # for sorted_challenge in sorted_challenges:
    #     print(sorted_challenge)

    return sorted_challenges


bot.run(TOKEN)
