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
        await ctx.send(f'Категорически приветствую, {author.mention}!'), print(f'$Bot send message: Hello, {author.mention}')

    @bot.command()
    async def bb(ctx):
        author = ctx.message.author
        await ctx.send(f'До связи, {author.mention} :)'), print(f'$Bot send message: Bye, {author.mention}')

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
        member = discord.Member
        try: await ctx.send(embed = embed), print(f'$Bot send embed dog (by', {member, author.mention}, ')' )
        except: await ctx.send('CommandNotFound', {author.mention})

    @bot.command()
    async def _clear_(ctx, amount=None):
        await ctx.channel.purge(limit=int(amount))
        await ctx.channel.send(':: Сообщения успешно удалены')

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _kick_ (ctx, member: discord.Member, *, reason = None):
        emb = discord.Embed (title = 'Kick :camel:', colour = discord.Color.dark_red())

        await ctx.channel.purge(limit = 1)

        await member.kick(reason = reason)

        emb.set_author (name = member.name, icon_url = member.avatar_url)
        emb.add_field (name = 'Kick user', value = 'Kicked user : {}'.format(member.mention))
        emb.set_footer (text = 'Был опасхален администратором {}'.format (ctx.author.name), icon_url = ctx.author.avatar_url)

        await ctx.send (embed = emb)

        print(f'Bot kicked { member }')

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _ban_ (ctx, member: discord.Member, *, reason = f'Нарушение правил сервера. $Banlist.append(you)'):
        emb = discord.Embed (title = 'Ban :lock:', colour = discord.Color.dark_red())

        await ctx.channel.purge(limit = 1)

        await member.ban(reason = reason)

        emb.set_author (name = member.name, icon_url = member.avatar_url)
        emb.add_field (name = 'Ban user', value = 'Ban user : {}'.format(member.mention))
        emb.set_footer (text = 'Был смешан с асфальтом администратором {}'.format (ctx.author.name), icon_url = ctx.author.avatar_url)

        await ctx.send (embed = emb)

        print(f'Bot banned { member }')

    @bot.command()
    async def _banlist_(ctx):
        try:
            await ctx.guild.bans()
            print(1)
        except:
            print(0)

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
