# High Heels Discord Bot

A Discord bot I'm making to help me practice coding! :)

## Installation

These instructions are mostly for myself, so I can remember how to re-install the project.

### Development Environment

After cloning the repo, create a virtual environment and activate it:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Now you can install the packages using the requirements file:

```bash
pip install -r requirements.txt
```

The following command creates a `.env` file containing our environment variables:

```bash
echo -e "DISCORD_TOKEN=" >> .env
```

### Create the bot account and invite it to your Server

Head to <https://discord.com/developers/applications> and Create a New Application.

After creating your application, head to the Bot tab and create a new bot.

Then add the bot to a server using the OAuth2 tab, scroll down to scopes, check bot and visit the generated URL.

### Environment Variables

* `DISCORD_TOKEN` can be found in the Bot tab. Copy it and append to our `.env` file.

### Run the script

To run the script for the bot, simply run

```bash
python3 bot.py
```

## Running the bot as a process

I use PM2 to run the bot as a process in the background.

To install PM2:

```bash
npm install -g pm2
```

In the project directory, start the bot:

```bash
pm2 start bot.py --interpreter=/usr/bin/python3
```

### Useful commands

```bash
pm2 list                list all pm2 processes
pm2 stop bot.py         stop the bot
pm2 restart bot.py      restart the bot
```
