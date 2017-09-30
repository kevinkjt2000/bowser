from src.main import Bot
import asynctest
import discord
import unittest.mock


class TestMain(asynctest.TestCase):
    def setUp(self):
        self.bot = Bot()
        self.bot.user = unittest.mock.MagicMock(
            spec=discord.User,
            id=42,
            name='mock_name',
            bot=self.bot,
        )
        self.mock_run = unittest.mock.patch('discord.Client.run')
        self.mock_run.start()

    def tearDown(self):
        self.mock_run.stop()

    async def test__it_works(self):
        # await self.bot.on_ready()
        assert 1 == 1
