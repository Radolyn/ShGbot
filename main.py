import discord
import json
import requests
from discord.ext import commands
from config import settings

bot = commands.Bot(command_prefix = settings['PREFIX'])

try:

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name}')

    @bot.command() 
    async def _hola_(ctx, arg):
        await ctx.send(arg), print(f'$Bot send message: {arg}')

    @bot.command()
    async def qq(ctx):
        author = ctx.message.author
        await ctx.send(f'Hello, {author.mention}!'), print(f'$Bot send message: Hello, {author.mention}')

    @bot.command()
    async def bb(ctx):
        author = ctx.message.author
        await ctx.send(f'See you later, {author.mention} :)'), print(f'$Bot send message: Bye, {author.mention}')

    @bot.command()
    async def pp(ctx):
        author = ctx.message.author
        await ctx.send(f'{author.mention} Отошел.'), print(f'$Bot send message: {author.mention} Отошел.')

    @bot.command()
    async def _pp_(ctx):
        author = ctx.message.author
        await ctx.send(f'{author.mention} Вернулся.'), print(f'$Bot send message: {author.mention} Вернулся.')

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
        try: await ctx.send(embed = embed), print('$Bot send embed dog (by', author.mention, ')' )
        except: await ctx.send('CommandNotFound', {author.mention})

    @bot.command()
    async def _clear_(ctx, amount=None):
        await ctx.channel.purge(limit=int(amount))
        await ctx.channel.send(':: Сообщения успешно удалены')

    print('\nMainThread Running')
    print('ThreadPoolExecutor-0_0 Running')
    print('Thread-6 Running\n')
    print('Work Status: 1\n\nSteps:\n')

    bot.run(settings['TOKEN'])

except: print('\nWork status: 0')

finally:
    print('\nWell done ;)')
    

#D✔Бот for discord channel
#NzIxODQ2ODk5OTg0MDM5OTY5.Xuaeyg.08dfDqsAcWxBDv6wAfXxkXe_fCg'
#https://discord.com/developers/applications/721846899984039969/information 
#https://discord.com/oauth2/authorize?client_id=721846899984039969&scope=bot&permissions=8
