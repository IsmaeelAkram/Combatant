import discord
from discord.ext import commands
from utils import embed, config
import json


class CreateVerify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vars = json.load(open("./vars.json"))
        self.emojis = self.vars['emojis']
        self.icons = self.vars['icons']

    @commands.command(description="Create verification message")
    async def createverify(self, ctx: commands.Context):
        await ctx.message.delete()
        GuildConfig = config.Config(ctx.guild.id)
        await GuildConfig.create_verification_message(
            self.bot, ctx.channel.id, ctx.author.id)
