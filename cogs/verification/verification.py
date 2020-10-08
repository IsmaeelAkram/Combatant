import discord
from discord.ext import commands
from utils import embed, config
import asyncio
import json


class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vars = json.load(open("./vars.json"))
        self.emojis = self.vars['emojis']
        self.icons = self.vars['icons']

    async def start_verification(self, user: discord.User, guild: discord.Guild):
        await user.send(embed=embed.Embed(title="Verification", description="What is your Riot ID? You have 60 seconds to answer.\n\n**Example: Combatant#0001**", image=self.bot.user.avatar_url))

        def check(message):
            return message.channel.type == discord.ChannelType.private

        try:
            riot_id = await self.bot.wait_for('message', check=check, timeout=60)
        except asyncio.TimeoutError:
            await user.send(embed=embed.Embed(title="Verification timed out."))
            return

        GuildConfig = config.Config(guild.id)
        await GuildConfig.verify(self.bot, guild, user, riot_id.content)

        await user.send(embed=embed.Embed(title="Verification successful."))
