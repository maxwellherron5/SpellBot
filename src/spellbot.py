"""
Driver for SpellBot. This bot gets triggered by server member commands to
query the public d&d API Open5e.
Author: Maxwell Herron
Python Version: 3.8.6
"""

import os
import logging
import json

import discord
from discord.ext import commands
from dotenv import load_dotenv

from api_utils import get_spell_details

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
    """Entry point for bot start-up.
    """
    LOGGER.info("%s has connected to the server", bot.user.name)


@bot.command(name="spell", help="Enter the name of your spell and I'll tell you about it! For now, please format as <spell-name>")
async def on_message(ctx, spell: str):
    """
    """
    LOGGER.info("New message: %s", spell)
    spell_details = get_spell_details(spell)

    # Formatting the output details into an embedded message
    msg = discord.Embed(title=f"{spell_details['Name']}", description="Here's all you need to know! (and probably more)")

    # Populating embedded message with all returned fields
    for field in spell_details:
        # Setting base value for empty fields
        if not spell_details[field]:
            spell_details[field] = "None"
        LOGGER.info("field --- %s", field)
        LOGGER.info("value --- %s", spell_details[field])
        msg.add_field(name=f"**{field}**", value=f"{spell_details[field]}", inline=False)
    msg.set_footer(text="...anything look weird here? Let me know!")

    await ctx.channel.send(embed=msg)


@bot.event
async def on_error(event, *args, **kwargs):
    """Handles any 
    """
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

bot.run(TOKEN)
