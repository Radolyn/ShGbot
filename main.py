import discord
import json
import requests
from discord.ext import commands
from config import settings
from discord import utils
from discord.utils import get
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient

bot = commands.Bot(command_prefix = settings['PREFIX'])

try:
    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name}')

    @bot.command() 
    async def _hola_(ctx, arg):
        await ctx.channel.purge(limit = 1)
        await ctx.send(arg), print(f'$Bot send message: {arg}')

    @bot.command()
    async def qq(ctx):
        author = ctx.message.author
        await ctx.send(f'Категорически приветствую, {author.mention}!'), print(f'$Bot send message: Hello, {author.nick} ({author.name})')

    @bot.command()
    async def bb(ctx):
        author = ctx.message.author
        await ctx.send(f'До связи, {author.mention} :)'), print(f'$Bot send message: Bye, {author.nick} ({author.name})')

    @bot.command()
    async def pp(ctx):
        await ctx.channel.purge(limit = 1)
        author = ctx.message.author
        await ctx.send(f'{author.mention} Отошел.'), print(f'$Bot send message: {author.nick} ({author.name}) Отошел.')

    @bot.command()
    async def _pp_(ctx):
        await ctx.channel.purge(limit = 1)
        author = ctx.message.author
        await ctx.send(f'{author.mention} Вернулся.'), print(f'$Bot send message: {author.nick} ({author.name}) Вернулся.')

    @bot.command()
    async def fox(ctx):
        response = requests.get('https://some-random-api.ml/img/fox')
        json_data = json.loads(response.text)
        author = ctx.message.author

        embed = discord.Embed(color = 0xff9900, title = 'Random Fox')
        embed.set_image(url = json_data['link'])
        await ctx.send(embed = embed), print(f'$Bot send embed fox (by',author.nick, ')' )

    @bot.command()
    async def dog(ctx):
        response = requests.get('https://some-random-api.ml/img/dog')
        json_data = json.loads(response.text)
        author = ctx.message.author

        embed = discord.Embed(color = 0xff9900, title = 'Random Dog')
        embed.set_image(url = json_data['link'])
        member = discord.Member
        try: await ctx.send(embed = embed), print(f'$Bot send embed dog (by',author.nick, ')' )
        except: await ctx.send('CommandNotFound', {author.mention})

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _cleaner_(ctx, amount=None):
        author = ctx.message.author
        await ctx.channel.purge(limit=int(amount))
        await ctx.channel.send(':: Сообщения успешно удалены'), print(f'{author.nick} cleaned chat for {amount} positions')

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _kick_ (ctx, member: discord.Member, *, reason = None):
        emb = discord.Embed (title = 'Kick :skull:', colour = discord.Color.dark_red())

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
    @commands.has_permissions(administrator = True)
    #not all compiled (has problems);
    async def _mute_ (ctx, member: discord.Member):
        await ctx.channel.purge(limit = 1)
        emb = discord.Embed (title = 'Mute :mute:', colour = discord.Color.gold())
        mute_role = discord.utils.get(ctx.message.guild.roles, name = 'MUTED')
        await member.add_roles (mute_role)
        emb.set_author (name = member.name, icon_url = member.avatar_url)
        emb.add_field (name = 'MUTE', value = 'Muted user : {}'.format(member.mention))
        emb.set_footer (text = 'Был помещён в мут администратором {}'.format (ctx.author.name), icon_url = ctx.author.avatar_url)
        await ctx.send (embed = emb)#not work!!!

    @bot.command()
    async def _join_(ctx):
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(bot.voice_clients, guild = ctx.guild)
        
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            await ctx.send('Успешно прикатился :man_in_manual_wheelchair:')

    @bot.command()
    async def _leave_(ctx):
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(bot.voice_clients, guild = ctx.guild)
        
        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send('Успешно откатился :camel:')
        else:
            await voice.disconnect()
            await ctx.send('Успешно откатился :camel:')

#section of errors

    @_cleaner_.error
    async def cleaner_error(ctx,error):
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.author.name}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.name}, вы не обладаете такими правами!')

    @_kick_.error
    async def kick_error(ctx,error):
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.author.name}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.name}, вы не обладаете такими правами!')

    @bot.command(pass_context = True)
    async def _help_(ctx):
        emb = discord.Embed (title = 'Навигация по командам :clipboard: ')
        emb.add_field(name ='Описание сервера', value = 'Описание приняло ислам')
        emb.add_field(name ='{}```_cleaner_ int``` :broom: '.format(settings['PREFIX']), value = 'Очистка чата (adm)')
        emb.add_field(name ='{}```_ban_ ID``` :lock:'.format(settings['PREFIX']), value = 'Бан клиента с сервера(adm)')
        emb.add_field(name ='{}```_kick_ ID``` :skull: '.format(settings['PREFIX']), value = 'Кик клиента с сервера(adm)')
        emb.add_field(name ='{}```qq```'.format(settings['PREFIX']), value = 'Приветствие')
        emb.add_field(name ='{}```bb```'.format(settings['PREFIX']), value = 'Прощание')
        emb.add_field(name ='{}```pp```'.format(settings['PREFIX']), value = 'Клиент отошел')
        emb.add_field(name ='{}```_pp_```'.format(settings['PREFIX']), value = 'Клиент вернулся')
        emb.add_field(name ='{}```fox || dog```'.format(settings['PREFIX']), value = 'Генерация img')
        emb.add_field(name ='{}```_join_```'.format(settings['PREFIX']), value = 'Подключение бота к текущему каналу')
        emb.add_field(name ='{}```_leave_```'.format(settings['PREFIX']), value = 'Отключение бота от канала')
        await ctx.send ( embed = emb )

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
