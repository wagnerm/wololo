#!/usr/bin/env python

import discord
from dotenv import load_dotenv
import os
import re
import traceback

load_dotenv()

intents = discord.Intents(
    message_content=True,
    messages=True,
    voice_states=True,
    guilds=True,
)

TOKEN = os.getenv("DISCORD_TOKEN")
AUDIO_ROOT_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "audio")


class BaseCommand(object):
    def __init__(self, name):
        self.name = name
        self.commands = []

    def register(self, name, regex, func):
        self.commands.append({
            "name": name,
            "regex": regex,
            "func": func,
        })

    async def handle_message(self, message, message_content):
        if message_content:
            return await self.process_chat(message, message_content)

    async def process_chat(self, message, message_content):
        for command in self.commands:
            if len(command["regex"]) != 0:
                match = re.compile(command["regex"]).match(message_content)
                if match is None:
                    print("Match is none")
                    continue

                func = command["func"]
                return await func(message, message_content)

        return None


class DiscordConnectionFailure(Exception):
    pass


class AudioCommand(object):
    async def connect(self, voice_channel):
        try:
            return await voice_channel.connect(reconnect=False, timeout=2)
        except discord.errors.ClientException:
            # Already connected, attempt to attain VoiceClient
            return voice_channel.guild.voice_client

        raise DiscordConnectionFailure("VoiceClient cannot be attained!")

    async def play_in_channel(self, message, audio_source):
        author_voice_state = message.author.voice
        if author_voice_state == None:
            print(f"{message.author} not in voice channel, skipping")
            return

        voice_client = await self.connect(author_voice_state.channel)

        if voice_client.is_playing():
            voice_client.stop()

        voice_client.play(audio_source)


class Wololo(BaseCommand, AudioCommand):
    def __init__(self):
        super(Wololo, self).__init__("wololo")
        self.register(None, ".*wololo.*", self.wololo)

    async def wololo(self, message, message_content):
        audio_source = discord.FFmpegPCMAudio(
            os.path.join(AUDIO_ROOT_PATH, "wololo/wololo.wav"))
        return await self.play_in_channel(message, audio_source)


class Bot(discord.Client):
    def __init__(self, intents):
        super(Bot, self).__init__(intents=intents)
        self.handlers = [
            Wololo(),
        ]

    async def on_ready(self):
        print("Bot has connected to Discord!")

    async def on_message(self, message):
        try:
            for handler in self.handlers:
                response = await handler.handle_message(message, message.content)
                if response is not None:
                    await message.channel.send(response)
                    break
                else:
                    pass
        except Exception as e:
            print("Error: {} {}".format(e, e.__traceback__))
            print(traceback.format_exc())


chat = Bot(intents)
chat.run(TOKEN)
