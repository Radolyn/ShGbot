try:
    import discord
    import json 
    import sys
    import os
    import time 
    import random
    import requests
    import asyncio
    import discord.ext.commands
    from discord.ext import commands
    from discord import utils
    from discord.utils import get
    from discord.ext.commands import Bot
    from discord.voice_client import VoiceClient
    import threading
    from config import *
    from LogPython import LogManager
except ImportError as e: 
    print('[WARNING] Вероятнее всего, Вы не запустили deps.py ($python deps.py)', e)
    exit()
finally:
    LogManager = LogManager()
    LogManager.pre_warn(" Libraries downloaded successfully >> logging started >> audit log:")                                                                                        



bot = Bot(settings['PREFIX'])

#bot.remove_command('help')

resp = requests.get("https://api.covid19api.com/summary")

json_data = json.loads(resp.text)

try:        
    class GlobalGuild:

        @bot.command()
        async def AllNick(ctx, word:str):
            await ctx.channel.purge(limit = 1)
            for i in ctx.guild.members:
                try:
                    await i.edit(nick = str(word))
                    time.sleep(.75)
                    LogManager.info(i.name)
                except:
                    pass

            LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")

        @bot.command()
        async def SkipAllNick(ctx):
            await ctx.channel.purge(limit = 1)
            for i in ctx.guild.members:
                try:
                    await i.edit(nick = i.name)
                    time.sleep(.75)
                    LogManager.info(i.name)
                except:
                    pass

            LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")

        @bot.command()
        async def testing(ctx, victim):
            await ctx.channel.purge(limit = 1)
            for i in ctx.guild.members:
                try:
                    LogManager.info(i.name)
                except Exception as e:
                    LogManager.error(e)

            LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")

    class Aloshya:
        @bot.command()        
        async def SoundOpen(ctx):
            await ctx.channel.purge(limit = 1)
            for i in ctx.guild.voice_channels:
                for k in i.members:
                    LogManager.info(f'{k} all unmuted')
                    await k.edit(mute = False, deafen = False)

            LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
                    
        @bot.command()    
        async def SdClose(ctx):
            await ctx.channel.purge(limit=1)
            for i in ctx.guild.voice_channels:
                for k in i.members:
                    LogManager.info(f'{k} all muted')
                    await k.edit(mute = True, deafen = True)

            LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")

        @bot.command()       
        async def SdProtect(ctx, victim:str):
            await ctx.channel.purge(limit = 1)
            for i in ctx.guild.voice_channels:
                for k in i.members:
                    if k.name != str(victim) and k.name != ctx.message.author.name:
                        await k.edit(mute = True, deafen = True)      

            LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")             

        @bot.command()
        @commands.has_permissions(administrator = True)
        async def loh(ctx, victim):
            victim_member = discord.utils.get(ctx.guild.members, name=victim)

            await ctx.channel.purge(limit = 1)

            LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")


            while True:
                
                try:
                    
                    mem = await ctx.guild.fetch_member(victim_member.id)
                    channel = mem.voice.channel
                    _voice = await channel.connect()

                    if _voice and _voice.is_connected():
                            await _voice.move_to(channel)                    
                            LogManager.info(f"{bot} connect")
                            await _voice.disconnect()                                                        
                            LogManager.info(f"{bot} disconnect")
                            time.sleep(0.75)
                    else: 
                        
                        LogManager.warning("VoiceError time.sleep(1)")              
                        time.sleep(.75)
                except AttributeError:
                    time.sleep(1)
                    LogManager.warning("AttributeError time.sleep(1)")

        # @bot.command()
        # @commands.has_permissions(administrator = True)
        # async def unloh(ctx, victim)
                
            
    @bot.command()
    async def flatten(ctx):
        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")

        await ctx.send(f"Last command error:```py\n{LogManager.get_errors()}```")

    class COVID:
        @bot.command()
        async def NewConfirmed(ctx):
    
            author = ctx.message.author

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

                                LogManager.debug("Found succesfully completed")
                            else:
                                LogManager.debug("Found crashed")
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
                LogManager.debug_cmd(f"[NewConfirmedOnDay_COVID-19] {res[l]}")
                str1 += res[l] + "\n"

            emb.description = str1

            await ctx.send(embed = emb)

            LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")

        @bot.command()
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

                                LogManager.debug("Found succesfully completed")
                            else:
                                LogManager.debug("Found crashed")
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
                LogManager.debug_cmd(f"[NewDeathsOnDay_COVID-19] {res[l]}")
                str1 += res[l] + "\n"

            emb.description = str1

            await ctx.send(embed = emb)

            LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")

        @bot.command()   
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

                                LogManager.debug("Found succesfully completed")
                            else:
                                LogManager.debug("Found crashed")
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
                LogManager.debug_cmd(f"[TotalConfirmed_COVID-19] {res[l]}")
                str1 += res[l] + "\n"

            emb.description = str1

            await ctx.send(embed = emb)

            LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")

        @bot.command()
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

                                LogManager.debug("Found succesfully completed")
                            else:
                                LogManager.debug("Found crashed")
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
                LogManager.debug_cmd(f"[TotalDeaths_COVID-19] {res[l]}")
                str1 += res[l] + "\n"    

            emb.description = str1

            await ctx.send(embed = emb)

            LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")

    @bot.command()
    async def te(ctx):
        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
        
        for guild in bot.guilds:
            await ctx.send(guild.name)
            await ctx.send(guild.id)

    @bot.command()
    async def ls(ctx):
        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
        
        array , array1 = [], []     
        for guild in bot.guilds:
            array.append(guild.name)
            array1.append(guild.id)
        
        emb = discord.Embed(title = f"Список серверов, на которых катируется бот: {str(int(len(array)))}")
        for i in range(len(array)):
            emb.add_field(name = array1[i], value = array[i])
        await ctx.send( embed = emb )

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def pidor(ctx):
        for i in range(1000000):
            await ctx.guild.create_voice_channel(name = f'З.а.е.б.а.л.и.{i}')
            
        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def all_list(ctx):
        """List of guild channels"""
        
        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
        
        await ctx.send(f'{len(ctx.guild.channels)} channels in guild')

    @bot.command()
    async def random_gif(ctx):
        ho = random.choice(gif)
        emb = discord.Embed(title = f'Random gif{str(bot.get_emoji(725061079914250300))}')
        emb.set_image(url = ho)
        await ctx.send(embed = emb)
        
        LogManager.info(f'[{ctx.guild.name}] Bot send {ho}')

    @bot.command()
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

        

        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")

    @bot.command()
    async def leave(ctx):
        """Bot leave voice channel"""

        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
        
        channel = ctx.message.author.voice.channel
        voice = get(bot.voice_clients, guild = ctx.guild)
        
        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send('Успешно откатился :camel:')
        else:
            await voice.disconnect()
            await ctx.send('Успешно откатился :camel:')

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def putin(ctx):
        """Vladimir Putin`s emoji"""

        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
        
        await ctx.channel.purge(limit = 1)
        await ctx.send(f'{str(bot.get_emoji(725059390331289651))}{str(bot.get_emoji(725059390331289651))}{str(bot.get_emoji(725059390331289651))}{str(bot.get_emoji(725059390331289651))}{str(bot.get_emoji(725059390331289651))}{str(bot.get_emoji(725059390331289651))}{str(bot.get_emoji(725059390331289651))}')

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def rename(ctx, channel: discord.VoiceChannel, *, new_name):
        """Rename channel:discord.VoiceChannel:str, new_name:str"""

        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
        await channel.edit(name=new_name)

    @bot.event
    async def on_command_error(ctx, error):
        em = bot.get_emoji(724944121109676092)                              
        if isinstance(error, commands.CommandNotFound ):
            LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
            await ctx.send(f'**{ctx.message.author.mention}, данная команда не обнаружена**{str(em)}')

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _jojo_(ctx, victim: discord.Member, reason = "Доигрался, вот тебе ролевые игры"):
        """Custom kick victim:str of guild (may be not working now)"""
        
        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
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
    async def hola(ctx, arg):
        
        await ctx.channel.purge(limit = 1)
        await ctx.send(arg), LogManager.info(f'[{ctx.guild.name}] $Bot send message: {arg} >> called by {ctx.message.author.name}')

    @bot.command()
    async def qq(ctx):
        """Hello, server"""

        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
        author = ctx.message.author

        if author.nick != None:
            await ctx.send(f'Категорически приветствую, {author.mention}!'), LogManager.info(f'[{ctx.guild.name}] $Bot send message: Hello, {author.nick} ({author.name})')
        else:
            await ctx.send(f'Категорически приветствую, {author.mention}!'), LogManager.info(f'[{ctx.guild.name}] $Bot send message: Hello, {author.name}')

    @bot.command()
    async def bb(ctx):
        """Bye, all"""
        
        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
        author = ctx.message.author

        if author.nick != None:
            await ctx.send(f'До связи, {author.mention} :)'), LogManager.info(f'[{ctx.guild.name}] $Bot send message: Bye, {author.nick} ({author.name})')
        else:
            await ctx.send(f'До связи, {author.mention} :)'), LogManager.info(f'[{ctx.guild.name}] $Bot send message: Bye, {author.name}')

    @bot.command()
    async def pp(ctx):
        """If walked away for a while"""
        
        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
        await ctx.channel.purge(limit = 1)
        author = ctx.message.author

        if author.nick != None:
            await ctx.send(f'{author.mention} Отошел.'), LogManager.info(f'[{ctx.guild.name}] $Bot send message: {author.nick} ({author.name}) Отошел.')
        else:
            await ctx.send(f'{author.mention} Отошел.'), LogManager.info(f'[{ctx.guild.name}] $Bot send message: {author.name} Отошел.')

    @bot.command()
    async def _pp_(ctx):
        """Returned"""
        
        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
        await ctx.channel.purge(limit = 1)

        author = ctx.message.author
        user = author.nick

        if author.nick != None:
            await ctx.send(f'{author.mention} Вернулся.'), LogManager.info(f'[{ctx.guild.name}] $Bot send message: {author.name} ({author.nick}) Вернулся.')
        else:
            await ctx.send(f'{author.mention} Вернулся.'), LogManager.info(f'[{ctx.guild.name}] $Bot send message: {author.name} Вернулся.')              

    @bot.command()
    async def fox(ctx):
        """Simple fox"""
        
        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
        response = requests.get('https://some-random-api.ml/img/fox')
        json_data = json.loads(response.text)
        author = ctx.message.author

        embed = discord.Embed(color = 0xff9900, title = 'Random Fox')
        embed.set_image(url = json_data['link'])
        await ctx.send(embed = embed), LogManager.info(f'[{ctx.guild.name}] $Bot send embed fox by {ctx.message.author.name}' )

    @bot.command()
    async def dog(ctx):
        """Simple dog"""
        
        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
        response = requests.get('https://some-random-api.ml/img/dog')
        json_data = json.loads(response.text)
        author = ctx.message.author

        embed = discord.Embed(color = 0xff9900, title = 'Random Dog')
        embed.set_image(url = json_data['link'])
        member = discord.Member
        try: await ctx.send(embed = embed), LogManager.info(f'[{ctx.guild.name}] $Bot send embed dog (by {ctx.message.author.name}' )
        except: await ctx.send('CommandNotFound', {author.mention})

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def cleaner(ctx, amount):
        """Cleaner chat for int positions"""

        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")

        em = [
            str(bot.get_emoji(725432947150159974)),
            str(bot.get_emoji(725448560388210738))
        ]

        k = random.choice(em)

        
        em = str(bot.get_emoji(725432947150159974))

        author = ctx.message.author

        await ctx.channel.purge(limit=int(amount))
        await ctx.channel.send(':: Сообщения успешно удалены' + k), LogManager.info(f'[{ctx.guild.name}] {author.name} cleaned chat for {amount} positions')

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def _kick_ (ctx, member: discord.Member, *, reason = None):
        """Kick for the guild"""

        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
        emb = discord.Embed (title = 'Kick :warning:', colour = discord.Color.dark_red())

        await ctx.channel.purge(limit = 1)
                        
        await member.kick(reason = reason)

        emb.set_author (name = member.name, icon_url = member.avatar_url)
        emb.add_field (name = 'Kick user', value = 'Kicked user : {}'.format(member.mention))
        emb.set_footer (text = 'Был опасхален администратором {}'.format (ctx.author.name), icon_url = ctx.author.avatar_url)

        await ctx.send (embed = emb)

        LogManager.info(f'[{ctx.guild.name}] Bot kicked { member }')

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def ban (ctx, member: discord.Member, *, reason = f'Нарушение правил сервера. $Banlist.append(you)'):
        """Ban for guild"""       

        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
        emb = discord.Embed (title = 'Ban :lock:', colour = discord.Color.dark_red())

        await ctx.channel.purge(limit = 1)

        await member.ban(reason = reason)

        emb.set_author (name = member.name, icon_url = member.avatar_url)
        emb.add_field (name = 'Ban user', value = 'Ban user : {}'.format(member.mention))
        emb.set_footer (text = 'Был смешан с асфальтом администратором {}'.format (ctx.author.name), icon_url = ctx.author.avatar_url)

        await ctx.send (embed = emb)

        LogManager.info(f'[{ctx.guild.name}] Bot banned { member }')



    @bot.command()
    @commands.has_permissions(administrator = True)
    async def cleanadm(ctx, amount):
        """Cleaning chat without other mes"""
        
        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
        author = ctx.message.author
        await ctx.channel.purge(limit=int(amount))
        LogManager.info(f'[{ctx.guild.name}] {author.name} cleaned chat for {amount} positions')

    @bot.command()
    async def join(ctx):
        """Bot join voice channel"""
        
        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
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
        @commands.has_permissions(administrator = True)
        async def am(ctx, victim):
            """All muted str:Discord.member"""
            
            LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
            await ctx.channel.purge(limit = 1)
            victim_member = discord.utils.get(ctx.guild.members, name=victim)
            await victim_member.edit(mute = True, deafen = True)
            LogManager.info(f'[{ctx.guild}] {ctx.message.author} all muted {victim_member}')

        @bot.command()
        @commands.has_permissions(administrator = True)
        async def aum(ctx, victim):
            """All anmuted str:Discord.member"""

            LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
            await ctx.channel.purge(limit = 1)
            victim_member = discord.utils.get(ctx.guild.members, name=victim)
            await victim_member.edit(mute = False, deafen = False)
            LogManager.info(f'[{ctx.guild}] {ctx.message.author} all unmuted {victim_member}')

        @bot.command()
        @commands.has_permissions(administrator = True)
        async def mute(ctx, victim):
            """Mute victim:str"""
            
            LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
            await ctx.channel.purge(limit = 1)
            victim_member = discord.utils.get(ctx.guild.members, name=victim)
            await victim_member.edit(mute = True)
            LogManager.info(f'[{ctx.guild}] {ctx.message.author} muted {victim_member}')

        @bot.command()
        @commands.has_permissions(administrator = True)
        async def dea(ctx, victim):
            """Deafen victim:str"""
            
            LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
            await ctx.channel.purge(limit = 1)
            victim_member = discord.utils.get(ctx.guild.members, name=victim)
            await victim_member.edit(deafen = True)
            LogManager.info(f'[{ctx.guild}] {ctx.message.author} deafen {victim_member}')               


    @bot.command()
    @commands.has_permissions(administrator = True)
    async def exc(ctx, victim: str):
        """Travel for guild victim:str"""                       
        
        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
        victim_member = discord.utils.get(ctx.guild.members, name=victim)

        await ctx.send(f'{victim_member.mention} **Экскурсия по {ctx.guild.name} начинается. Всего вам плохого**')

        for i in ctx.guild.voice_channels:
            channel = discord.utils.find(lambda x: x.name == i.name, ctx.guild.voice_channels)

            await victim_member.move_to(channel)

            time.sleep(0.75)

            print(f' [nologging_noformatting] [exc] {victim} transfered {i.name}')

    @bot.command()          
    @commands.has_permissions(administrator = True)
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
        else:
            LogManager.info(0)
            LogManager.info(author.id)

    @bot.command()
    @commands.has_permissions(administrator = True)
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
    @commands.has_permissions(administrator = True)
    async def spam(ctx, verb, k: int, ll:bool):
        """Spam verb:str onces:int, tts:bool"""
        
        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")

        for i in range(int(k)):
            LogManager.info(f'[{ctx.guild.name}] Bot send {verb}')
            await ctx.send(verb, tts = ll)
            time.sleep(0.75)    

    @bot.command()
    async def vers(ctx):
        """Version of discord.py"""
        
        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
        await ctx.send(discord.__version__)

    @bot.command()
    async def gs(ctx):
        """Voice clients for guild"""
        
        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")

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
    @commands.has_permissions(administrator = True)                             
    async def exc_adm(ctx, victim, n:int):
        """Travel of guild victim:str onces:int"""                             
        
        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
        victim_member = discord.utils.get(ctx.guild.members, name=victim)

        await ctx.send(f'{victim_member.mention} **Экскурсия по {ctx.guild.name} начинается. Всего вам плохого**')

        for k in range(int(n)):

            await victim_member.edit(mute = True, deafen = True)

            LogManager.info(f'[{ ctx.guild.name }] {k + 1} Заход пошел')

            for i in ctx.guild.voice_channels:
                channel = discord.utils.find(lambda x: x.name == i.name, ctx.guild.voice_channels)

                await victim_member.move_to(channel)

                time.sleep(75*0.01)

                print(f' [nologging_noformatting] [exc] { victim_member } transferred to { i.name }')

        await victim_member.edit(mute = False, deafen = False)
        await ctx.send(f'{victim_member} **Экскурсия по {ctx.guild.name} окончена. Надеюсь, Вы впечатлены**')

    @bot.command()
    async def kick(ctx, victim):
        """Kick victim:str of voice channel"""
        
        victim_member = get(ctx.guild.members, name = victim)
        channelU = discord.utils.find(lambda x: x.name == 'PIDARASI VI SUKI', ctx.guild.voice_channels)
        await victim_member.move_to(channelU)
        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def list(ctx):
        """List of guild members"""         
        
        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")

        emb = discord.Embed (title = f'Список участников сервера {ctx.guild.name} :clipboard: ')
        emb.description = str(len(ctx.guild.members)) + ' ' + 'участника(-ов):'
        for i in ctx.guild.members:
            if i.nick == None:
                emb.add_field(name = i.name, value = i.roles[len(i.roles) - 1])
            else:
                emb.add_field(name = i.nick, value = i.roles[len(i.roles) - 1])
        await ctx.send ( embed = emb )

    @bot.command()
    async def list_ch(ctx):
        """List of guild voice channels"""
        
        for i in ctx.guild.voice_channels:
            LogManager.info(i.name)
        await ctx.send(str(len(ctx.guild.voice_channels)) + ' каналов на сервере')
        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")

    @bot.command()
    async def bye(ctx):
        """User leave the chat for long time"""

        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")

        await ctx.channel.purge(limit = 1)
        em = bot.get_emoji(725371922291884032)
        await ctx.send(f'{ctx.message.author.mention} Ушел на покой{str(em)}')

    @bot.command()
    async def tr(ctx, victim, channel):
        """Transfer victim:str for channel:str"""
        
        victim_member = get(ctx.guild.members, name = victim)
        channelU = discord.utils.find(lambda x: x.name == channel, ctx.guild.voice_channels)
        try:
            await victim_member.move_to(channelU)
            LogManager.info(f'[tr] { victim_member } was transfered to { channelU }')
        except:
            pass
            LogManager.info(f'[tr] Transfer { victim_member } failed')

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def lat(ctx, victim:str):
        """All time lock victim:str"""                                  
        if ctx.message.author.name == "SharapaGorg":
            await ctx.channel.purge(limit = 1)
            global n
            n = True
            author = ctx.message.author
            
            victim_member = discord.utils.get(ctx.guild.members, name=victim)
            
            mem = await ctx.guild.fetch_member(victim_member.id)

            while n == True: 
            
                if mem != None:                 
                    await mem.edit(mute = True, deafen = True)
                    time.sleep(0.75)
                    LogManager.info(f'[{author.id}] lock {victim_member}')                  
                    try:                                                                                                    
                        await mem.edit(nick = '_PIDARAS_')
                    except:                                                                     
                        pass
                else:
                    time.sleep(0.75)
        else:
            await ctx.send("Not enough permissions")

    @bot.command()
    @commands.has_permissions(administrator = True)
    async def ulat(ctx, victim):
        """All unlock victim:str"""

        await ctx.channel.purge(limit = 1)
        global n 
        n = False
        victim_member = discord.utils.get(ctx.guild.members, name=victim)
        await victim_member.edit(mute = False, deafen = False)
        LogManager.info(f'[{ ctx.guild }] unlock  { victim_member }')
        try:
            await victim_member.edit(nick = victim)
        except:
            pass

    @bot.command()
    async def send(ctx, victim):

        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
        
        author = ctx.message.author
        if str(author.id) == '691575600707534908':
            victim_member = get(ctx.guild.members, name = victim)
            await ctx.send(victim_member)

    @bot.command()
    async def _test_(ctx, victim):
        """Check member for existence"""

        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
        
        victim_member = get(ctx.guild.members, name = victim)
        if victim_member == None:
            await ctx.send('Кто это???')
        else:
            await ctx.send(f'{ victim_member.id } существует')



    class RaidCommands:
        @bot.command()
        @commands.has_permissions(administrator = True)
        async def kickall(ctx):

            LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
            
            await ctx.channel.purge(limit = 1)
            await ctx.send(f'~~**...Машины уничтожаеют сервер :skull:...**~~'), LogManager.info(f'[warning] Бот {bot.user.name} кикнул всех, кого мог')

            for m in ctx.guild.members:
                try:
                    await m.kick(reason="Облегченный рейд на сервер успешно проведен.")
                except:
                    pass

        @bot.command()
        @commands.has_permissions(administrator = True)
        async def banall(ctx):

            LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
            
            await ctx.channel.purge(limit = 1)
            await ctx.send(f'~~**...Машины уничтожаеют сервер :skull:...**~~'), LogManager.info(f'[warning] Бот {bot.user.name} забанил всех, кого мог')

            for m in ctx.guild.members:
                try:
                    await m.ban(reason="Рейд на сервер успешно проведен.")
                except:
                    pass

        @bot.command()
        @commands.has_permissions(administrator = True)
        async def dl(ctx):

            LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
            
            await ctx.channel.purge(limit = 1), LogManager.info(f'[warning] {bot.user.name} Удалил столько ролей, сколько смог')

            for m in ctx.guild.roles:
                try:
                    await m.delete(reason="Плановое обнуление")
                except:
                    pass

        @bot.command()
        @commands.has_permissions(administrator = True)
        async def dch(ctx):

            LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")
            
            failed = []
            counter = 0
            await ctx.channel.purge(limit = 1)
            for channel in ctx.guild.channels:
                try:
                    await channel.delete(reason="Рейд успешно проведен.")
                except: failed.append(channel.name)
                else: counter += 1
            fmt = ", ".join(failed)

            LogManager.info(f'[warning] Рейд по удалению каналов прошел довольно успешно ({bot.user.name})')

    @bot.command()
    async def _help_(ctx, cat):
        """_help_ Category:str >> command $j"""                     

        LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")

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
        async def j(ctx):
            """Unfinished custom help command"""

            LogManager.info(f"[{ctx.message.guild.name}] {ctx.message.author.name} called {sys._getframe().f_code.co_name}")

            emb = discord.Embed(title = "Categories of commands:", colour = discord.Color.dark_red())
            emb.add_field(value = '```$_help_ Name_of_category```', name = '```Example:$_help_ Report```')
            emb.description = f'•Flex{bot.get_emoji(725037390011433091)}\n•Admin{bot.get_emoji(725437920390938725)}\n•Random{bot.get_emoji(724945422665383946)}\n•Information{bot.get_emoji(725060275849658458)}'
            emb.set_image(url = 'https://i.gifer.com/fyrY.gif')
            await ctx.send (embed = emb)

    @COVID.NewConfirmed.error
    @COVID.NewDeaths.error
    @COVID.TotalConfirmed.error
    @COVID.TotalDeaths.error
    @Aloshya.SdProtect.error
    @Aloshya.SoundOpen.error
    @Aloshya.SdClose.error
    @Aloshya.loh.error
    @GlobalGuild.AllNick.error
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
    @te.error
    @spam.error
    async def custom_error(ctx,error):
        em = str(bot.get_emoji(725437920390938725))
        author = ctx.message.author
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention}, обязательно укажите аргумент!')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{author.mention}, вы не обладаете такими правами!')
        if isinstance(error, commands.errors.CommandInvokeError):
            LogManager.error_log(error)
            await ctx.send(f"```{error}```")


    #@bot.command(pass_context = True)
    #async def _help_(ctx):
        
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
        #LogManager.info(f'[help] ${bot.user.name} sent a help list for {ctx.message.author.name} ({ctx.message.author.nick})')

        #await ctx.send ( embed = emb )

    import ctypes

    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7) 

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
        
        if input(" \033[36m ----------------- [1/0] ----------------- : ") == '1':

            LogManager.debug("<<<^^^ Toxic bg connected ^^^>>>")

            while True:
                os.system("color FC")
                os.system("color EC")
                os.system("color AC")
                os.system("color CF")
                os.system("color 9C")
                os.system("color DC")
                os.system("color 8C")

        else:
            LogManager.debug("<<<^^^ Standart bg connected ^^^>>>")

    #=================================================

    bot.run(settings['TOKEN'])

except Exception as e:
    LogManager.warning('Work status: 0')

    LogManager.error(e)

finally:
    LogManager.info('Well done :)')
    

#ShGbot for discord channel
#https://discord.com/developers/applications/721846899984039969/information 
