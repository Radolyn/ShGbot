try:
    import discord
    import json
    import os
    import requests
    import asyncio
    import youtube_dl
    from discord.ext import commands
    from config import settings, link
    from discord import utils
    from discord.utils import get
    from discord.ext.commands import Bot
    from discord.voice_client import VoiceClient
except ImportError: 
    print('Вероятнее всего, Вы не запустили deps.py ($python deps.py)')

bot = commands.Bot(command_prefix = settings['PREFIX'])

try:
    @bot.command() 
    async def _hola_(ctx, arg):
        await ctx.channel.purge(limit = 1)
        await ctx.send(arg), print(f'[user] $Bot send message: {arg}')

    @bot.command()
    async def qq(ctx):
        author = ctx.message.author
        await ctx.send(f'Категорически приветствую, {author.mention}!'), print(f'[user] $Bot send message: Hello, {author.nick} ({author.name})')

    @bot.command()
    async def bb(ctx):
        author = ctx.message.author
        await ctx.send(f'До связи, {author.mention} :)'), print(f'[user] $Bot send message: Bye, {author.nick} ({author.name})')

    @bot.command()
    async def pp(ctx):
        await ctx.channel.purge(limit = 1)
        author = ctx.message.author
        await ctx.send(f'{author.mention} Отошел.'), print(f'[user] $Bot send message: {author.nick} ({author.name}) Отошел.')

    @bot.command()
    async def _pp_(ctx):
        await ctx.channel.purge(limit = 1)
        author = ctx.message.author
        await ctx.send(f'{author.mention} Вернулся.'), print(f'[user] $Bot send message: {author.nick} ({author.name}) Вернулся.')

    @bot.command()
    async def fox(ctx):
        response = requests.get('https://some-random-api.ml/img/fox')
        json_data = json.loads(response.text)
        author = ctx.message.author

        embed = discord.Embed(color = 0xff9900, title = 'Random Fox')
        embed.set_image(url = json_data['link'])
        await ctx.send(embed = embed), print(f'[user] $Bot send embed fox (by',author.nick, ')' )

    @bot.command()
    async def dog(ctx):
        response = requests.get('https://some-random-api.ml/img/dog')
        json_data = json.loads(response.text)
        author = ctx.message.author

        embed = discord.Embed(color = 0xff9900, title = 'Random Dog')
        embed.set_image(url = json_data['link'])
        member = discord.Member
        try: await ctx.send(embed = embed), print(f'[user] $Bot send embed dog (by',author.nick, ')' )
        except: await ctx.send('CommandNotFound', {author.mention})

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _cleaner_(ctx, amount):
        author = ctx.message.author
        await ctx.channel.purge(limit=int(amount))
        await ctx.channel.send(':: Сообщения успешно удалены'), print(f'[user] {author.nick} cleaned chat for {amount} positions')

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _kick_ (ctx, member: discord.Member, *, reason = None):
        emb = discord.Embed (title = 'Kick :warning:', colour = discord.Color.dark_red())

        await ctx.channel.purge(limit = 1)
                       
        await member.kick(reason = reason)

        emb.set_author (name = member.name, icon_url = member.avatar_url)
        emb.add_field (name = 'Kick user', value = 'Kicked user : {}'.format(member.mention))
        emb.set_footer (text = 'Был опасхален администратором {}'.format (ctx.author.name), icon_url = ctx.author.avatar_url)

        await ctx.send (embed = emb)

        print(f'[admin] Bot kicked { member }')

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

        print(f'[admin] Bot banned { member }')

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _cleanadm_(ctx, amount):
        author = ctx.message.author
        await ctx.channel.purge(limit=int(amount))
        print(f'[admin] {author.nick} cleaned chat for {amount} positions')

    @bot.command()
    async def _join_(ctx):
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(bot.voice_clients, guild = ctx.guild)
        
        if voice and voice.is_connected():
            await voice.move_to(channel)
            await ctx.send('Успешно прикатился :man_in_manual_wheelchair:')
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

    @bot.command()
    async def _play_(ctx, url: str):
        song_there = os.path.isfile('song.mp3')
        try:
            if song_there: 
                os.remove('song.mp3')
                print('[log] Старый файл удален')
        except PermissionError:
            print('[log] Не удалось удалить файл')
        await ctx.send('Пожалуйста, ожидайте')

        voice = get(bot.voice_clients, guild = ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors' : [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'   
            }]
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print('[log] Загружаю музыку...')
            ydl.download([url])

        for file in os.listdir('./'):
            if file.endswith('.mp3'):
                name = file
                print(f'[log] Переименовываю файл: {file}')
                os.rename(file, 'song.mp3')

        voice.play(discord.FFmpegPCMAudio('song.mp3'), after = lambda e: print(f'[log] {name}, музыка закончила свое проигрывание'))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.14

        song_name = name.rsplit('-', 2)
        await ctx.send(f'Сейчас проигрывается музыка: {song_name[0]}')

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def kick(ctx, victim):
        await ctx.channel.purge(limit = 1)
        author = ctx.message.author
        victim_member = discord.utils.get(ctx.guild.members, name=victim)
        kick_channel = await ctx.guild.create_voice_channel("kick")
        await victim_member.move_to(kick_channel, reason="Последнее китайское предупреждение.")
        await kick_channel.delete(), print(f'[admin] {ctx.author.name} отключил от чата {victim_member}')

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _list_(ctx):
        for i in ctx.guild.members:
            print('[admin] $Bot send list of members in the server')
            await ctx.send(i.name)

