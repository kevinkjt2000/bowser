from mcstatus.pinger import PingResponse
from unittest.mock import patch
from src.main import get_formatted_status_message
import re


@patch('src.main.MinecraftServer')
def test__can_fetch_good_server_status(fake_minecraft_server):
    good_status = PingResponse({
        'description': 'fake description',
        'modinfo': {
            'modList': [],
        },
        'players': {
            'online': 0,
            'max': 0,
            'sample': [],
        },
        'version': {
            'name': 'fake name',
            'protocol': 316,
        },
    })
    fake_minecraft_server.status.return_value = good_status
    status_re = re.compile('\d+ mods loaded, players \d+/\d+: (.*(, )?)*')
    status_message = get_formatted_status_message(fake_minecraft_server)
    assert status_re.match(status_message) is not None
