import discord


def Embed(description=None, image=None, title=None, color=0xe82c3f, footer=None):
    embed = discord.Embed(description=description,
                          image=image, title=title, color=color)
    if footer != None:
        embed.set_footer(text=footer)
    return embed
