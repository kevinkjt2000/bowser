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
    status_re = re.compile('^players \d+/\d+$')
    mc = Minecraft(test_server=fake_minecraft_server)
    status_message = mc.get_formatted_status_message()
    assert status_re.match(status_message) is not None


status_modded_online = PingResponse({
    'description': {'text': 'fake description', },
    'modinfo': {'modList': [
        {'modid': 'FML', 'version': '8.0.99.99'},
        {'modid': 'forge', 'version': '14.22.0.2460'},
    ], },
    'players': {'online': 1, 'max': 8, 'sample': [{
        'id': '291b495c-b03b-46bb-b2c8-e31ad4cdef44',
        'name': 'fake_name',
    }, ], },
    'version': {'name': 'fake_name', 'protocol': 316, },
})


@patch('src.Minecraft.MinecraftServer')
def test__forge_version_message_matches_modid_forge_version(fake):
    fake.status.return_value = status_modded_online
    mc = Minecraft(test_server=fake)
    forge_message = mc.get_forge_version_message()
    assert forge_message == 'Forge is at version 14.22.0.2460'


@patch('src.Minecraft.MinecraftServer')
def test__can_fetch_modded_server_status(fake_minecraft_server):
    fake_minecraft_server.status.return_value = status_modded_online
    status_re = re.compile('^\d+ mods loaded, players \d+/\d+: `(.*(, )?)*`$')
    mc = Minecraft(test_server=fake_minecraft_server)
    status_message = mc.get_formatted_status_message()
    assert status_re.match(status_message) is not None
