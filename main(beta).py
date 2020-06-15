import discord
import json
import requests
import random
from discord.ext import commands
from config import settings

bot = commands.Bot(command_prefix = settings['PREFIX'])

list_of_channel = ["test2", "__test__", "__main__"]

try:
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

    print('\nMainThread Running')
    print('ThreadPoolExecutor-0_0 Running')
    print('Thread-6 Running\n')
    print('Work Status: Work now.\n\nSteps:\n')

    bot.run(settings['TOKEN'])

    @bot.command()
    async def tp(ctx):
        n = int(input("сколько раз вы хотите путешествий?"))
        b = str(input("кого хотите(без собачки)"))

        while n > 0:
           if '$move' in message.content.upper():
                author = message.author
                x = random.randint(0, 2)
                list2 = list_of_channel[x]
                channel = discord.utils.find(lambda y: list_of_channel == 'list', message.server.channels)
                await client.move_member(author, channel)
                n -= 1

except discord.ext.commands.errors.CommandNotFound: print(0)

finally:
    print('\nWell done ;)')
    

#D✔Бот for discord channel
#NzIxODQ2ODk5OTg0MDM5OTY5.Xuaeyg.08dfDqsAcWxBDv6wAfXxkXe_fCg'
#https://discord.com/developers/applications/721846899984039969/information
