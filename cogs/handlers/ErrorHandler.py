import discord
from discord.ext import commands
import json
from utils import embed


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if('You' in str(error)):
            softErrorEmbed = embed.Embed(
                title="Oops!", description=str(error))
            await ctx.channel.send(embed=embed.Embed())
        else:
            hardErrorEmbed = embed.Embed(
                title="Oops! An error seems to have occurred.", description=str(error), footer="Please report this to Mahjestic#9700.")
            await ctx.channel.send(embed=hardErrorEmbed)
