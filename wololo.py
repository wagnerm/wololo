import discord
import os
import re
import traceback

TOKEN = os.getenv("DISCORD_TOKEN")
BOT_ID = os.getenv("BOT_ID")

client = discord.Client()


class BaseCommand(object):
    def __init__(self, name):
        self.name = name
        self.commands = []

    def register(self, name, regex, help, func):
        self.commands.append({
            "name": name,
            "regex": regex,
            "help": help,
            "func": func,
        })

    def help(self, indent=4):
        message_indent = " " * indent
        message = [
            'Command help:',
        ]
        for command in self.commands:
            if command["name"] is None:
                message.append(
                    "{}`{}` - {}".format(message_indent, self.name, command["help"]))
            else:
                message.append("{}`{} {}` - {}".format(
                    message_indent, self.name, command["name"], command["help"]))

        return "\n".join(message)

    async def handle_message(self, message, message_content):
        if message_content:
            print(message_content)
            return await self.process_chat(message, message_content)

    async def process_chat(self, message, message_content):
        for command in self.commands:
            if len(command["regex"]) != 0:
                match = re.compile(command["regex"]).match(message_content)
                if match is None:
                    print("Match is none")
                    continue

                func = command["func"]
                return func(message, message_content)

        return None


class Wololo(BaseCommand):
    def __init__(self):
        super(Wololo, self).__init__("wololo")
        self.register(None, ".*wololo.*", "Try me", self.wololo)

    def wololo(self, message, message_content):
        return "WOLOLO"


class Bot(discord.Client):
    def __init__(self):
        super(Bot, self).__init__()
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


chat = Bot()
chat.run(TOKEN)
