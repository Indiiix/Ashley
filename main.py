import discord
import asyncio
import json
from cogs.logger import logger
from discord.ext import commands

from loadconfig import *
import loaduserdata
from cogs.downtime import DT

description = 'Manage party equipment, session rsvp, and optimal killing strats'

bot = commands.Bot(command_prefix=settings['prefix'], description=description)
bot.remove_command("help")
print('Preparing session . . .')


@bot.event
async def on_ready():
    await bot.edit_profile(username=settings['botName'])
    await bot.change_presence(game=discord.Game(name=settings['botStatus']))

    # Load Cogs
    for cog in cogs:
        try:
            bot.load_extension(cog)
            print(f'+{cog}')
        except Exception as err:
            print(f'Cog not found: ---{cog}')
            print(repr(err))

    # Load UserData
    try:
        loaduserdata.loaddata(bot)
    except Exception as err:
        print(f'User data not found.')
        print(f'{repr(err)}')


@bot.event
async def on_member_join(member):
    await bot.send_message(bot.get_channel(settings['defaultChannel']), "Welcome " + member.mention)
    embed = discord.Embed(color=0x008000)
    embed.add_field(name="!", value="“Here at the Psi’ Tshiks Adventuring Guild we accept adventurers"
                                    " from all across the globe in order to complete tasks ranging from the mundane"
                                    " to the deadly! As a member you will be expected to work well with others and be"
                                    " capable of moving and fighting as a team! Here as a Psi’ Tshik it would be your"
                                    " duty and responsibility to help and serve your community! Please make sure to visit"
                                    " the pinned messages for your introductory brochure!  One of our recruiters will be"
                                    " with you shortly for an interview!")
    await bot.send_message(bot.get_channel(settings['defaultChannel']), embed=embed)

    try:
        loaduserdata.loaddata(bot)
    except Exception as err:
        print(f'User data not found.')
        print(f'{repr(err)}')

    member.add_roles(settings['defaultRole'])

    await bot.send_message(member, "Welcome once again!  We at Psi\' Tshiks use a special magic network"
                                   "to keep track of everyone, you can learn more about what it and I can help"
                                   "you with by typing /help either here, or in any discord channel.  Make sure"
                                   "to register your character name using the /newCharacter command so I can start"
                                   "keeping track of your downtime hours!")


@bot.event
async def on_member_remove(member):
    await bot.send_message(bot.get_channel(settings['defaultChannel']),
                           "Goodbye " + member.display_name + ", we hope to see you again at the Psi' Tshiks Adventuring Guild!")


# Lists help commands
@bot.command(pass_context=True)
async def help(ctx, menu=None):
    if menu in ['pc', 'character', 'p', 'c']:
        embed = discord.Embed(title="Character Commands (Type without the <>)", color=0x008000)
        embed.add_field(name=f"{settings['prefix']}newCharacter <name>", value="Add a new player character",
                        inline=False)
        embed.add_field(name=f"{settings['prefix']}delCharacter <name>",
                        value="Deletes a player character ( CAREFUL )", inline=False)
        embed.add_field(name=f"{settings['prefix']}downtime", value="Shows your characters\' available downtime",
                        inline=False)
        embed.add_field(name=f"{settings['prefix']}useDowntime <name> <amount>",
                        value="Uses <amount> downtime from character <name>", inline=False)

    elif menu in ['dice', 'd']:
        embed = discord.Embed(title="Dice Commands (Type without the <>)", color=0x008000)
        embed.add_field(name=f"{settings['prefix']}roll <ndm+p>",
                        value="Roll an m-sided die n times and add/subtract p modifier ( p is optional ) ex. 1d20+3",
                        inline=False)
        embed.add_field(name=f"{settings['prefix']}rollAdv <ndm+p>",
                        value="Roll two m sided dice n times and add/subtract p modifier from the highest of the two rolls",
                        inline=False)
        embed.add_field(name=f"{settings['prefix']}rollDisadv <ndm+p>",
                        value="Roll two m sided dice n times and add/subtract p modifier from the lowest of the two rolls",
                        inline=False)
        embed.add_field(name=f"{settings['prefix']}stats", value="Rolls stats in 4d6-lowest form", inline=False)

    elif menu in ['admin', 'a']:
        embed = discord.Embed(title="Admin Commands (Type without the <>)", color=0x008000)
        embed.add_field(name=f"{settings['prefix']}say <message>", value="Has Ashley say <message>", inline=False)
        embed.add_field(name=f"{settings['prefix']}addDowntimeToCharacter <playername> <pcname> <amount>",
                        value="Adds <amount> downtime to <playername>'s character <pcname>", inline=False)
        embed.add_field(name=f"{settings['prefix']}addDowntimeToAll <amount>",
                        value="Adds <amount> downtime to ALL characters", inline=False)

    else:
        embed = discord.Embed(title="Command Menu (Type without the <>)", color=0x008000)
        embed.add_field(name=f"{settings['prefix']}help pc", value="Shows all character commands", inline=False)
        embed.add_field(name=f"{settings['prefix']}help dice", value="Shows all dice commands", inline=False)
        embed.add_field(name=f"{settings['prefix']}help admin",
                        value="Shows admin commands (Only admins have access)", inline=False)

    await bot.send_message(ctx.message.channel, embed=embed)

bot.run(settings['token'])
