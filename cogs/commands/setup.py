import discord
from discord.ext import commands
from discord.utils import get
from utils import embed, config
import json
import asyncio


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vars = json.load(open("./vars.json"))
        self.emojis = self.vars['emojis']
        self.icons = self.vars['icons']

    @commands.command(description="Helps you set up the bot")
    @commands.has_permissions(manage_roles=True)
    async def setup(self, ctx: commands.Context):
        await ctx.channel.send(embed=embed.Embed(description="Thanks for using Combatant! Here's the super simple setup guide!"))

        if not get(ctx.guild.roles, name="Host"):
            ctx.guild.create_role(name="Host")

        if not get(ctx.guild.roles, name="Valorant Linked"):
            ctx.guild.create_role(name="Valorant Linked")

        await ctx.channel.send(embed=embed.Embed(description="The first thing you have to do is make a channel (ideally named `#link-valorant`) where people can't talk. This channel will be for the account verification message. Once you have made it, type **next**.", footer="To cancel, type cancel"))
        try:
            confirmation = await self.bot.wait_for('message', check=check, timeout=600)
            if(confirmation == "next"):
                pass
            if(confirmation == "cancel"):
                await ctx.channel.send(embed=embed.Embed(title="Setup cancelled."))
                return
        except asyncio.TimeoutError:
            await user.send(embed=embed.Embed(title="You took more than 10 minutes to tell me the channel name. Begin the setup process again with `v!setup`."))
            return

        await ctx.channel.send(embed=embed.Embed(description="Now make another channel (ideally named `#valorant-scrims`) where only people with the `Host` rank can talk. This channel will be to announce new scrims. Once you have made it, type **next**.", footer="To cancel, type cancel"))
        try:
            confirmation = await self.bot.wait_for('message', check=check, timeout=600)
            if(confirmation == "next"):
                pass
            if(confirmation == "cancel"):
                await ctx.channel.send(embed=embed.Embed(title="Setup cancelled."))
                return
        except asyncio.TimeoutError:
            await user.send(embed=embed.Embed(title="You took more than 10 minutes to tell me the channel name. Begin the setup process again with `v!setup`."))
            return

        await ctx.channel.send(embed=embed.Embed(description="The last thing you have to do is create a verification message in scrim announcements channel by typing `v!createverify` in that channel. Once you have made it, type **next**.", footer="To cancel, type cancel"))
        try:
            confirmation = await self.bot.wait_for('message', check=check, timeout=600)
            if(confirmation == "next"):
                pass
            if(confirmation == "cancel"):
                await ctx.channel.send(embed=embed.Embed(title="Setup cancelled."))
                return
        except asyncio.TimeoutError:
            await user.send(embed=embed.Embed(title="You took more than 10 minutes to tell me the channel name. Begin the setup process again with `v!setup`."))
            return

        await ctx.channel.send(embed=embed.Embed(description="You're done! To start matches, type `v!startmatch <description` in the scrim announcements channel!"))
