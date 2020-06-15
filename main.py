import discord
import json
import requests
from discord.ext import commands
from config import settings

bot = commands.Bot(command_prefix = settings['PREFIX'])

@bot.command() 
async def _hola_(ctx, arg):
    await ctx.send(arg)

@bot.command()
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(f'Hello, {author.mention}!')

@bot.command()
async def fox(ctx):
    response = requests.get('https://some-random-api.ml/img/fox')
    json_data = json.loads(response.text)
    author = ctx.message.author

    embed = discord.Embed(color = 0xff9900, title = 'Random Fox')
    embed.set_image(url = json_data['link'])
    await ctx.send(embed = embed), print('$Bot send embed fox (by ', author.mention, ')' )

@bot.command()
async def dog(ctx):
    response = requests.get('https://some-random-api.ml/img/dog')
    json_data = json.loads(response.text)
    author = ctx.message.author

    embed = discord.Embed(color = 0xff9900, title = 'Random Dog')
    embed.set_image(url = json_data['link'])
    await ctx.send(embed = embed), print('$Bot send embed dog (by', author.mention, ')' )


print('\nMainThread Running')
print('ThreadPoolExecutor-0_0 Running')
print('Thread-6 Running\n')
print('Work Status: Work now.\n\nSteps:\n')
bot.run(settings['TOKEN'])

#D✔Бот for discord channel
#NzIxODQ2ODk5OTg0MDM5OTY5.Xuaeyg.08dfDqsAcWxBDv6wAfXxkXe_fCg'
#https://discord.com/developers/applications/721846899984039969/information