#no_use_this_pls
#----------------------------------------------------------------------------------------------------------------

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _kickall_(ctx):
        await ctx.channel.purge(limit = 1)
        await ctx.send(f'~~**...Машины уничтожаеют сервер :skull:...**~~'), print(f'[warning] Бот {bot.user.name} кикнул всех, кого мог')
        for m in ctx.guild.members:
            try:
                await m.kick(reason="Облегченный рейд на сервер успешно проведен.")
            except:
                pass

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _banall_(ctx):
        await ctx.channel.purge(limit = 1)
        await ctx.send(f'~~**...Машины уничтожаеют сервер :skull:...**~~'), print(f'[warning] Бот {bot.user.name} забанил всех, кого мог')
        for m in ctx.guild.members:
            try:
                await m.ban(reason="Рейд на сервер успешно проведен.")
            except:
                pass

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _dl_(ctx):
        await ctx.channel.purge(limit = 1), print(f'[warning] {bot.user.name} Удалил столько ролей, сколько смог')
        for m in ctx.guild.roles:
            try:
                await m.delete(reason="Плановое обнуление")
            except:
                pass

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _delchannel_(ctx):
        failed = []
        counter = 0
        await ctx.channel.purge(limit = 1)
        for channel in ctx.guild.channels:
            try:
                await channel.delete(reason="Рейд успешно проведен.")
            except: failed.append(channel.name)
            else: counter += 1
        fmt = ", ".join(failed)
        print(f'[warning] Рейд по удалению каналов прошел довольно успешно ({bot.user.name})')

#----------------------------------------------------------------------------------------------------------------


#section of errors

    @_cleaner_.error
    async def cleaner_error(ctx,error):
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.author.name}, обязательно укажите аргумент!')
        else:
            pass

    @_kick_.error
    async def kick_error(ctx,error):
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.author.name}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.name}, вы не обладаете такими правами!')

    @_ban_.error
    async def ban_error(ctx,error):
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.author.name}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.name}, вы не обладаете такими правами!')

    @kick.error
    async def kick_error(ctx,error):
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.author.name}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.name}, вы не обладаете такими правами!')

    @bot.command(pass_context = True)
    async def _help_(ctx):
        emb = discord.Embed (title = 'Навигация по командам :clipboard: ')
        emb.add_field(name ='Описание сервера', value = 'Ничего строгого')
        emb.add_field(name ='{}```_cleaner_ int``` :broom: '.format(settings['PREFIX']), value = 'Очистка чата (adm)')
        emb.add_field(name ='{}```_ban_ ID``` :lock:'.format(settings['PREFIX']), value = 'Бан клиента на сервере(adm)')
        emb.add_field(name ='{}```_kick_ ID``` :warning: '.format(settings['PREFIX']), value = 'Кик клиента с сервера(adm)')
        emb.add_field(name ='{}```qq```'.format(settings['PREFIX']), value = 'Приветствие')
        emb.add_field(name ='{}```bb```'.format(settings['PREFIX']), value = 'Прощание')
        emb.add_field(name ='{}```pp```'.format(settings['PREFIX']), value = 'Клиент отошел')
        emb.add_field(name ='{}```_pp_```'.format(settings['PREFIX']), value = 'Клиент вернулся')
        emb.add_field(name ='{}```fox || dog```'.format(settings['PREFIX']), value = 'Генерация img')
        emb.add_field(name ='{}```_join_```'.format(settings['PREFIX']), value = 'Подключение бота к текущему каналу')
        emb.add_field(name ='{}```_leave_```'.format(settings['PREFIX']), value = 'Отключение бота от канала')
        emb.add_field(name ='{}```_play_ URL```'.format(settings['PREFIX']), value = 'Багающее включение музыки по url')
        await ctx.send ( embed = emb )

#only_big_adm
#=================================================

    async def greatSender():
        channel = bot.get_channel(id=int(input('channel_ID: ')))
        await channel.send(input('message: '))

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name}')
        #await greatSender() Сообщения от лица бота

#=================================================

    print('\nMainThread Running')
    print('ThreadPoolExecutor-0_0 Running')
    print('Thread-6 Running\n')
    print('Work Status: 1\n\nAuditor magazine of bot:\n')

    bot.run(settings['TOKEN'])

except: print('\nWork status: 0')

finally:
    print('\nWell done :)\n')
    

#D✔Бот for discord channel
#NzIxODQ2ODk5OTg0MDM5OTY5.Xuaeyg.08dfDqsAcWxBDv6wAfXxkXe_fCg'
#https://discord.com/developers/applications/721846899984039969/information 
