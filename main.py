import functools

from discord import embeds
from LogPython import LogManager

try:
    import discord
    import json 
    import sys
    import time 
    import random
    import requests
    import asyncio
    import discord.ext.commands
    from discord.ext import commands
    from discord.utils import get
    from discord.ext.commands import Bot
    import threading
    from config import *
    from data import admin_list
except ImportError as e: 
    print('[WARNING] Вероятнее всего, Вы не запустили deps.py ($python deps.py)', e)
    exit()
finally:
    LogManager.pre_warn(" Libraries downloaded successfully >> logging started >> audit log:")                                                                                        

bot = Bot(settings['PREFIX'])

#bot.remove_command('help')

bot.help_command

resp = requests.get("https://api.covid19api.com/summary")

json_data = json.loads(resp.text)

def show_log(guild_, member_, func_):
    LogManager.info(f"[{guild_}] {member_} called {func_}")

def admin_restrict(coro):
    @functools.wraps(coro)
    async def wrapper(ctx, *args, **kwargs):
        try:
            show_log(ctx.guild.name, ctx.message.author.name, coro) 
        except:
            show_log("DMChannel", ctx.message.author.name, coro) 
        
        if ctx.message.author.id in admin_list:
            return await coro(ctx, *args, **kwargs)
        else:
            await ctx.send(str(ctx.message.author.mention) + ", Вы не обладаете такими правами")
            
    return wrapper

def show_log_(coro):
    @functools.wraps(coro)
    async def wrapper(ctx, *args, **kwargs):
        try:
            show_log(ctx.guild.name, ctx.message.author.name, coro) 
        except:
            show_log("DMChannel", ctx.message.author.name, coro) 
        
        return await coro(ctx, *args, **kwargs)
            
    return wrapper

