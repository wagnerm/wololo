import discord
import pytest

from wololo import Wololo


class TestCommand:
    def setup(self):
        self.w = Wololo()

    def test_commands_registered(self):
        assert 1 == len(self.w.commands)

    def test_help(self):
        help = self.w.help()
        assert help == """Command help:
    `wololo` - Try me"""

    def test_wololo(self):
        ctx = discord.ext.commands.Context(
            "wololo",
            None,
            [],
        )
        self.w.wololo()
