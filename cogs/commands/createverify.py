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

    @commands.command(description="Force verify someone's Riot ID (skipping verification process)")
    @commands.has_permissions(manage_roles=True)
    async def forceverify(self, ctx: commands.Context, user: discord.User, riot_id: str):
        await ctx.message.delete()
        GuildConfig = config.Config(ctx.guild.id)
        await GuildConfig.verify(self.bot, ctx.guild, user, riot_id)
        await ctx.channel.send(embed=embed.Embed(description=f"<@{user.id}> has been forcefully linked to Riot ID `{riot_id}` by <@{ctx.author.id}>"))

    @commands.command(description="Create verification message")
    @commands.has_permissions(manage_roles=True)
    async def createverify(self, ctx: commands.Context):
        await ctx.message.delete()
        GuildConfig = config.Config(ctx.guild.id)
        await GuildConfig.create_verification_message(
            self.bot, ctx.channel.id, ctx.author.id)