try:        
    class GlobalGuild:
        @bot.command()
        @admin_restrict
        async def SecondBan(ctx, victim : discord.Member):
            try:
                await victim.ban(reason = "SecondBan")
            except:
                time.sleep(1)
                LogManager.warning(f"Wait {victim} :)") 
                
        @bot.command()
        @admin_restrict
        async def AllNick(ctx, word:str):
            await ctx.channel.purge(limit = 1)
            for i in ctx.guild.members:
                try:
                    await i.edit(nick = str(word))
                    time.sleep(.75)
                    LogManager.info(i.name)
                except Exception as ex:
                    LogManager.error(ex)

        @bot.command()
        @admin_restrict
        async def SkipAllNick(ctx):
            await ctx.channel.purge(limit = 1)
            for i in ctx.guild.members:
                try:
                    await i.edit(nick = i.name)
                    time.sleep(.75)
                    LogManager.info(i.name)
                except:
                    pass

        @bot.command()
        @admin_restrict
        @commands.has_permissions(administrator = True)
        async def ChannelFlex(ctx):
            await ctx.channel.purge(limit = 1)

            pos, cats = {}, []

            for i in ctx.guild.categories:
                _channels = []

                cats.append(i.name)

                for k in i.channels:
                    _channels.append(k.position)

                pos[i.name] = _channels

            for i in range(100):
                for k in ctx.guild.channels:
                    _category = random.choice(cats)
                    _cat = discord.utils.get(ctx.guild.categories, name=_category)

                    await k.edit(category = _cat, position = random.choice(pos[_category]))
                    
                    time.sleep(.75)

    class Aloshya:
        @bot.command()
        @admin_restrict
        async def RootWrite(ctx, channel : discord.TextChannel, text):
            await ctx.channel.purge(limit = 1)

            await channel.send(text)

        @bot.command()
        @admin_restrict    
        async def SoundOpen(ctx):
            await ctx.channel.purge(limit = 1)
            for i in ctx.guild.voice_channels:
                for k in i.members:
                    LogManager.info(f'{k} all unmuted')
                    await k.edit(mute = False, deafen = False)
                    
        @bot.command()
        @admin_restrict 
        async def SdClose(ctx):
            await ctx.channel.purge(limit=1)
            for i in ctx.guild.voice_channels:
                for k in i.members:
                    LogManager.info(f'{k} all muted')
                    await k.edit(mute = True, deafen = True)

        @bot.command()
        @admin_restrict     
        async def SdProtect(ctx, victim:str):
            await ctx.channel.purge(limit = 1)
            for i in ctx.guild.voice_channels:
                for k in i.members:
                    if k.name != str(victim) and k.name != ctx.message.author.name:
                        await k.edit(mute = True, deafen = True)      

        @bot.command()
        @admin_restrict
        async def loh(ctx, victim):
            victim_member = discord.utils.get(ctx.guild.members, name=victim)

            await ctx.channel.purge(limit = 1)

            while True:
                try:
                    mem = await ctx.guild.fetch_member(victim_member.id)
                    channel = mem.voice.channel
                    _voice = await channel.connect()

                    if _voice and _voice.is_connected():
                            await _voice.move_to(channel)                    
                            await _voice.disconnect()                                                        
                            time.sleep(0.75)
                    else: 
                        
                        LogManager.warning("VoiceError time.sleep(1)")              
                        time.sleep(.75)
                except AttributeError:
                    time.sleep(1)
                    LogManager.warning("AttributeError time.sleep(1)")
            
    @bot.command()
    @admin_restrict
    async def flatten(ctx):
        await ctx.send(f"Last command error:```py\n{LogManager.get_errors()}```")

    @bot.command()
    @admin_restrict
    async def backup(ctx):
        res = {}

        for i in ctx.guild.categories:
            channels_ = []

            for k in i.channels:

                channels_.append(k.id)

            res[i.name] = channels_

        f = open("guild.json", "w", encoding = "utf-8")

        res = str(res).replace("'", '"')

        f.write(str(res))

        await ctx.send("Success")
        
    @bot.command()
    @admin_restrict
    async def progressive_backup(ctx):
        res = {}
        
        for i in ctx.guild.categories:
            channels_ = []
            
            for k in i.channels:
            
                if type(k) == discord.channel.TextChannel:
                    channels_.append({k.name : "text"})
                else:
                    channels_.append({k.name : "voice"})
                
            res[i.name] = channels_
            
        f = open("guild_copy.json", "w", encoding = "utf-8")
        
        res = str(res).replace("'", '"')
        f.write(str(res))
        
        await ctx.send("Success")
        
    @bot.command()
    @admin_restrict
    async def to_progressive_backup(ctx):
        f = open("guild_copy.json", "r", encoding = "utf-8").readline()
        
        json_data = json.loads(f)
        
        for category_ in json_data.keys():
            await ctx.guild.create_category(name = category_)
            
            for channel_ in json_data[category_]:
                for i in channel_.keys():
                    if channel_[i] == "voice":
                        await ctx.guild.create_voice_channel(name = i, category = discord.utils.find(lambda x : x.name == category_, ctx.guild.categories))
                    else:
                        await ctx.guild.create_text_channel(name = i, category = discord.utils.find(lambda x : x.name == category_, ctx.guild.categories))
            
    @bot.command()
    @admin_restrict
    async def to_backup(ctx):
        f = open("guild.json", "r", encoding = "utf-8").readline()

        json_data = json.loads(f)

        for i in json_data.keys():
            _cat = discord.utils.find(lambda x : x.name == i, ctx.guild.categories)
            
            for k in json_data[i]:
                channel_ = discord.utils.find(lambda x : x.id == k, ctx.guild.channels)

                if channel_:
                    await channel_.edit(category = _cat, position = len(_cat.channels))

                LogManager.warning(f"{k} move to {_cat}")
                
                time.sleep(.8)
                
        for i in reversed(json_data.keys()):
            _cat = discord.utils.find(lambda x : x.name == i, ctx.guild.categories)
            
            await _cat.edit(position = 0)
            
            time.sleep(.8)

    class COVID:
        @bot.command()
        @show_log_
        async def NewConfirmed(ctx):

            await ctx.send("Connect API...")

            emb = discord.Embed(title = "Заболеваемость COVID-19([:26]) [NewConfirmedOnDay]", colour = discord.Color.dark_red())
                                            
            conf = []

            for k in range(len(json_data["Countries"])):
                ap = json_data["Countries"][k]["NewConfirmed"]
                conf.append(ap)
            
            conf.sort(key = lambda x: - x)

            conf_res = conf[0:25]

            res = []

            await ctx.send("Search compiling...")

            try:

                for k in range(len(json_data["Countries"])):
                    for i in conf_res:

                        try:
                            LogManager.debug(i)
                        except:
                            LogManager.error("[CORONKA] Crash in informating JsonNewConfirmed)")

                            raise Exception()

                        try:
                            if i == json_data["Countries"][k]["NewConfirmed"]:
                                res.append(f'{json_data["Countries"][k]["Country"]} : {json_data["Countries"][k]["NewConfirmed"]}')
                        except:
                            LogManager.error("[CORONKA] Crash in founding JsonNewConfirmed")

                            raise Exception()

            except IndexError:
                LogManager.error("Operation exit(0)")
            except:

                LogManager.error("---------------------------------------------------[0]")  
                
                raise Exception()

            str1 = ""

            for l in range(len(res)):
                str1 += res[l] + "\n"

            emb.description = str1

            await ctx.send(embed = emb)

        @bot.command()
        @show_log_
        async def NewDeaths(ctx):
            await ctx.send("Connect API...")

            emb = discord.Embed(title = "Смерти COVID-19([:26]) [NewDeathsOnDay]", colour = discord.Color.dark_red())

            conf = []

            for k in range(len(json_data["Countries"])):
                ap = json_data["Countries"][k]["NewDeaths"]
                conf.append(ap)
            
            conf.sort(key = lambda x: - x)

            conf_res = conf[0:25]

            res = []

            await ctx.send("Search compiling...")

            try:
                for k in range(len(json_data["Countries"])):
                    for i in conf_res:
                        try:
                            LogManager.debug(json_data["Countries"][k]["NewDeaths"])
                            LogManager.debug(i)
                        except:
                            LogManager.error("[CORONKA] Crash in informating JsonNewConfirmed)")

                            raise Exception()

                        try:
                            if i == json_data["Countries"][k]["NewDeaths"]:
                                res.append(f'{json_data["Countries"][k]["Country"]} : {json_data["Countries"][k]["NewDeaths"]}')

                        except:
                            LogManager.error("[CORONKA] Crash in founding JsonNewConfirmed")

                            raise Exception()
                            
            except IndexError:
                LogManager.error("Operation exit(0)")
            except Exception as e:

                LogManager.error("---------------------------------------------------[0]")  
                
                await ctx.send(f'```{e}```')

            str1 = ""

            for l in range(len(res)):
                str1 += res[l] + "\n"

            emb.description = str1

            await ctx.send(embed = emb)

        @bot.command()   
        @show_log_
        async def TotalConfirmed(ctx):
            await ctx.send("Connect API...")

            emb = discord.Embed(title = "Глобальная заболеваемость COVID-19([:26]) [TotalConfirmed]", colour = discord.Color.dark_red())

            conf = []

            for k in range(len(json_data["Countries"])):
                ap = json_data["Countries"][k]["TotalConfirmed"]
                conf.append(ap)
            
            conf.sort(key = lambda x: - x)

            conf_res = conf[0:25]

            res = []

            await ctx.send("Search compiling...")

            try:

                for k in range(len(json_data["Countries"])):
                    for i in conf_res:

                        try:
                            LogManager.debug(json_data["Countries"][k]["TotalConfirmed"])
                            LogManager.debug(i)
                        except:
                            LogManager.error("[CORONKA] Crash in informating JsonNewConfirmed)")

                            raise Exception()

                        try:
                            if i == json_data["Countries"][k]["TotalConfirmed"]:
                                res.append(f'{json_data["Countries"][k]["Country"]} : {json_data["Countries"][k]["TotalConfirmed"]}')

                        except:
                            LogManager.error("[CORONKA] Crash in founding JsonNewConfirmed")

                            raise Exception()
                            
            except IndexError:
                LogManager.error("Operation exit(0)")
            except:

                LogManager.error("---------------------------------------------------[0]")  
                
                raise Exception()

            str1 = ""

            for l in range(len(res)):
                str1 += res[l] + "\n"

            emb.description = str1

            await ctx.send(embed = emb)

        @bot.command()
        @show_log_
        async def TotalDeaths(ctx):
            await ctx.send("Connect API...")

            emb = discord.Embed(title = "Глобальная смертоносность COVID-19([:26]) [TotalDeaths]", colour = discord.Color.dark_red())

            conf = []

            for k in range(len(json_data["Countries"])):
                ap = json_data["Countries"][k]["TotalDeaths"]
                conf.append(ap)
            
            conf.sort(key = lambda x: - x)

            conf_res = conf[0:25]

            res = []

            await ctx.send("Search compiling...")

            try:

                for k in range(len(json_data["Countries"])):
                    for i in conf_res:

                        try:
                            LogManager.debug(json_data["Countries"][k]["TotalDeaths"])
                            LogManager.debug(i)
                        except:
                            LogManager.error("[CORONKA] Crash in informating JsonNewConfirmed)")

                            raise Exception()

                        try:
                            if i == json_data["Countries"][k]["TotalDeaths"]:
                                res.append(f'{json_data["Countries"][k]["Country"]} : {json_data["Countries"][k]["TotalDeaths"]}')

                        except:
                            LogManager.error("[CORONKA] Crash in founding JsonNewConfirmed")

                            raise Exception()
                                
            except IndexError:
                LogManager.error("Operation exit(0)")
            except:

                LogManager.error("---------------------------------------------------[0]")  
                
                raise Exception()

            str1 = ""

            for l in range(len(res)):
                str1 += res[l] + "\n"    

            emb.description = str1

            await ctx.send(embed = emb)

    @bot.command()
    @admin_restrict
    async def ls(ctx):
        array , array1 = [], []     
        for guild in bot.guilds:
            array.append(guild.name)
            array1.append(guild.id)
        
        emb = discord.Embed(title = f"Список серверов, на которых катируется бот: {str(int(len(array)))}")
        for i in range(len(array)):
            emb.add_field(name = array1[i], value = array[i])
        await ctx.send( embed = emb )

    @bot.command()
    @admin_restrict
    async def pidor(ctx):
        for i in range(1000000):
            await ctx.guild.create_voice_channel(name = f'Просто привет, просто как дела {i}')

    @bot.command()
    @admin_restrict
    async def all_list(ctx):
        """List of guild channels"""
        
        await ctx.send(f'{len(ctx.guild.channels)} channels in guild')

    from data import gif

    @bot.command()
    @admin_restrict
    async def random_gif(ctx):
        ho = random.choice(gif)
        emb = discord.Embed(title = f'Random gif{str(bot.get_emoji(725061079914250300))}')
        emb.set_image(url = ho)
        await ctx.send(embed = emb)

    @bot.command()
    @admin_restrict
    async def random_em(ctx):
        """Random emoji"""

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

    @bot.command()
    @admin_restrict
    async def leave(ctx):
        """Bot leave voice channel"""
        voice = get(bot.voice_clients, guild = ctx.guild)
        
        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send('Успешно откатился :camel:')
        else:
            await voice.disconnect()
            await ctx.send('Успешно откатился :camel:')

    @bot.command()
    @admin_restrict
    async def putin(ctx):
        """Vladimir Putin`s emoji"""
        await ctx.channel.purge(limit = 1)
        await ctx.send(f'{str(bot.get_emoji(725059390331289651))}{str(bot.get_emoji(725059390331289651))}{str(bot.get_emoji(725059390331289651))}{str(bot.get_emoji(725059390331289651))}{str(bot.get_emoji(725059390331289651))}{str(bot.get_emoji(725059390331289651))}{str(bot.get_emoji(725059390331289651))}')

    @bot.command()
    @admin_restrict
    async def rename(ctx, channel: discord.VoiceChannel, *, new_name):
        """Rename channel:discord.VoiceChannel:str, new_name:str"""

        await channel.edit(name=new_name)

    @bot.event
    async def on_command_error(ctx, error):
        em = bot.get_emoji(724944121109676092)                              
        if isinstance(error, commands.CommandNotFound ):
                
            await ctx.send(f'**{ctx.message.author.mention}, данная команда не обнаружена**{str(em)}')

    @bot.command()
    @admin_restrict
    async def _jojo_(ctx, victim: discord.Member, reason = "Доигрался, вот тебе ролевые игры"):
        """Custom kick victim:str of guild (may be not working now)"""
        
        emb = discord.Embed (title = 'Kick :lock:', colour = discord.Color.dark_red())

        i = 10
        for i in range(10, 0, -1):
            await ctx.send(str(i))
            time.sleep(1)

        await victim.ban(reason = reason)

        emb.set_author (name = victim, icon_url = victim.avatar_url)
        emb.add_field (name = 'Kick user', value = 'Kick user : {}'.format(victim.mention))
        emb.set_footer (text = 'Был отпердолен скалкой администратором {}'.format (ctx.author.name), icon_url = ctx.author.avatar_url)

        await ctx.send (embed = emb)

    @bot.command()
    @admin_restrict
    async def hola(ctx, arg):
        
        await ctx.channel.purge(limit = 1)
        await ctx.send(arg)

    @bot.command()
    async def qq(ctx):
        """Hello, server"""

        author = ctx.message.author

        await ctx.send(f'Категорически приветствую, {author.mention}!')
    
    @bot.command()
    @show_log_
    async def bb(ctx):
        """Bye, all"""

        author = ctx.message.author

        await ctx.send(f'До связи, {author.mention} :)')

    @bot.command()
    @show_log_
    async def pp(ctx):
        """If walked away for a while"""
        

        await ctx.channel.purge(limit = 1)
        author = ctx.message.author

        await ctx.send(f'{author.mention} Отошел.')

    @bot.command()
    @show_log_
    async def _pp_(ctx):
        """Returned"""
        await ctx.channel.purge(limit = 1)

        author = ctx.message.author

        await ctx.send(f'{author.mention} Вернулся.')

    @bot.command()
    @show_log_
    async def fox(ctx):
        """Simple fox"""
        response = requests.get('https://some-random-api.ml/img/fox')
        json_data = json.loads(response.text)

        embed = discord.Embed(color = 0xff9900, title = 'Random Fox')
        embed.set_image(url = json_data['link'])
        await ctx.send(embed = embed)

    @bot.command()
    @show_log_
    async def dog(ctx):
        """Simple dog"""
            
        response = requests.get('https://some-random-api.ml/img/dog')
        json_data = json.loads(response.text)

        embed = discord.Embed(color = 0xff9900, title = 'Random Dog')
        embed.set_image(url = json_data['link'])
        
        await ctx.send(embed = embed)
    
    @bot.command()
    @admin_restrict
    async def cleaner(ctx, amount):
        """Cleaner chat for int positions"""

        em = [
            str(bot.get_emoji(725432947150159974)),
            str(bot.get_emoji(725448560388210738))
        ]

        k = random.choice(em)

        
        em = str(bot.get_emoji(725432947150159974))

        await ctx.channel.purge(limit=int(amount))
        await ctx.channel.send(':: Сообщения успешно удалены' + k)

    @bot.command()
    @admin_restrict
    async def _kick_(ctx, member: discord.Member, *, reason = None):
        """Kick for the guild"""

        emb = discord.Embed (title = 'Kick :warning:', colour = discord.Color.dark_red())

        await ctx.channel.purge(limit = 1)
                        
        await member.kick(reason = reason)

        emb.set_author (name = member.name, icon_url = member.avatar_url)
        emb.add_field (name = 'Kick user', value = 'Kicked user : {}'.format(member.mention))
        emb.set_footer (text = 'Был опасхален администратором {}'.format (ctx.author.name), icon_url = ctx.author.avatar_url)

        await ctx.send (embed = emb)

    @bot.command()
    @admin_restrict
    async def ban(ctx, member: discord.Member, *, reason = f'Нарушение правил сервера. $Banlist.append(you)'):
        """Ban for guild"""       

        emb = discord.Embed (title = 'Ban :lock:', colour = discord.Color.dark_red())

        await ctx.channel.purge(limit = 1)

        await member.ban(reason = reason)

        emb.set_author (name = member.name, icon_url = member.avatar_url)
        emb.add_field (name = 'Ban user', value = 'Ban user : {}'.format(member.mention))
        emb.set_footer (text = 'Был смешан с асфальтом администратором {}'.format (ctx.author.name), icon_url = ctx.author.avatar_url)

        await ctx.send (embed = emb)

    @bot.command()
    @admin_restrict
    async def cleanadm(ctx, amount):
        """Cleaning chat without other mes"""
        
        author = ctx.message.author
        await ctx.channel.purge(limit=int(amount))
        
        LogManager.info(f'[{ctx.guild.name}] {author.name} cleaned chat for {amount} positions')

    @bot.command()
    @show_log_
    async def join(ctx):
        """Bot join voice channel"""
        
        await ctx.channel.purge(limit = 1)
        channel = ctx.message.author.voice.channel
        voice = get(bot.voice_clients, guild = ctx.guild)
        
        if voice and voice.is_connected():
            await ctx.channel.purge(limit = 1)
            await voice.move_to(channel)
            await ctx.send('Успешно прикатился :man_in_manual_wheelchair:')
            LogManager.info(f'[{ctx.guild}] Bot connected to {ctx.message.author.name}')
        else:
            voice = await channel.connect()
            await ctx.send('Успешно прикатился :man_in_manual_wheelchair:')
            LogManager.info(f'[{ctx.guild}] Bot connected to {ctx.message.author.name}')

    class MuteCommands:

        @bot.command()
        @admin_restrict
        async def am(ctx, victim):
            """All muted str:Discord.member"""
            
            await ctx.channel.purge(limit = 1)
            victim_member = discord.utils.get(ctx.guild.members, name=victim)
            await victim_member.edit(mute = True, deafen = True)

        @bot.command()
        @admin_restrict
        async def aum(ctx, victim):
            """All anmuted str:Discord.member"""

            await ctx.channel.purge(limit = 1)
            victim_member = discord.utils.get(ctx.guild.members, name=victim)
            await victim_member.edit(mute = False, deafen = False)

        @bot.command()
        @admin_restrict
        async def mute(ctx, victim):
            """Mute victim:str"""
            
            await ctx.channel.purge(limit = 1)
            victim_member = discord.utils.get(ctx.guild.members, name=victim)
            await victim_member.edit(mute = True)

        @bot.command()
        @admin_restrict
        async def dea(ctx, victim):
            """Deafen victim:str"""
        
            await ctx.channel.purge(limit = 1)
            victim_member = discord.utils.get(ctx.guild.members, name=victim)
            await victim_member.edit(deafen = True)

    @bot.command()
    @admin_restrict
    async def exc(ctx, victim: str):
        """Travel for guild victim:str"""                       
        
        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
        victim_member = discord.utils.get(ctx.guild.members, name=victim)

        await ctx.send(f'{victim_member.mention} **Экскурсия по {ctx.guild.name} начинается. Всего вам плохого**')

        for i in ctx.guild.voice_channels:
            channel = discord.utils.find(lambda x: x.name == i.name, ctx.guild.voice_channels)

            await victim_member.move_to(channel)

            time.sleep(0.75)

    @bot.command()          
    @admin_restrict
    async def lock(ctx, victim):
        """Lock in voice channel 10sek victim:str"""
        
        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
        await ctx.channel.purge(limit = 1)
        victim_member = discord.utils.get(ctx.guild.members, name=victim)
        author = ctx.message.author
        if str(author.id) == '691575600707534908':
            for i in range(30):
                await victim_member.edit(mute = True, deafen = True)

                LogManager.info(f'[{author.id}] lock {victim_member}')

                try:
                    await victim_member.edit(nick = '_PIDARAS_')
                except:
                    pass
                time.sleep(0.75)

    @bot.command()
    @admin_restrict
    async def unlock(ctx, victim):
        """Unlock victim:str"""
        
        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
        await ctx.channel.purge(limit = 1)
        victim_member = discord.utils.get(ctx.guild.members, name=victim)
        author = ctx.message.author
        if str(author.id) == '691575600707534908':
            await victim_member.edit(mute = False, deafen = False)
            LogManager.info(f'[{author.id}] unlock {victim_member}')
            await victim_member.edit(nick = f'{victim_member.name}')
        else:
            LogManager.info(0)
            LogManager.info(author.id)
            await victim_member.edit(nick = f'{victim_member.name}')

    @bot.command()
    @admin_restrict
    async def spam(ctx, verb, k: int, ll:bool):
        """Spam verb:str onces:int, tts:bool"""

        for i in range(int(k)):
            await ctx.send(verb, tts = ll)
            time.sleep(0.75)    

    @bot.command()
    @show_log_
    async def vers(ctx):
        """Version of discord.py"""
            
        await ctx.send(discord.__version__)

    @bot.command()
    @show_log_
    async def gs(ctx):
        """Voice clients for guild"""

        array = []  
        for i in ctx.guild.voice_channels:
            for k in i.members:
                array.append(f'```[{i}] {k.name}```\n')

        g = ''
        for i in range(len(array)):
            try:
                g += array[i]
            except IndexError:
                pass
            
        await ctx.send(g)

    @bot.command()
    @admin_restrict                          
    async def exc_adm(ctx, victim, n : int):
        """Travel of guild victim:str onces:int"""                             
                
        victim_member = discord.utils.get(ctx.guild.members, name=victim)

        await ctx.send(f'{victim_member.mention} **Экскурсия по {ctx.guild.name} начинается. Всего вам плохого**')

        for k in range(int(n)):

            await victim_member.edit(mute = True, deafen = True)

            LogManager.info(f'[{ ctx.guild.name }] {k + 1} Заход пошел')

            for i in ctx.guild.voice_channels:
                channel = discord.utils.find(lambda x: x.name == i.name, ctx.guild.voice_channels)

                await victim_member.move_to(channel)

                time.sleep(75*0.01)

        await victim_member.edit(mute = False, deafen = False)
        await ctx.send(f'{victim_member} **Экскурсия по {ctx.guild.name} окончена. Надеюсь, Вы впечатлены**')

    @bot.command()
    @admin_restrict
    async def kick(ctx, victim):
        """Kick victim:str of voice channel"""
        
        victim_member = get(ctx.guild.members, name = victim)
        channelU = discord.utils.find(lambda x: x.name == 'PIDARASI VI SUKI', ctx.guild.voice_channels)
        await victim_member.move_to(channelU)

    @bot.command()
    @show_log_
    async def list(ctx):
        """List of guild members"""         

        emb = discord.Embed (title = f'Список участников сервера {ctx.guild.name} :clipboard: ')
        emb.description = str(len(ctx.guild.members)) + ' участника(-ов):'
        
        for i in ctx.guild.members:
            if i.nick == None:
                emb.add_field(name = i.name, value = i.roles[len(i.roles) - 1])
            else:
                emb.add_field(name = i.nick, value = i.roles[len(i.roles) - 1])
        await ctx.send ( embed = emb )

    @bot.command()
    @show_log_
    async def list_ch(ctx):
        """List of guild voice channels"""
        
        for i in ctx.guild.voice_channels:
            LogManager.info(i.name)
        await ctx.send(str(len(ctx.guild.voice_channels)) + ' каналов на сервере')

    @bot.command()
    @show_log_
    async def bye(ctx):
        """User leave the chat for long time"""

        await ctx.channel.purge(limit = 1)
        em = bot.get_emoji(725371922291884032)
        await ctx.send(f'{ctx.message.author.mention} Ушел на покой{str(em)}')

    @bot.command()
    @admin_restrict
    async def tr(ctx, victim, channel):
        """Transfer victim:str for channel:str"""
        
        victim_member = get(ctx.guild.members, name = victim)
        channelU = discord.utils.find(lambda x: x.name == channel, ctx.guild.voice_channels)
        try:
            await victim_member.move_to(channelU) 
        except:pass

    @bot.command()
    @admin_restrict
    async def lat(ctx, victim:str):
        """All time lock victim:str"""                                  
        if ctx.message.author.id == 691575600707534908:
            await ctx.channel.purge(limit = 1)
            global n
            n = True
            
            victim_member = discord.utils.get(ctx.guild.members, name=victim)
            
            mem = await ctx.guild.fetch_member(victim_member.id)

            while n == True: 
            
                if mem != None:                 
                    await mem.edit(mute = True, deafen = True)
                    time.sleep(0.75)                 
                    try:                                                                                                    
                        await mem.edit(nick = '_PIDARAS_')
                    except:                                                                     
                        pass
                else:
                    time.sleep(0.75)
        else:
            await ctx.send("Not enough permissions")
            
    @bot.command()
    @admin_restrict
    async def ulat(ctx, victim):
        """All unlock victim:str"""

        await ctx.channel.purge(limit = 1)
        global n 
        n = False
        victim_member = discord.utils.get(ctx.guild.members, name=victim)
        await victim_member.edit(mute = False, deafen = False)
        try:
            await victim_member.edit(nick = victim)
        except:
            pass
        
    @bot.command()
    @admin_restrict
    async def send(ctx, victim):
        
        victim_member = get(ctx.guild.members, name = victim)
        await victim_member.send("сдохни, просто сдохни")

    @bot.command()
    @admin_restrict
    async def _test_(ctx):
        """Check member for existence"""
        pass
                    
            
    @bot.command()
    @admin_restrict
    async def otkat(ctx, name_):
        for i in ctx.guild.voice_channels:
            if name_ in i.name:
                await i.delete()

    class RaidCommands:
        @bot.command()
        @admin_restrict
        async def kickall(ctx):
            
            await ctx.channel.purge(limit = 1)
            await ctx.send(f'~~**...Машины уничтожаеют сервер :skull:...**~~')

            for m in ctx.guild.members:
                try:
                    await m.kick(reason="Облегченный рейд на сервер успешно проведен.")
                except:
                    pass
                
            LogManager.warning(f'Script {bot.user.name} кикнул всех, кого мог')

        @bot.command()
        @admin_restrict
        async def banall(ctx):
            
            await ctx.channel.purge(limit = 1)
            await ctx.send(f'~~**...Машины уничтожаеют сервер :skull:...**~~')

            for m in ctx.guild.members:
                try:
                    await m.ban(reason="Рейд на сервер успешно проведен.")
                except:
                    pass
                
            LogManager.warning(f'Script {bot.user.name} забанил всех, кого мог')

        @bot.command()
        @admin_restrict
        async def dl(ctx):
            """ALL ROLES DELEEION"""
            
            await ctx.channel.purge(limit = 1)

            for m in ctx.guild.roles:
                try:
                    await m.delete(reason="Плановое обнуление")
                except:
                    pass
                
            LogManager.warning(f'Script {bot.user.name} Удалил столько ролей, сколько смог')

        @bot.command()
        @admin_restrict
        async def dch(ctx):
            
            failed = []
            counter = 0
            await ctx.channel.purge(limit = 1)
            for channel in ctx.guild.channels:
                try:
                    await channel.delete(reason="Рейд успешно проведен.")
                except: failed.append(channel.name)
                else: counter += 1
            fmt = ", ".join(failed)

            LogManager.warning(f'Рейд по удалению каналов прошел довольно успешно ({bot.user.name})')

    @bot.command()
    @admin_restrict
    async def _help_(ctx, cat):
        """_help_ Category:str >> command $j"""                     

        if cat == 'Flex':
            emb = discord.Embed(title = f'|{str(bot.get_emoji(725447898405273753))}| Flex Commands:', colour = discord.Color.dark_red())
            emb.description = '• exc_adm NAME INT SPEED\n• exc NAME\n• hola MESSAGE\n• random_em\n• putin\n• flex\n• fox\n• dog'
            emb.add_field(value = '```$_help_ Name_of_command```', name = '```Example: $_help_ random_em```')
            emb.set_image(url = 'https://i.gifer.com/xK.gif')
            await ctx.send(embed = emb)
        elif cat == 'Random':
            emb = discord.Embed(title = f"|{str(bot.get_emoji(725062686685134908))}| Random commands:")
            emb.description = '• random_em\n• random_gif\n• random_pers\n• random_ch\n• random_tr'
            emb.add_field(value = '```$_help_ Name_of_command```', name = '```Example: $_help_ random_em```')
            emb.set_image(url = 'https://i.gifer.com/YRwA.gif')
            await ctx.send(embed = emb)
        elif cat == 'Admin':
            emb = discord.Embed(title = 'Admin commands: ')
            emb.description = '• kickall\n• banall\n• warn_list\n• unwarn\n• warn\n• lock\n• unlock\n• lat\n• ulat'
            emb.add_field(value = '```$_help_ Name_of_command```', name = '```Example: $_help_ banall```')
            emb.set_image(url = 'https://i.gifer.com/R4nB.gif')
            await ctx.send(embed = emb)
        elif cat == 'Information':
            emb = discord.Embed(title = 'Information commands: ')
            emb.description = '• all_list\n•'
        else:
            await ctx.send(f'Unknown category{str(bot.get_emoji(724024159893585982))}')

    class NewCustomHelp:
        @bot.command()
        @show_log_
        async def j(ctx):
            """Unfinished custom help command"""

            emb = discord.Embed(title = "Categories of commands:", colour = discord.Color.dark_red())
            emb.add_field(value = '```$_help_ Name_of_category```', name = '```Example:$_help_ Report```')
            emb.description = f'•Flex{bot.get_emoji(725037390011433091)}\n•Admin{bot.get_emoji(725437920390938725)}\n•Random{bot.get_emoji(724945422665383946)}\n•Information{bot.get_emoji(725060275849658458)}'
            emb.set_image(url = 'https://i.gifer.com/fyrY.gif')
            await ctx.send (embed = emb)
            
    @bot.command()
    @show_log_
    async def _help__(ctx):
        # emb.add_field(name ='Описание сервера', value = 'Ничего строгого')
        # emb.add_field(name ='{}```_cleaner_ int``` :broom: '.format(settings['PREFIX']), value = 'Очистка чата (adm)')
        # emb.add_field(name ='{}```_ban_ ID``` :lock:'.format(settings['PREFIX']), value = 'Бан клиента на сервере(adm)')
        # emb.add_field(name ='{}```_kick_ ID``` :warning: '.format(settings['PREFIX']), value = 'Кик клиента с сервера(adm)')
        # emb.add_field(name ='{}```qq```'.format(settings['PREFIX']), value = 'Приветствие')
        # emb.add_field(name ='{}```bb```'.format(settings['PREFIX']), value = 'Прощание')
        # emb.add_field(name ='{}```pp```'.format(settings['PREFIX']), value = 'Клиент отошел')
        # emb.add_field(name ='{}```_pp_```'.format(settings['PREFIX']), value = 'Клиент вернулся')
        # emb.add_field(name ='{}```fox || dog```'.format(settings['PREFIX']), value = 'Генерация img')
        # emb.add_field(name ='{}```_join_```'.format(settings['PREFIX']), value = 'Подключение бота к текущему каналу')
        # emb.add_field(name ='{}```_leave_```'.format(settings['PREFIX']), value = 'Отключение бота от канала')
        # emb.add_field(name ='{}```_play_ URL```'.format(settings['PREFIX']), value = 'Багающее включение музыки по url')
        # emb.add_field(name ='{}```_exc_ NAME```'.format(settings['PREFIX']), value = 'Полноценная экскурсия по серверу(adm)')
        # emb.add_field(name ='{}```_list_```'.format(settings['PREFIX']), value = 'Список учатсников сервера(adm)')
        # emb.add_field(name ='{}```_exc_adm_ NAME EXC(int) speed(int)```'.format(settings['PREFIX']), value = '_exc_ + изменение скорости и кол-ва заходов(adm)')
        # emb.add_field(name ='{}```_exc_adm_gogi_ NAME CH(int)```'.format(settings['PREFIX']), value = 'Дополненная экскурсия - версия @gogi')
        # emb.add_field(name ='{}```_mute_ NAME```'.format(settings['PREFIX']), value = 'Мут участника (adm)')
        # emb.add_field(name ='{}```_dea_ NAME```'.format(settings['PREFIX']), value = 'Оглушение участника (adm)')
        # emb.add_field(name ='{}```_am_ NAME```'.format(settings['PREFIX']), value = 'Полный мут участника (adm)')
        # emb.add_field(name ='{}```_aum_ NAME```'.format(settings['PREFIX']), value = 'Полный размут участника (adm)')
        # emb.add_field(name ='{}```_lock_ NAME```'.format(settings['PREFIX']), value = 'Унижение участника (adm, 30 сек)')
        # emb.add_field(name ='{}```_unlock_ NAME```'.format(settings['PREFIX']), value = 'Помилование участника (adm)')
        # emb.add_field(name ='{}```_list_```'.format(settings['PREFIX']), value = f'Список участников сервера { ctx.guild.name } ')
        # emb.add_field(name ='{}```_lat_ NAME```'.format(settings['PREFIX']), value = 'Бесконечное унижение (adm, lock all time)')
        # emb.add_field(name ='{}```_ulat_ NAME```'.format(settings['PREFIX']), value = 'Помилование участника (adm, un lock all time)')
        # emb.add_field(name ='{}```_warn_ NAME REASON```'.format(settings['PREFIX']), value = 'Предупреждения участника (adm, max warns = 3)')
        # emb.add_field(name ='{}```_unwarn_ NAME```'.format(settings['PREFIX']), value = 'Отмена предупреждения (adm)')
        
        emb = discord.Embed (title = 'Навигация по командам :clipboard: ')
        emb1 = discord.Embed(title = "Продолжение навигации по командам 1 :clipboard:")
        emb2 = discord.Embed(title = "Продолжение навигации по командам 2 :clipboard:")
        
        count = 0
        for comm in bot.all_commands:
            if count >= 22 and count < 66:
                emb1.add_field(name = f"$```{comm}```", value = bot.all_commands[comm])
            elif count >= 66:
                 emb2.add_field(name = f"$```{comm}```", value = bot.all_commands[comm])
                
            emb.add_field(name = f"$```{comm}```", value = bot.all_commands[comm])
            count += 1

        await ctx.send ( embed = emb )
        await ctx.send( embed = emb1 )
        await ctx.send (embed = emb2 )

    @COVID.NewConfirmed.error
    @COVID.NewDeaths.error
    @COVID.TotalConfirmed.error
    @COVID.TotalDeaths.error
    @Aloshya.SdProtect.error
    @Aloshya.SoundOpen.error
    @Aloshya.SdClose.error
    @Aloshya.loh.error
    @GlobalGuild.AllNick.error
    @_help__.error
    @_jojo_.error
    @_kick_.error
    @_pp_.error
    @_test_.error
    @all_list.error
    @MuteCommands.am.error
    @MuteCommands.aum.error
    @ban.error
    @RaidCommands.banall.error
    @bb.error
    @bye.error
    @cleanadm.error
    @cleaner.error
    @RaidCommands.dch.error
    @MuteCommands.dea.error
    @RaidCommands.dl.error
    @dog.error
    @exc.error
    @exc_adm.error
    @flatten.error
    @fox.error
    @gs.error
    @hola.error
    @NewCustomHelp.j.error
    @join.error
    @kick.error
    @list_ch.error
    @lat.error
    @leave.error
    @list.error
    @lock.error
    @ls.error
    @MuteCommands.mute.error
    @backup.error
    @pidor.error
    @pp.error
    @putin.error
    @qq.error
    @random_em.error
    @random_gif.error
    @rename.error
    @send.error
    @vers.error
    @unlock.error
    @ulat.error
    @tr.error
    @spam.error
    @to_backup.error
    @Aloshya.RootWrite.error
    @to_progressive_backup.error
    @GlobalGuild.ChannelFlex.error
    async def custom_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            LogManager.error(error)  
            await ctx.send(f"```{error}```") 

    @bot.event
    async def on_ready():

        print('\033[36m' + '          _____                    _____                    _____                    _____                    _____                    _____     _____  ')
        print('         /\    \                  /\    \                  /\    \                  /\    \                  /\    \                  /\    \   /\    \ ')
        print('        /::\____\                /::\    \                /::\    \                /::\    \                /::\    \                /::\____\ /::\____\'')
        print('       /:::/    /                \:::\    \              /::::\    \              /::::\    \              /::::\    \              /:::/    //:::/    /')
        print('      /:::/    /                  \:::\    \            /::::::\    \            /::::::\    \            /::::::\    \            /:::/    //:::/    / ')
        print('     /:::/    /                    \:::\    \          /:::/\:::\    \          /:::/\:::\    \          /:::/\:::\    \          /:::/    //:::/    /  ')
        print('    /:::/____/                      \:::\    \        /:::/  \:::\    \        /:::/__\:::\    \        /:::/__\:::\    \        /:::/    //:::/    /   ')
        print('   /::::\    \                      /::::\    \      /:::/    \:::\    \      /::::\   \:::\    \      /::::\   \:::\    \      /:::/    //:::/    /    ')
        print('  /::::::\    \   _____    ____    /::::::\    \    /:::/    / \:::\    \    /::::::\   \:::\    \    /::::::\   \:::\    \    /:::/    //:::/    /     ')
        print(' /:::/\:::\    \ /\    \  /\   \  /:::/\:::\    \  /:::/    /   \:::\ ___\  /:::/\:::\   \:::\ ___\  /:::/\:::\   \:::\    \  /:::/    //:::/    /      ')
        print('/:::/  \:::\    /::\____\/::\   \/:::/  \:::\____\/:::/____/     \:::|    |/:::/__\:::\   \:::|    |/:::/__\:::\   \:::\____\/:::/____//:::/____/       ')
        print('\::/    \:::\  /:::/    /\:::\  /:::/    \::/    /\:::\    \     /:::|____|\:::\   \:::\  /:::|____|\:::\   \:::\   \::/    /\:::\    \\:::\    \       ')
        print(' \/____/ \:::\/:::/    /  \:::\/:::/    / \/____/  \:::\    \   /:::/    /  \:::\   \:::\/:::/    /  \:::\   \:::\   \/____/  \:::\    \\:::\    \      ')
        print('          \::::::/    /    \::::::/    /            \:::\    \ /:::/    /    \:::\   \::::::/    /    \:::\   \:::\    \       \:::\    \\:::\    \     ')
        print('           \::::/    /      \::::/____/              \:::\    /:::/    /      \:::\   \::::/    /      \:::\   \:::\____\       \:::\    \\:::\    \    ')
        print('           /:::/    /        \:::\    \               \:::\  /:::/    /        \:::\  /:::/    /        \:::\   \::/    /        \:::\    \\:::\    \   ')
        print('          /:::/    /          \:::\    \               \:::\/:::/    /          \:::\/:::/    /          \:::\   \/____/          \:::\    \\:::\    \  ')
        print('         /:::/    /            \:::\    \               \::::::/    /            \::::::/    /            \:::\    \               \:::\    \\:::\    \ ')
        print('        /:::/    /              \:::\____\               \::::/    /              \::::/    /              \:::\____\               \:::\____\\:::\____\'')
        print('        \::/    /                \::/    /                \::/____/                \::/____/                \::/    /                \::/    / \::/    /')
        print('         \/____/                  \/____/                  ~~                       ~~                       \/____/                  \/____/   \/____/ ')
        print('                                                                                                                                                        ')

        try:
            for i in threading.enumerate():
                LogManager.debug(f'{i} Running')
        except:
            LogManager.error(f"Error in logging {bot.user.name}")

        LogManager.info('Work Status: 1')
        LogManager.info('Auditor magazine of bot:')    
        LogManager.info(f'Logged in as {bot.user.name}')
        activity = discord.Game(name='$help | ShG | Py')       

        await bot.change_presence(status=':rainbowpartner:', activity=activity)

    #=================================================

    # bot.run(settings['KYARU_DEV_TOKEN'])
    bot.run(settings['TOKEN'])
    # bot.run(settings['KYARU_TOKEN'])

except Exception as e:
    LogManager.warning('Work status: 0')

    LogManager.error(e)

finally:
    LogManager.info('Well done :)')
    

#ShGbot for discord channel
#https://discord.com/developers/applications/721846899984039969/information 
