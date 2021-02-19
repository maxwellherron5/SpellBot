"""
Driver for SpellBot
Author: Maxwell Herron
Python Version: 3.8.6
"""

import os
import logging
import json

import urllib3
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Creating access to environment variables
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
DND_URL = os.getenv('DND_URL')

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    LOGGER.info("%s has connected to the server", bot.user.name)


@bot.command(name="spell", help="Enter the name of your spell and I'll tell you about it!")
async def on_message(ctx, spell: str):
    LOGGER.info("New message: %s", spell)
    msg = get_spell_details(spell)['desc']
    await ctx.send(msg)


@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

### API CALLS ###

def get_spell_details(spell: str) -> dict:
    """Makes a request to Open5e to access all details on the given spell.
    """
    http = urllib3.PoolManager()
    endpoint = f"{DND_URL}/spells/{spell}/"
    LOGGER.info("Request: %s", endpoint)
    res = http.request('GET', endpoint)
    LOGGER.info("GET REQUEST WITH RESPONSE CODE: %s", str(res.status))
    res = json.loads(res.data.decode('utf-8'))
    LOGGER.info(res)
    return res

bot.run(TOKEN)
