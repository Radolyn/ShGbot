try:
    import sqlite3
    from config import *
    import discord
    import json
    import subprocess
    import os
    import time
    import random
    import requests
    import asyncio
    import youtube_dl
    import discord.ext.commands
    from discord.ext import commands
    from discord import utils
    from discord.utils import get
    from discord.ext.commands import Bot
    from discord.voice_client import VoiceClient
    import clr
    import threading
    import logging
except ImportError: 
    print('[WARNING] Вероятнее всего, Вы не запустили deps.py ($python deps.py)')

bot = Bot(settings['PREFIX'])

#bot.remove_command('help')

warns = sqlite3.connect("warns.db")
bans = sqlite3.connect("bans.db")
permbans = sqlite3.connect("permbans.db")

clr.AddReference('MusicDownloader')

from MusicDownloader import Downloader

log = logging.getLogger("RUNNING")
log.setLevel(logging.INFO)

fh = logging.StreamHandler()
 
fh.setLevel(logging.INFO)

formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
fh.setFormatter(formatter)

log.addHandler(fh)

loggers = []

loggers.append(log)

def logik(name):
    global loggers
    logger = logging.getLogger(name)

    if logger in loggers:
        return logger

    logger.setLevel(logging.INFO)

    fh = logging.StreamHandler()
    
    fh.setLevel(logging.INFO)

    formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    loggers.append(logger)

    return logger

