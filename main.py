import discord
from discord.ext import commands
from config import settings

bot = commands.Bot(command_prefix = settings['PREFIX'])

@bot.command(pass_context=True) 
async def _hola_(ctx, arg):
    await ctx.send(arg)

@bot.command()
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(f'Hello, {author.mention}!')

bot.run(settings['TOKEN'])

#D✔Бот for discord channel
#NzIxODQ2ODk5OTg0MDM5OTY5.Xuaeyg.08dfDqsAcWxBDv6wAfXxkXe_fCg'
#https://discord.com/developers/applications/721846899984039969/information
