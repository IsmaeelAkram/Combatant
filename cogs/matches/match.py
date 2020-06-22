import discord
from discord.ext import commands
from utils import embed
import json


class Match(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vars = json.load(open("./vars.json"))
        self.emojis = self.vars['emojis']
        self.icons = self.vars['icons']

    @commands.command(description="Start any type of Valorant match.")
    @commands.has_role("Host")
    async def startmatch(self, ctx: commands.Context, *, description: str):
        # if host Riot acount is not linked, stop
        match_id = int(datetime.datetime.now().strftime('%Y%m%d'))

        await ctx.message.delete()
        host: discord.User = ctx.author

        matchEmbed = discord.Embed(
            color=0xe82c3f, title="New Match", description=f"<@{host.id}> is hosting a new match. React with the :raised_hand: emoji to participate.")
        matchEmbed.add_field(name="Description",
                             value=description, inline=False)
        matchEmbed.add_field(
            name="Host", value=f"<@{host.id}>", inline=False)

        message = await ctx.channel.send(embed=matchEmbed)
        await message.add_reaction("✋")
        await message.add_reaction("✅")

        # Instructions to Host
        await host.send(embed=embed.Embed(title="Instructions as Host",
                                          description="As host, you have to accept all friend requests from people who want to join. \n\n Instructions have been delivered to participants on how to join and who to add."))

        # Add match to database
        GuildConfig = config.Config(ctx.guild.id)
        await GuildConfig.add_match(ctx.guild.id, host.id,
                                    ctx.channel.id, message.id, match_id, description)
