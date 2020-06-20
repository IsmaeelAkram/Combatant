import discord
from discord.ext import commands
from utils import embed
import json


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vars = json.load(open("./vars.json"))
        self.emojis = self.vars['emojis']
        self.icons = self.vars['icons']

    @commands.command(description="Shows all available commands.")
    async def help(self, ctx: commands.Context):
        await ctx.message.add_reaction("📧")
        target = ctx.message.author

        help_message = ""
        for command in self.bot.commands:
            help_message += f"`{command.name}` - **{command.description}**\n"

        await target.send(embed=embed.Embed(title="Combatant Commands", description=help_message))
