import discord


def Embed(description=None, image=None, title=None, color=0xe82c3f, footer=None):
    return discord.Embed(description=description, image=image, title=title, color=color).set_footer(text=footer)