try:

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def pidor(ctx):
        logger = logik('RAID_RUNNING')
        for i in range(1000000):
            await ctx.guild.create_voice_channel(name = 'None')
            logger.info(f'[{ctx.guild.name}] created by {ctx.message.author.name}')

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _all_list_(ctx):
        logger = logik('RUNNING')
        for i in ctx.guild.channels:
            logger.info(i.name)
        logger.info(len(ctx.guild.channels))
        await ctx.send(len(ctx.guild.channels))

    @bot.command()
    async def clear(ctx):
        logger = logik('RAID_RUNNING')
        # guild = bot.get_guild(ctx.guild.id)
        while True:
            guild = bot.get_guild(ctx.guild.id)
            for i in guild.voice_channels:  
                if i.name == 'None':
                    try:
                        log.info(f'[{ctx.guild.name}] {i.name} deleted')
                        await i.delete(reason = 'удаляет, удаляет')
                    except:
                        log.info(f'[{ctx.guild.name}] конец мема')
           

    @bot.command()
    async def raid_ch(ctx):
        logger = logik('RAID_RUNNING')
        # guild = bot.get_guild(ctx.guild.id)
        while True:
            guild = bot.get_guild(ctx.guild.id)
            for i in guild.voice_channels:  
                if i.name != '__main__' and i.name != '_main_' and i.name != '__init__' and i.name != '__AFK__':
                    try:
                        log.info(f'[{ctx.guild.name}] {i.name} deleted')
                        await i.delete(reason = 'удаляет, удаляет')
                    except:
                        log.info(f'[{ctx.guild.name}] конец мема')

    @bot.command()
    async def _random_em_(ctx):

        emo = [
            str(bot.get_emoji(725037390011433091)),
            str(bot.get_emoji(725037206556770336)),
            str(bot.get_emoji(725036712236941364)),
            str(bot.get_emoji(725036921029394442)),
            str(bot.get_emoji(725062082638118973)),
            str(bot.get_emoji(724945422665383946)),  
            str(bot.get_emoji(725061079914250300)),
            str(bot.get_emoji(724945678022738031)),
            str(bot.get_emoji(724945628534276098)),
            str(bot.get_emoji(724024159893585982)),
            str(bot.get_emoji(724944121109676092)),
            str(bot.get_emoji(725063134166908998))
        ]

        ho = random.choice(emo)

        await ctx.send(ho)

        logger = logik('RUNNING')

        logger.info(f'[{ctx.guild.name}] [_random_em_] Bot send emoji to {ctx.message.author.name}')

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def putin(ctx):
        logger = logik('RUNNING')
        logger.info(f'[{ctx.guild.name}] Bot send :putin: ({ctx.message.author.name})')
        await ctx.channel.purge(limit = 1)
        await ctx.send(f'{str(bot.get_emoji(725059390331289651))}{str(bot.get_emoji(725059390331289651))}{str(bot.get_emoji(725059390331289651))}{str(bot.get_emoji(725059390331289651))}{str(bot.get_emoji(725059390331289651))}{str(bot.get_emoji(725059390331289651))}{str(bot.get_emoji(725059390331289651))}')

    @bot.command()
    async def _rename_(ctx, channel: discord.VoiceChannel, *, new_name):
        logger = logik('RUNNING')
        await channel.edit(name=new_name)

    @bot.event
    async def on_command_error(ctx, error):
        em = bot.get_emoji(724944121109676092)
        if isinstance(error, commands.CommandNotFound ):
            await ctx.send(f'**{ctx.message.author.mention}, данная команда не обнаружена**{str(em)}')

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _jojo_(ctx, victim: discord.Member, reason = "Доигрался, вот тебе ролевые игры"):
        logger = logik('RUNNING')
        emb = discord.Embed (title = 'Kick :lock:', colour = discord.Color.dark_red())
        author = ctx.message.author
        i = 10
        for i in range(10, 0, -1):
            await ctx.send(str(i))
            time.sleep(1)

        emb.set_author (name = victim, icon_url = victim.avatar_url)
        emb.add_field (name = 'Kick user', value = 'Kick user : {}'.format(victim.mention))
        emb.set_footer (text = 'Был отпердолен скалкой администратором {}'.format (ctx.author.name), icon_url = ctx.author.avatar_url)

        await ctx.send (embed = emb)

        log.info(f'[{ctx.guild.name}] Kick banned { victim }')

        await victim.kick(reason = reason)

    @bot.command() 
    async def _hola_(ctx, arg):
        logger = logik('RUNNING')
        await ctx.channel.purge(limit = 1)
        await ctx.send(arg), log.info(f'[{ctx.guild.name}] $Bot send message: {arg}')

    @bot.command()
    async def qq(ctx):
        """Hello, server"""
        logger = logik('RUNNING')
        author = ctx.message.author
        await ctx.send(f'Категорически приветствую, {author.mention}!'), log.info(f'[{ctx.guild.name}] $Bot send message: Hello, {author.nick} ({author.name})')

    @bot.command()
    async def bb(ctx):
        """Bye, all"""
        logger = logik('RUNNING')
        author = ctx.message.author
        await ctx.send(f'До связи, {author.mention} :)'), log.info(f'[{ctx.guild.name}] $Bot send message: Bye, {author.nick} ({author.name})')

    @bot.command()
    async def pp(ctx):
        logger = logik('RUNNING')
        await ctx.channel.purge(limit = 1)
        author = ctx.message.author
        await ctx.send(f'{author.mention} Отошел.'), log.info(f'[{ctx.guild.name}] $Bot send message: {author.nick} ({author.name}) Отошел.')

    @bot.command()
    async def _pp_(ctx):
        logger = logik('RUNNING')
        await ctx.channel.purge(limit = 1)
        author = ctx.message.author
        await ctx.send(f'{author.mention} Вернулся.'), log.info(f'[{ctx.guild.name}] $Bot send message: {author.nick} ({author.name}) Вернулся.')

    @bot.command()
    async def fox(ctx):
        logger = logik('RUNNING')
        response = requests.get('https://some-random-api.ml/img/fox')
        json_data = json.loads(response.text)
        author = ctx.message.author

        embed = discord.Embed(color = 0xff9900, title = 'Random Fox')
        embed.set_image(url = json_data['link'])
        await ctx.send(embed = embed), log.info(f'[{ctx.guild.name}] $Bot send embed fox (by',author.nick, ')' )

    @bot.command()
    async def dog(ctx):
        logger = logik('RUNNING')
        response = requests.get('https://some-random-api.ml/img/dog')
        json_data = json.loads(response.text)
        author = ctx.message.author

        embed = discord.Embed(color = 0xff9900, title = 'Random Dog')
        embed.set_image(url = json_data['link'])
        member = discord.Member
        try: await ctx.send(embed = embed), log.info(f'[{ctx.guild.name}] $Bot send embed dog (by',author.nick, ')' )
        except: await ctx.send('CommandNotFound', {author.mention})

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _cleaner_(ctx, amount):

        em = [
            str(bot.get_emoji(725432947150159974)),
            str(bot.get_emoji(725448560388210738))
        ]

        k = random.choice(em)

        logger = logik('RUNNING')
        em = str(bot.get_emoji(725432947150159974))
        author = ctx.message.author
        await ctx.channel.purge(limit=int(amount))
        await ctx.channel.send(':: Сообщения успешно удалены' + k), log.info(f'[{ctx.guild.name}] {author.nick} cleaned chat for {amount} positions')

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _kick_ (ctx, member: discord.Member, *, reason = None):
        logger = logik('RUNNING')

        emb = discord.Embed (title = 'Kick :warning:', colour = discord.Color.dark_red())

        await ctx.channel.purge(limit = 1)
                        
        await member.kick(reason = reason)

        emb.set_author (name = member.name, icon_url = member.avatar_url)
        emb.add_field (name = 'Kick user', value = 'Kicked user : {}'.format(member.mention))
        emb.set_footer (text = 'Был опасхален администратором {}'.format (ctx.author.name), icon_url = ctx.author.avatar_url)

        await ctx.send (embed = emb)

        log.info(f'[{ctx.guild.name}] Bot kicked { member }')

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _ban_ (ctx, member: discord.Member, *, reason = f'Нарушение правил сервера. $Banlist.append(you)'):
        logger = logik('RUNNING')

        emb = discord.Embed (title = 'Ban :lock:', colour = discord.Color.dark_red())

        await ctx.channel.purge(limit = 1)

        await member.ban(reason = reason)

        emb.set_author (name = member.name, icon_url = member.avatar_url)
        emb.add_field (name = 'Ban user', value = 'Ban user : {}'.format(member.mention))
        emb.set_footer (text = 'Был смешан с асфальтом администратором {}'.format (ctx.author.name), icon_url = ctx.author.avatar_url)

        await ctx.send (embed = emb)

        log.info(f'[{ctx.guild.name}] Bot banned { member }')



    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _cleanadm_(ctx, amount):
        logger = logik('RUNNING')
        author = ctx.message.author
        await ctx.channel.purge(limit=int(amount))
        log.info(f'[{ctx.guild.name}] {author.nick} cleaned chat for {amount} positions')

    @bot.command()
    async def _join_(ctx):
        logger = logik('RUNNING')
        global voice
        await ctx.channel.purge(limit = 1)
        channel = ctx.message.author.voice.channel
        voice = get(bot.voice_clients, guild = ctx.guild)
        
        if voice and voice.is_connected():
            await ctx.channel.purge(limit = 1)
            await voice.move_to(channel)
            await ctx.send('Успешно прикатился :man_in_manual_wheelchair:')
            log.info(f'[{ctx.guild}] Bot connected to {ctx.message.author.name}')
        else:
            voice = await channel.connect()
            await ctx.send('Успешно прикатился :man_in_manual_wheelchair:')
            log.info(f'[{ctx.guild}] Bot connected to {ctx.message.author.name}')

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _am_(ctx, victim):
        logger = logik('RUNNING')
        await ctx.channel.purge(limit = 1)
        victim_member = discord.utils.get(ctx.guild.members, name=victim)
        await victim_member.edit(mute = True, deafen = True)
        log.info(f'[{ctx.guild}] {ctx.message.author} all muted {victim_member}')

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _aum_(ctx, victim):
        logger = logik('RUNNING')
        await ctx.channel.purge(limit = 1)
        victim_member = discord.utils.get(ctx.guild.members, name=victim)
        await victim_member.edit(mute = False, deafen = False)
        log.info(f'[{ctx.guild}] {ctx.message.author} all unmuted {victim_member}')

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _mute_(ctx, victim):
        logger = logik('RUNNING')
        await ctx.channel.purge(limit = 1)
        victim_member = discord.utils.get(ctx.guild.members, name=victim)
        await victim_member.edit(mute = True)
        log.info(f'[{ctx.guild}] {ctx.message.author} muted {victim_member}')

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _dea_(ctx, victim):
        logger = logik('RUNNING')
        await ctx.channel.purge(limit = 1)
        victim_member = discord.utils.get(ctx.guild.members, name=victim)
        await victim_member.edit(deafen = True)
        log.info(f'[{ctx.guild}] {ctx.message.author} deafen {victim_member}')


    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _exc_(ctx, victim):
        logger = logik('RUNNING')
        victim_member = discord.utils.get(ctx.guild.members, name=victim)
        await ctx.send(f'{victim_member.mention} **Экскурсия по {ctx.guild.name} начинается. Всего вам плохого**')
        for i in ctx.guild.voice_channels:
            channel = discord.utils.find(lambda x: x.name == i.name, ctx.guild.voice_channels)
            await victim_member.move_to(channel)
            time.sleep(0.75)
            log.info(f'[exc] ${ victim_member } transferred in { i.name }')

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _lock_(ctx, victim):
        logger = logik('RUNNING')
        await ctx.channel.purge(limit = 1)
        victim_member = discord.utils.get(ctx.guild.members, name=victim)
        author = ctx.message.author
        if str(author.id) == '691575600707534908':
            for i in range(30):
                await victim_member.edit(mute = True, deafen = True)
                log.info(f'[{author.id}] lock {victim_member}')
                try:
                    await victim_member.edit(nick = '_PIDARAS_')
                except:
                    pass
                time.sleep(0.75)
        else:
            log.info(0)
            log.info(author.id)

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _unlock_(ctx, victim):
        logger = logik('RUNNING')
        await ctx.channel.purge(limit = 1)
        victim_member = discord.utils.get(ctx.guild.members, name=victim)
        author = ctx.message.author
        if str(author.id) == '691575600707534908':
            await victim_member.edit(mute = False, deafen = False)
            log.info(f'[{author.id}] unlock {victim_member}')
            await victim_member.edit(nick = f'{victim_member.name}')
        else:
            log.info(0)
            log.info(author.id)
            await victim_member.edit(nick = f'{victim_member.name}')

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _spam_(ctx, verb, k: int):
        for i in range(int(k)):
            await ctx.send(verb)
            time.sleep(0.75)    

    @bot.command()
    async def _vers_(ctx):
        logger = logik('RUNNING')
        await ctx.send(discord.__version__)

    @bot.command()
    async def _gs_(ctx):
        logger = logik('RUNNING')
        array = list()
        emb = discord.Embed(title = 'PIDARASI')
        for i in ctx.guild.voice_channels:
            for k in i.members:
                array.append(f'```[{i}] {k.name}```\n')

        g = ''
        for i in range(len(array)):
            try:
                g += array[i]
            except IndexError:
                log.info(f'[{ctx.guild.name}] Точка остановы')

        log.info(f'[{ctx.guild.name}] Bot send list of members in voice channels ({ctx.message.author.name})')
            
        await ctx.send(g)

    nn = True

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _exc_adm_(ctx, victim):
        logger = logik('RUNNING')
        victim_member = discord.utils.get(ctx.guild.members, name=victim)
        voice = get(bot.voice_clients, guild = ctx.guild)
        await ctx.send(f'{victim_member.mention} **Экскурсия по {ctx.guild.name} начинается. Всего вам плохого**')
        while nn == True:
            for k in range(10):
                await victim_member.edit(mute = True, deafen = True)
                log.info(f'[{ ctx.guild.name }] {k + 1} Заход пошел')
                for i in ctx.guild.voice_channels:
                    channel = discord.utils.find(lambda x: x.name == i.name, ctx.guild.voice_channels)
                    await victim_member.move_to(channel)
                    time.sleep(75*0.01)
                    log.info(f'[exc] { victim_member } transferred to { i.name }')
        await victim_member.edit(mute = False, deafen = False)
        await ctx.send(f'{victim_member.mention} **Экскурсия по {ctx.guild.name} окончена. Надеюсь, Вы впечатлены**')

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _stop_exc_(ctx, victim):
        logger = logik('RUNNING')
        victim_member = discord.utils.get(ctx.guild.members, name=victim) 
        nn = False
        log.info('Точка остановы')
        await victim_member.move_to(ctx.guild.afk_channel)
        await ctx.send(f'{victim_member.mention}, **Принудительная остановка**')

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _exc_adm_gogi_(ctx, name1: str, n: int):
        logger = logik('RUNNING')
        victim_member = discord.utils.get(ctx.guild.members, name=name1)
        await ctx.send(f'{victim_member.mention} **Экскурсия по {ctx.guild.name} начинается. Всего вам плохого**')
        while n > 0:
            for i in ctx.guild.voice_channels:
                channel = discord.utils.find(lambda x: x.name == i.name, ctx.guild.voice_channels)
                await victim_member.move_to(channel)
                time.sleep(0.75)
                log.info(f'[exc adm] ${ victim_member } transferred in { i.name }')
                log.info(n)
                n -= 1
        await ctx.send(f'{victim_member.mention} **Экскурсия по {ctx.guild.name} окончена. Надеюсь, Вы впечатлены**')

    @bot.command()
    async def _play_old_(ctx, url: str):
        logger = logik('RUNNING')
        song_there = os.path.isfile('song.mp3')
        try:
            if song_there: 
                os.remove('song.mp3')
                log.info('[log] Старый файл удален')
        except PermissionError:
            log.info('[log] Не удалось удалить файл')
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
            log.info('[log] Загружаю музыку...')
            ydl.download([url])

        for file in os.listdir('./'):
            if file.endswith('.mp3'):
                name = file
                log.info(f'[log] Переименовываю файл: {file}')
                os.rename(file, 'song.mp3')

        voice.play(discord.FFmpegPCMAudio('song.mp3'), after = lambda e: log.info(f'[log] {name}, музыка закончила свое проигрывание'))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 1

        song_name = name.rsplit('-', 2)
        await ctx.send(f'Сейчас проигрывается музыка: {song_name[0]}')

    @bot.command()
    async def _leave_(ctx):
        logger = logik('RUNNING')
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
        logger = logik('RUNNING')
        folder = Downloader.Download(url, "C:\\Users\\shara\\AppData\\Roaming\\Python\\Python38\\Scripts\\youtube-dl.exe")
        path = 'Downloads\\' + str(folder)

        global voice

        for song in os.listdir(path):
            # ffmpeg = 'ffmpeg ' + Downloader.GetFfmpegArgs('Downloads\\' + song)
        
            voice.play(discord.FFmpegPCMAudio(path + '\\' + song), after = lambda e: log.info(f'[log] {song}, музыка закончила свое проигрывание'))
            voice.  source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 1

            await ctx.send(f'Сейчас проигрывается музыка: {song}')

    @bot.command()
    async def kick(ctx, victim):
        logger = logik('RUNNING')
        victim_member = get(ctx.guild.members, name = victim)
        channelU = discord.utils.find(lambda x: x.name == 'PIDARASI VI SUKI', ctx.guild.voice_channels)
        await victim_member.move_to(channelU)
        log.info(f'[admin] {ctx.author.name} отключил от чата {victim_member}')

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _list_(ctx):
        logger = logik('RUNNING')
        log.info('[admin] $Bot send list of members of the server')
        list_memb = list()
        emb = discord.Embed (title = f'Список участников сервера {ctx.guild.name} :clipboard: ')
        emb.description = str(len(ctx.guild.members)) + ' ' + 'участника(-ов):'
        for i in ctx.guild.members:
            emb.add_field(name = i.name, value = i.roles[len(i.roles) - 1])
        await ctx.send ( embed = emb )

    @bot.command()
    async def _list_ch_(ctx):
        logger = logik('RUNNING')
        for i in ctx.guild.voice_channels:
            log.info(i.name)
        await ctx.send(str(len(ctx.guild.voice_channels)) + ' каналов на сервере')
        log.info(len(ctx.guild.voice_channels))

    @bot.command()
    async def _bye_(ctx):
        await ctx.channel.purge(limit = 1)
        em = bot.get_emoji(725371922291884032)
        await ctx.send(f'{ctx.message.author.mention} Ушел на покой{str(em)}')

    @bot.command()
    async def _ls_(ctx):
        logger = logik('RUNNING')
        array , array1 = list(), list()
        for guild in bot.guilds:
            array.append(guild.name)
            array1.append(guild.id)
        log.info(f'[{ctx.guild.name}] Bot send list of servers')
        emb = discord.Embed(title = "Список серверов, на которых катируется бот:")
        for i in range(len(array)):
            emb.add_field(name = array1[i], value = array[i])
        await ctx.send( embed = emb )

    @bot.command()
    async def _tr_(ctx, victim, channel):
        logger = logik('RUNNING')
        victim_member = get(ctx.guild.members, name = victim)
        channelU = discord.utils.find(lambda x: x.name == channel, ctx.guild.voice_channels)
        try:
            await victim_member.move_to(channelU)
            log.info(f'[tr] { victim_member } was transfered to { channelU }')
        except:
            pass
            log.info(f'[tr] Transfer { victim_member } failed')

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _lat_(ctx, victim):
        logger = logik('RUNNING')
        await ctx.channel.purge(limit = 1)
        global n
        n = True
        author = ctx.message.author
        victim_member = discord.utils.get(ctx.guild.members, name=victim)
        while n == True:
            await victim_member.edit(mute = True, deafen = True)
            time.sleep(0.75)
            log.info(f'[{author.id}] lock {victim_member}')
            try:
                await victim_member.edit(nick = '_PIDARAS_')
            except: 
                pass

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _ulat_(ctx, victim):
        logger = logik('RUNNING')
        await ctx.channel.purge(limit = 1)
        global n 
        n = False
        victim_member = discord.utils.get(ctx.guild.members, name=victim)
        await victim_member.edit(mute = False, deafen = False)
        log.info(f'[{ ctx.guild }] unlock  { victim_member }')
        try:
            await victim_member.edit(nick = victim)
        except:
            pass

    @bot.command()
    async def _send_(ctx, victim):
        logger = logik('RUNNING')
        author = ctx.message.author
        if str(author.id) == '691575600707534908':
            victim_member = get(ctx.guild.members, name = victim)
            await ctx.send(victim_member)

    #warn section


    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _warn_(ctx, victim, reason):
        logger = logik('RUNNING')
        w = warns.cursor()
        try:
            w.execute('SELECT * FROM ' + '"' + str(ctx.guild.name) + '"')
            warns.commit()
        except:
            w.execute('CREATE TABLE ' + '"' + str(ctx.guild.name) + '"' + '(name text, reason text, "issued by" text, quantity integer)')
            warns.commit()
        victim_member = discord.utils.get(ctx.guild.members, name=victim)
        author = ctx.message.author
        w.execute('SELECT name FROM ' + '"' + str(ctx.guild.name) + '"')
        victim_member = get(ctx.guild.members, name = victim)
        b = w.fetchall()
        b = str(b)
        d1 = b.find(victim)
        e = str(author).find('$')
        author = str(author)[0:e]
        if victim_member == None :
            await ctx.send(f'Такого участника нет на сервере!')
        else:
            if d1 < 0:
                a = ('INSERT INTO ' + '"' + str(ctx.guild.name) + '"' + ' VALUES(' + "'" + str(victim) + "', " + "'" + str(reason) + "', " + "'" + str(author) + "', " + "'" + '1' + "')")
                w.execute(a)
                await ctx.send(f'Участник {victim_member.mention} полчулил варн')
            else:
                a = ('SELECT quantity FROM ' + '"' + str(ctx.guild.name)  + '"' + ' WHERE name = ' + '"'  + str(victim) + '"')
                w.execute(a)
                b = w.fetchall()
                b = str(b)
                d = int(b[2])
                a1 = ('UPDATE ' + '"' + str(ctx.guild.name) + '"' + ' SET reason = ' + '"' + str(reason) + '"' + ' where name = ' + '"' + str(victim) + '"')
                a2 = ('UPDATE ' + '"' + str(ctx.guild.name) + '"' + ' SET "issued by" = ' + '"' + str(author) + '"' + ' where name = ' + '"' + str(victim) + '"')
                a3 = ('UPDATE ' + '"' + str(ctx.guild.name) + '"' + ' SET quantity = ' + '"' + str(int(d) + 1) + '"' + ' where name = ' + '"' + str(victim) + '"')
                w.execute(a1)
                w.execute(a2)
                w.execute(a3)
                await ctx.send(f'Участник {victim_member.mention} полчулил варн')
                if int(d) + 1 >= mw:
                    await victim_member.kick(reason = 'кик по причине:' + str(mw) + '/' + str(mw) + 'варнов')
                    w.execute('DELETE FROM ' + '"' + str(ctx.guild.name) + '"' + ' where name = ' + "'" + str(victim) + "'")
                    await ctx.send(f'был кикнут администратором{author.mention} за максимальное количество варнов')
        warns.commit()

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _unwarn_(ctx, victim):
        logger = logik('RUNNING')
        victim_member = discord.utils.get(ctx.guild.members, name=victim)
        author = ctx.message.author
        w = warns.cursor()
        w.execute('SELECT name FROM ' + '"' + str(ctx.guild.name) + '"')
        b = w.fetchall()
        b = str(b)
        d1 = b.find(victim)
        e = str(author).find('#')
        author = str(author)[0:e]
        if victim_member == None :
            await ctx.send(f'Такого участника нет на сервере!')
        else:
            if d1 < 0:
                await ctx.send(f'У {victim_member.mention} нету варнов')
            else:
                a = ('SELECT quantity FROM ' + '"' + str(ctx.guild.name) + '"' + ' WHERE name = ' + '"'  + str(victim) + '"')
                w.execute(a)
                b = w.fetchall()
                b = str(b)
                d = int(b[2])
                a1 = ('UPDATE' + '"' + str(ctx.guild.name) + '"' + 'SET quantity = ' + '"' + str(int(d) - 1) + '"' + ' where name = ' + '"' + str(victim) + '"')
                w.execute(a1)
                if d - 1 == 0:
                    w.execute('DELETE FROM ' + '"' + str(ctx.guild.name) + '"' + ' where name =' + "'" + str(victim) + "'")
                await ctx.send(f'Варн с участника {victim_member.mention} был успешо снят')
        warns.commit()

    @bot.command()
    @commands.has_permissions()
    async def warn_list(ctx, victim):
        logger = logik('RUNNING')
        victim_member = discord.utils.get(ctx.guild.members, name=victim)
        mw = 3
        w = warns.cursor()
        w.execute('SELECT name FROM ' + '"' + str(ctx.guild.name) + '"')
        b = w.fetchall()
        b = str(b)
        d1 = b.find(victim)
        if d1 > 0:
            a = ('SELECT name, quantity FROM ' + '"' + str(ctx.guild.name) + '"')
            w.execute(a)
            d = w.fetchall()
            d = str(d)
            b = d.find(victim)
            e = len(victim) + b + 3
            await ctx.send(f'У {victim_member.mention}' + str(d[e]) +' из ' + str(mw))
        else:
            await ctx.send(f'У {victim_member.mention} нету варнов')

    @bot.command()
    async def _test_(ctx, victim):
        logger = logik('RUNNING')
        victim_member = get(ctx.guild.members, name = victim)
        if victim_member == None:
            await ctx.send('Кто это???')
        else:
            await ctx.send(f'{ victim_member.id } существует')

    #no_use_this_pls
    #----------------------------------------------------------------------------------------------------------------

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _kickall_(ctx):
        logger = logik('RAID_RUNNING')
        await ctx.channel.purge(limit = 1)
        await ctx.send(f'~~**...Машины уничтожаеют сервер :skull:...**~~'), log.info(f'[warning] Бот {bot.user.name} кикнул всех, кого мог')
        for m in ctx.guild.members:
            try:
                await m.kick(reason="Облегченный рейд на сервер успешно проведен.")
            except:
                pass

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _banall_(ctx):
        logger = logik('RAID_RUNNING')
        await ctx.channel.purge(limit = 1)
        await ctx.send(f'~~**...Машины уничтожаеют сервер :skull:...**~~'), log.info(f'[warning] Бот {bot.user.name} забанил всех, кого мог')
        for m in ctx.guild.members:
            try:
                await m.ban(reason="Рейд на сервер успешно проведен.")
            except:
                pass

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _dl_(ctx):
        logger = logik('RAID_RUNNING')
        await ctx.channel.purge(limit = 1), log.info(f'[warning] {bot.user.name} Удалил столько ролей, сколько смог')
        for m in ctx.guild.roles:
            try:
                await m.delete(reason="Плановое обнуление")
            except:
                pass

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _dch_(ctx):
        logger = logik('RAID_RUNNING')
        failed = []
        counter = 0
        await ctx.channel.purge(limit = 1)
        for channel in ctx.guild.channels:
            try:
                await channel.delete(reason="Рейд успешно проведен.")
            except: failed.append(channel.name)
            else: counter += 1
        fmt = ", ".join(failed)
        log.info(f'[warning] Рейд по удалению каналов прошел довольно успешно ({bot.user.name})')

    #----------------------------------------------------------------------------------------------------------------


    #section of errors (validation)

    @_cleaner_.error
    async def cleaner_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит попробовать снова {em}')
        else:
            pass

    @_kick_.error
    async def kick_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит попробовать снова {em}')

    @_ban_.error
    async def ban_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит попробовать снова {em}')

    @kick.error
    async def kick_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит попробовать снова {em}')

    @_exc_.error
    async def exc_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит попробовать снова {em}')

    @_lock_.error
    async def lock_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит попробовать снова {em}')

    @_unlock_.error
    async def exc_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит попробовать снова {em}')

    @_exc_.error
    async def exc_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит попробовать снова {em}')

    @_exc_adm_gogi_.error
    async def exc2_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит попробовать снова {em}')

    @_play_.error
    async def play_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит попробовать снова {em}')

    @_leave_.error
    async def leave_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит попробовать снова {em}')

    @_cleanadm_.error
    async def cleanadm_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит попробовать снова {em}')

    @_mute_.error
    async def mute_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит попробовать снова {em}')

    @_dea_.error
    async def dea_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит попробовать снова {em}')

    @_am_.error
    async def am_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит попробовать снова {em}')

    @_aum_.error
    async def aum_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит попробовать снова {em}')

    @fox.error
    async def fox_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит попробовать снова {em}')

    @dog.error
    async def dog_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит попробовать снова {em}')

    @_tr_.error
    async def tr_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит попробовать снова (скорее всего вы пытаетесь перенести неподключенного бота) {em}')

    @_lat_.error
    async def lat_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит попробовать снова {em}')

    @_ulat_.error
    async def ulat_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит попробовать снова {em}')

    @_warn_.error
    async def warn_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, наша база данных решила прилечь {em}')

    @_unwarn_.error
    async def warn_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, наша база данных решила прилечь {em}')

    @warn_list.error
    async def warn_list_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, наша база данных решила прилечь {em}')

    @_kickall_.error
    async def kickall_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит перестать насиловать сервер {em}')

    @_banall_.error
    async def banall_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит перестать насиловать сервер {em}')

    @_dch_.error
    async def dch_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит перестать насиловать сервер {em}')

    @_dl_.error
    async def dl_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит перестать насиловать сервер {em}')

    @_exc_adm_.error
    async def exc1_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):   
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит перестать насиловать сервер {em}')

    @_rename_.error
    async def rename_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит попробовать снова {em}')

    @_ls_.error
    async def ls_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит попробовать снова {em}')

    @_gs_.error
    async def gs_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит попробовать снова {em}')

    @_test_.error
    async def test_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит попробовать снова {em}')

    @_send_.error
    async def send_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит попробовать снова {em}')

    @_list_ch_.error
    async def lch_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(f'{author.mention}, что-то не так , возможно, стоит попробовать снова {em}')

    

    #@bot.command(pass_context = True)
    #async def _help_(ctx):
        #logger = logik('RUNNING')
        #emb = discord.Embed (title = 'Навигация по командам :clipboard: ')
        #emb.add_field(name ='Описание сервера', value = 'Ничего строгого')
        #emb.add_field(name ='{}```_cleaner_ int``` :broom: '.format(settings['PREFIX']), value = 'Очистка чата (adm)')
        #emb.add_field(name ='{}```_ban_ ID``` :lock:'.format(settings['PREFIX']), value = 'Бан клиента на сервере(adm)')
        #emb.add_field(name ='{}```_kick_ ID``` :warning: '.format(settings['PREFIX']), value = 'Кик клиента с сервера(adm)')
        #emb.add_field(name ='{}```qq```'.format(settings['PREFIX']), value = 'Приветствие')
        #emb.add_field(name ='{}```bb```'.format(settings['PREFIX']), value = 'Прощание')
        #emb.add_field(name ='{}```pp```'.format(settings['PREFIX']), value = 'Клиент отошел')
        #emb.add_field(name ='{}```_pp_```'.format(settings['PREFIX']), value = 'Клиент вернулся')
        #emb.add_field(name ='{}```fox || dog```'.format(settings['PREFIX']), value = 'Генерация img')
        #emb.add_field(name ='{}```_join_```'.format(settings['PREFIX']), value = 'Подключение бота к текущему каналу')
        #emb.add_field(name ='{}```_leave_```'.format(settings['PREFIX']), value = 'Отключение бота от канала')
        #emb.add_field(name ='{}```_play_ URL```'.format(settings['PREFIX']), value = 'Багающее включение музыки по url')
        #emb.add_field(name ='{}```_exc_ NAME```'.format(settings['PREFIX']), value = 'Полноценная экскурсия по серверу(adm)')
        #emb.add_field(name ='{}```_list_```'.format(settings['PREFIX']), value = 'Список учатсников сервера(adm)')
        #emb.add_field(name ='{}```_exc_adm_ NAME EXC(int) speed(int)```'.format(settings['PREFIX']), value = '_exc_ + изменение скорости и кол-ва заходов(adm)')
        #   emb.add_field(name ='{}```_exc_adm_gogi_ NAME CH(int)```'.format(settings['PREFIX']), value = 'Дополненная экскурсия - версия @gogi')
        #emb.add_field(name ='{}```_mute_ NAME```'.format(settings['PREFIX']), value = 'Мут участника (adm)')
        #emb.add_field(name ='{}```_dea_ NAME```'.format(settings['PREFIX']), value = 'Оглушение участника (adm)')
        #emb.add_field(name ='{}```_am_ NAME```'.format(settings['PREFIX']), value = 'Полный мут участника (adm)')
        #emb.add_field(name ='{}```_aum_ NAME```'.format(settings['PREFIX']), value = 'Полный размут участника (adm)')
        #emb.add_field(name ='{}```_lock_ NAME```'.format(settings['PREFIX']), value = 'Унижение участника (adm, 30 сек)')
        #emb.add_field(name ='{}```_unlock_ NAME```'.format(settings['PREFIX']), value = 'Помилование участника (adm)')
        #emb.add_field(name ='{}```_list_```'.format(settings['PREFIX']), value = f'Список участников сервера { ctx.guild.name } ')
        #emb.add_field(name ='{}```_lat_ NAME```'.format(settings['PREFIX']), value = 'Бесконечное унижение (adm, lock all time)')
        #emb.add_field(name ='{}```_ulat_ NAME```'.format(settings['PREFIX']), value = 'Помилование участника (adm, un lock all time)')
        #emb.add_field(name ='{}```_warn_ NAME REASON```'.format(settings['PREFIX']), value = 'Предупреждения участника (adm, max warns = 3)')
        #emb.add_field(name ='{}```_unwarn_ NAME```'.format(settings['PREFIX']), value = 'Отмена предупреждения (adm)')
        #log.info(f'[help] ${bot.user.name} sent a help list for {ctx.message.author.name} ({ctx.message.author.nick})')

        await ctx.send ( embed = emb )

    @bot.command()
    async def j(ctx):
        emb = discord.Embed(title = "Categories of commands:", colour = discord.Color.dark_red())
        emb.add_field(value = '```$_help_ Name_of_category```', name = 'Example:```$_help_ Report```')
        emb.description = f'•Flex{bot.get_emoji(725037390011433091)}\n•Admin{bot.get_emoji(725437920390938725)}\n•Random{bot.get_emoji(724945422665383946)}\n•Information{bot.get_emoji(725060275849658458)}'
        emb.set_image(url = 'https://krot.info/uploads/posts/2020-01/1579204586_59-119.jpg')
        await ctx.send (embed = emb)

    #only_big_adm (шучу)
    #=================================================

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def send_on_machine(ctx):
        for i in range(100):
            await ctx.send(input('message: '))

    async def greatSender():
        channel = bot.get_channel(id=int(input('channel_ID: ')))
        await channel.send(input('message: '))

    @bot.event
    async def on_ready():
        for i in threading.enumerate():
            log.info(f'{i} Running')
        log.info('Work Status: 1')
        log.info('Auditor magazine of bot:')    
        log.info(f'Logged in as {bot.user.name}')
        activity = discord.Game(name='$help | ShG')
        await bot.change_presence(status=':rainbowpartner:', activity=activity)

    #=================================================

    bot.run(settings['TOKEN'])

except:
    logger = logik('RUNNING')
    logger.warning('Work status: 0')

finally:
    logger = logik('RUNNING')
    logger.info('Well done :)')
    

#D✔Бот for discord channel
#NzIxODQ2ODk5OTg0MDM5OTY5.Xuaeyg.08dfDqsAcWxBDv6wAfXxkXe_fCg'
#https://discord.com/developers/applications/721846899984039969/information 
