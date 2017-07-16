from mcstatus.pinger import PingResponse
from unittest.mock import patch
from src.Minecraft import Minecraft
import re


@patch('src.Minecraft.MinecraftServer')
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
    mc = Minecraft(test_server=fake_minecraft_server)
    status_message = mc.get_formatted_status_message()
    assert status_re.match(status_message) is not None
