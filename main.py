#! /usr/bin/env python
# -*- coding: utf-8 -*- // 


# Надо для работы в линуксе русских символов
import sys
sys.path.insert(1, '/home/linaro/')
from t import BOT_TOKEN

import discord
import asyncio
import pyttsx3
import os
import random
from time import time


WORDS = {"соси" : [None, "Sam sosi XD"],

         "пенетрайшн" : ["8 differet Penetrationsounds.wav", ""],
         "анал" : ["Anal.wav", ""],
         "сее" : ["Do you like what you see.mp3", ""],
         "данжн" : ["Dungeon master.mp3", ""],
         "300" : ["Fisting is 300.mp3", ""],
         "фак" : ["FUCK YOU.wav", ""],
         "слейвс" : ["Fuckin Slaves.wav", ""],
         "дееп" : ["It's so fucking deep.mp3", ""],
         "камм" : ["Make me cum.wav", ""],
         "сори" : ["Oh Shit Im Sorry.wav", ""],
         "фор" : ["Sorry for what.wav", ""],
         "каминг" : ["Ooouuuuh Im fucking cumming.wav", ""],
         "фингер" : ["Stick your finger.mp3", ""],
         "сволов" : ["Swallow my cum.mp3", ""],
         "бой" : ["Take it boy.mp3", ""],

        "suck" : [None, "Sam sosi XD"],
}

MESSAGE = 745396711794409593

CHANNEL = 745394748147105843

EMOTIONS = {
'🎶' : "8 differet Penetrationsounds.wav",
'⭕' : "Anal.wav",
'👀' : "Do you like what you see.mp3",
'⛰️' : "Dungeon master.mp3",
'✊' : "Fisting is 300.mp3",
'📣' : "FUCK YOU.wav",
'⛓️' : "Fuckin Slaves.wav",
'🥖' : "It's so fucking deep.mp3",
'😳' : "Make me cum.wav",
'😰' : "Oh Shit Im Sorry.wav",
'😏' : "Sorry for what.wav",
'🎆' : "Ooouuuuh Im fucking cumming.wav",
'👍' : "Stick your finger.mp3",
'🥛' : "Swallow my cum.mp3",
'🤝' : "Take it boy.mp3",
'🔀' : "RANDOM",
'🔇' : "OFF",
}

MAIN_PATH = "/home/linaro/botDiscordGachi/sounds/"

class MyClient(discord.Client):

    async def on_ready(self):
        self.voice_channel_list = []
        self.current_channel = None
        self.voice = None
        self.is_on = True

        for guild in self.guilds:
            for channel in guild.voice_channels:
                if channel.id != 734866467128082475:
                    self.voice_channel_list.append(channel) # Беру список всех голосовых каналов кроме афк и записываю в переменную
        # print(voice_channel_list)

        await self.ch_reactions()

        print('Logged on as {0}!'.format(self.user.display_name))
        await self.check() # Запускаю выполнение функции проверки

    async def random(self):
        random.seed(time())
        rn = random.choice(list(EMOTIONS.values()))
        if rn != "RANDOM" and rn != "OFF":
            await self.play_sound(rn, "sound")
        else:
            await self.random()


    async def ch_reactions(self):
        channel = client.get_channel(CHANNEL)
        msg = await channel.fetch_message(MESSAGE)
        if len(msg.reactions)!=len(EMOTIONS):
            for r in msg.reactions:
                await r.clear()
            for key in EMOTIONS:
                await msg.add_reaction(key)

    async def check(self): # Функция проверки
        
        while self.current_channel == None: # Пока бот не зашел не в один канал
            if self.is_on:
                for ch in reversed(self.voice_channel_list): # идем по списку каналов в обратном порядке, чтобы главной был первым
                    if ch.members: # Если в канале есть люди
                        await self.conn(ch) # Вызываем функцию подключения
                        print(f"connected to -> {ch.name}")
            await asyncio.sleep(2) # Ждем 2 секунды

    async def conn(self, ch): # Функция подключения
            vc = await ch.connect() 
            self.voice = vc
            self.current_channel = ch # Подключаемся к каналу
            while self.current_channel != None: # Пока подключены
                if len(ch.members) > 1 and self.is_on: # 
                    await asyncio.sleep(2)
                else:
                    await self.voice.disconnect()
                    await asyncio.sleep(2)
                    self.voice = None
                    self.current_channel = None
                    await self.check()

    async def play_sound(self, content, typ):
        if self.voice != None:
            if typ == "sound":
                # print(f"{MAIN_PATH}{content}")
                self.voice.play(discord.FFmpegPCMAudio(source=f"{MAIN_PATH}{content}"))
                while self.voice.is_playing():
                    await asyncio.sleep(.1)   
        else:
            await self.check()
            print("Bot not in voice room")
                
    async def on_message(self, message):
        if message.author != self.user:
            for key in WORDS:
                if key in message.content.lower():
                    i = 0
                    for item in WORDS[key]:
                        if i == 0:
                            if item != None:
                                if self.current_channel != None:
                                    await self.play_sound(item, "sound")
                        # else:
                             # await message.channel.send(item)
                        i+=1
        if message.channel.id == CHANNEL:
            await message.delete(delay=5)  


    async def on_raw_reaction_add(self, payload):
        if payload.message_id == MESSAGE:
            sound = EMOTIONS[str(payload.emoji)]
            if sound == "RANDOM":
                await self.random()
            elif sound == "OFF":
                pass
            else:
                await self.play_sound(sound, "sound")

    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == MESSAGE:
            sound = EMOTIONS[str(payload.emoji)]
            if sound == "RANDOM":
                await self.random()
            elif sound == "OFF":
                pass
            else:
                await self.play_sound(sound, "sound")

client = MyClient()
token = BOT_TOKEN
client.run(str(token))

