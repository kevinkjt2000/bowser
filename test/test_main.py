from mcstatus.pinger import PingResponse
from unittest.mock import patch
from src.Minecraft import Minecraft
import re


@patch('src.Minecraft.MinecraftServer')
def test__can_display_server_status_from_vanilla_server(fake_minecraft_server):
    status_vanilla_empty = PingResponse({
        'description': {'text': 'Minecraft is awesome!', },
        'players': {'online': 0, 'max': 8, },
        'version': {'name': '1.12.1', 'protocol': 338, },
    })
    fake_minecraft_server.status.return_value = status_vanilla_empty
    status_re = re.compile('players \d+/\d+: (.*(, )?)*')
    mc = Minecraft(test_server=fake_minecraft_server)
    status_message = mc.get_formatted_status_message()
    assert status_re.match(status_message) is not None


@patch('src.Minecraft.MinecraftServer')
def test__can_fetch_modded_server_status(fake_minecraft_server):
    status_modded_empty = PingResponse({
        'description': {'text': 'fake description', },
        'modinfo': {'modList': [], },
        'players': {'online': 0, 'max': 8, },
        'version': {'name': 'fake name', 'protocol': 316, },
    })
    fake_minecraft_server.status.return_value = status_modded_empty
    status_re = re.compile('\d+ mods loaded, players \d+/\d+: (.*(, )?)*')
    mc = Minecraft(test_server=fake_minecraft_server)
    status_message = mc.get_formatted_status_message()
    assert status_re.match(status_message) is not None
