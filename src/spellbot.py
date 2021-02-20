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

from api_utils import (
    get_spell_details,
    get_monster_details,
    RequestExecutionError
)

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

@bot.command(name="goodbot", help="Tell this bot how good they are")
async def on_message(ctx):
    """
    """
    await ctx.channel.send(u"thank you \U0001f604")

@bot.command(name="spell", help="Enter the name of your spell and I'll tell you about it! For now, please format as <spell-name>")
async def on_message(ctx, spell: str):
    """
    """
    LOGGER.info("New message: %s", spell)
    try:
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

    except RequestExecutionError as exc:
        msg = exc.message
        await ctx.channel.send(msg)


@bot.command(name="monster", help="Enter the name of the monster and I'll tell you about it! For now, please format as <monster-name>")
async def on_message(ctx, monster: str):
    """
    """
    LOGGER.info("New message: %s", monster)
    try:
        monster_details = get_monster_details(monster)
        # Formatting the output details into an embedded message
        msg = discord.Embed(title=f"{monster_details['Name']}", description="Here's all you need to know! (and probably more)")

        # Populating embedded message with all returned fields
        for field in monster_details:
            # Setting base value for empty fields
            if not monster_details[field]:
                monster_details[field] = "None"
            LOGGER.info("field --- %s", field)
            LOGGER.info("value --- %s", monster_details[field])
            if isinstance(monster_details[field], dict):
                msg.add_field(name=f"**{field}**", value=f"All details for field {field} below", inline=False)
                for key in monster_details[field]:
                    if len(str(monster_details[field][key])) > 1024:
                        pass
                    msg.add_field(name=f"{key}", value=f"{monster_details[field][key]}", inline=False)
            elif isinstance(monster_details[field], list):
                msg.add_field(name=f"**{field}**", value=f"All details for field {field} below", inline=False)
                for item in monster_details[field]:
                    for tup in item.items():
                        if len(str(tup[1])) > 1024:
                            pass
                        msg.add_field(name=f"**{tup[0]}**", value=f"{tup[1]}", inline=False)
            else:
                if len(str(monster_details[field])) <= 1024:
                    msg.add_field(name=f"**{field}**", value=f"{monster_details[field]}", inline=False)
        msg.set_footer(text="...anything look weird here? Let me know!")
        await ctx.channel.send(embed=msg)

    except RequestExecutionError as exc:
        msg = exc.message
        await ctx.channel.send(msg)


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
