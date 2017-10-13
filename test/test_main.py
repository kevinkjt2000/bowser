from unittest.mock import MagicMock, patch
import asyncio
import discord
import random
import unittest


class TestMain(unittest.TestCase):
    @patch('src.main.main')
    def test__init_calls_main_once(self, mock_main):
        import src.main
        with patch.object(src.main, '__name__', '__main__'):
            src.main.init()
            mock_main.assert_called_once_with()


def async_test(f):
    def wrapper(*args, **kwargs):
        coro = asyncio.coroutine(f)
        future = coro(*args, **kwargs)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)
    return wrapper


class TestBot(unittest.TestCase):
    def setUp(self):
        import src.main
        self.bot = MagicMock(
            spec=src.main.Bot,
            user=_get_mock_user(bot=True),
        )
        self.mock_run = asynctest.patch.object(self.bot, 'run')
        self.mock_run.start()

    def tearDown(self):
        self.mock_run.stop()

    def test__sends_error_message_when_connection_refused(self):
        with patch.object(
                self.bot.mc, 'get_formatted_status_message') as mock_mc:
            mock_mc.side_effect = ConnectionRefusedError
            mock_message = _get_mock_message('!status')
            with asynctest.patch.object(self.bot, 'send_message') as mock_send:
                with asynctest.patch.object(self.bot, 'on_command_error') as \
                        mock_on_error:
                    yield from self.bot.on_message(mock_message)
                    mock_mc.assert_called_once()
                    mock_on_error.assert_called_once()
                    mock_send.assert_called_once_with(mock_message)


def _get_mock_message(content):
    return MagicMock(
        spec=discord.Message,
        author=_get_mock_user(),
        channel=MagicMock(spec=discord.Channel),
        content=content,
        mentions=[],
    )


def _get_mock_user(bot=None):
    return MagicMock(
        spec=discord.User,
        id=random.randrange(999999),
        name='mock_user',
        bot=bot,
    )
