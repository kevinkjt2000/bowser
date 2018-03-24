from unittest.mock import patch, mock_open
import unittest
import asynctest
import bowser.main


class TestMain(unittest.TestCase):
    @patch('bowser.main.main')
    def test__init_calls_main_once(self, mock_main):
        with patch.object(bowser.main, '__name__', '__main__'):
            bowser.main.init()
            mock_main.assert_called_once_with()

    @patch('time.sleep')
    @asynctest.patch('bowser.main.Bot.run')
    @patch('builtins.open', new_callable=mock_open, read_data='mock_token')
    def test__main_keeps_running_until_something_bad_happens(
            self, mock_open, mock_bot_run, mock_sleep):
        mock_bot_run.side_effect = [
            ConnectionResetError,
            ConnectionResetError,
            ConnectionResetError,
            Exception,
        ]
        self.assertRaises(Exception, bowser.main.main)
        assert mock_bot_run.call_count == 4

    @patch('bowser.main.Bot.run')
    @patch('builtins.open', new_callable=mock_open, read_data='mock_token')
    def test__main_starts_the_bot(self, mock_open, mock_bot_run):
        bowser.main.main()
        mock_bot_run.assert_called_once_with('mock_token')
