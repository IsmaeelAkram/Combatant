import os
import sqlite3
import discord
from discord.ext import commands
from discord.utils import get
from utils import embed


class Config():
    def __init__(self, guild_id):
        self.guild_id = guild_id
        self.db = sqlite3.connect("main.sqlite")
        self.cursor = self.db.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS verification_messages (
            server_id INTEGER, 
            channel_id INTEGER,
            message_id INTEGER PRIMARY KEY, 
            creator_id INTEGER
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS verified_users (
            server_id INTEGER, 
            user_id INTEGER PRIMARY KEY, 
            riot_id TEXT
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            server_id INTEGER, 
            host_id INTEGER,
            channel_id INTEGER, 
            message_id INTEGER PRIMARY KEY, 
            match_id INTEGER, 
            description TEXT
        )
        """)
        self.db.commit()

    def get_channel_id(self):
        self.cursor.execute(
            f"SELECT * from verification_messages WHERE server_id={self.guild_id}")
        response = self.cursor.fetchone()

        server_id, channel_id, message_id, creator_id = response
        return channel_id

    def get_message_id(self):
        self.cursor.execute(
            f"SELECT * from verification_messages WHERE server_id={self.guild_id}")
        response = self.cursor.fetchone()

        server_id, channel_id, message_id, creator_id = response
        return message_id

    def get_creator_id(self):
        self.cursor.execute(
            f"SELECT * from verification_messages WHERE server_id={self.guild_id}")
        response = self.cursor.fetchone()

        server_id, channel_id, message_id, creator_id = response
        return creator_id

    async def create_verification_message(self, bot: commands.Bot, channel_id, creator_id):
        self.cursor.execute(
            f"SELECT * from verification_messages WHERE server_id={self.guild_id}")
        response = self.cursor.fetchone()

        if response:
            self.cursor.execute(
                f"DELETE from verification_messages WHERE server_id={self.guild_id}")

        channel: discord.TextChannel = bot.get_channel(channel_id)
        message = await channel.send(embed=embed.Embed(title="Verification",
                                                       description="React with the ✋ emoji to start the verification process.", image=bot.user.avatar_url))
        await message.add_reaction("✋")

        self.cursor.execute(
            f"INSERT INTO verification_messages VALUES ({self.guild_id}, {channel_id}, {message.id}, {creator_id})")
        self.db.commit()

    async def verify(self, bot: commands.Bot, guild: discord.Guild, user: discord.User, riot_id: str):
        self.cursor.execute(
            f"SELECT * from verified_users WHERE user_id={user.id}")
        response = self.cursor.fetchone()

        if response:
            self.cursor.execute(
                f"DELETE from verified_users WHERE user_id={user.id}")
        self.cursor.execute(
            f"INSERT INTO verified_users VALUES ({guild.id}, {user.id}, \"{riot_id}\")")
        self.db.commit()

        role = get(guild.roles, name="Valorant Linked")
        for member in bot.get_all_members():
            if(member.id == user.id):
                if(role < bot.top_role):
                    await member.add_roles()
                else:
                    user.send(embed=embed.Embed(
                        title="Oops!", description=f"I do not have permission to give you the `Valorant Linked` role in **{guild.name}**. Please contact an admin."))

    def get_player_riot_id(self, user: discord.User):
        self.cursor.execute(
            f"SELECT * from verified_users WHERE user_id={user.id}")
        response = self.cursor.fetchone()
        if not response:
            return None
        else:
            server_id, user_id, riot_id = response
            return riot_id

    def check_reaction_match(self, message_id):
        self.cursor.execute(
            f"SELECT * from matches WHERE message_id={message_id}")
        response = self.cursor.fetchone()
        if not response:
            return None
        else:
            server_id, host_id, channel_id, message_id, match_id, description = response
            return match_id

    def get_match_host(self, bot, match_id):
        self.cursor.execute(
            f"SELECT * from matches WHERE match_id={match_id}")
        response = self.cursor.fetchone()
        if not response:
            return None
        else:
            server_id, host_id, channel_id, message_id, match_id, description = response
            return bot.get_user(host_id)

    async def add_match(self, server_id, host_id, channel_id, message_id, match_id, description):
        self.cursor.execute(
            f"INSERT INTO matches VALUES ({server_id}, {host_id}, {channel_id}, {message_id}, {match_id}, \"{description}\")")
        self.db.commit()

    async def dispatch_match(self, bot, match_id):
        self.cursor.execute(
            f"SELECT * from matches WHERE match_id={match_id}")
        response = self.cursor.fetchone()
        self.cursor.execute(
            f"DELETE from matches WHERE match_id={match_id}")
        self.db.commit()
        server_id, host_id, channel_id, message_id, match_id, description = response
        message = await bot.get_channel(channel_id).fetch_message(message_id)

        matchEmbed = discord.Embed(
            color=0xe82c3f, title="Game Started", description=f"**This match has already been started. Please wait for the next one.**")
        matchEmbed.add_field(name="Description",
                             value=description, inline=False)

        await message.edit(embed=matchEmbed)

    async def add_player_to_match(self, bot, guild: discord.Guild, match_id, user: discord.User):
        host_riot_id = self.get_player_riot_id(
            self.get_match_host(bot, match_id))
        await user.send(embed=embed.Embed(title="How to Participate",
                                          description=f"**1.** Send a friend request in Valorant to `{host_riot_id}`.\n\n**2. **Join their game and wait until the match is started.\n\nThat's it!"))

    def check_reaction_verify(self, message_id):
        self.cursor.execute(
            f"SELECT * from verification_messages WHERE message_id={message_id}")
        response = self.cursor.fetchone()

        if not response:
            return False
        else:
            return True
