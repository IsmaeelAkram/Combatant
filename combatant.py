import discord
from discord.ext import commands
import chalk
import json

from cogs.commands import createverify, help
from cogs.verification import verification
from cogs.matches.match import Match

from utils import config

vars = json.load(open('./vars.json'))
bot = commands.Bot("v!")
bot.remove_command("help")

cogs = []


def add_cog(cog):
    bot.add_cog(cog)
    cogs.append(cog)
    print(chalk.cyan(f"Loaded cog: {cog}"))


def register_cogs():
    add_cog(help.Help(bot))
    add_cog(createverify.CreateVerify(bot))
    add_cog(verification.Verification(bot))
    add_cog(Match(bot))
    print(chalk.yellow("Loading cogs..."))


def start():
    register_cogs()
    print(chalk.yellow("Bot starting..."))
    bot.run(vars["token"])


@bot.event
async def on_connect():
    print(chalk.yellow("Connected to Discord servers..."))

# Reactions
@bot.event
async def on_raw_reaction_add(reaction: discord.RawReactionActionEvent):
    if(bot.get_user(reaction.user_id) == bot.user):
        return

    channel = bot.get_channel(reaction.channel_id)
    GuildConfig = config.Config(reaction.guild_id)

    if(GuildConfig.check_reaction_verify(reaction.message_id) and bot.get_user(reaction.user_id) != bot.user):
        verificationProcess = verification.Verification(bot)
        await verificationProcess.start_verification(bot.get_user(reaction.user_id), bot.get_guild(reaction.guild_id))

    current_match_id = GuildConfig.check_reaction_match(reaction.message_id)
    if(current_match_id != None and bot.get_user(reaction.user_id) != bot.user):
        if(str(reaction.emoji) == "✋"):
            await GuildConfig.add_player_to_match(bot, bot.get_guild(
                reaction.guild_id), current_match_id, bot.get_user(reaction.user_id))
        if(str(reaction.emoji) == "✅"):
            await GuildConfig.dispatch_match(bot, current_match_id)


@bot.event
async def on_ready():
    print(chalk.green("Bot is ready."))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(f"VALORANT"))


@bot.event
async def on_disconnect():
    print(chalk.red("Disconnected from Discord servers..."))

start()
