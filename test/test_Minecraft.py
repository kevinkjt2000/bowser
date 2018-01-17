from mcstatus.pinger import PingResponse
from unittest import TestCase
from unittest.mock import patch, mock_open, MagicMock
from bowser.Minecraft import Minecraft
from types import SimpleNamespace
import re

status_vanilla_empty = PingResponse({
    'description': {'text': ''},
    'players': {'online': 0, 'max': 8},
    'version': {'name': '1.12.1', 'protocol': 338},
})

status_modded_online = PingResponse({
    'description': {
        'text': '§9§k||§bStuff§9§k||§r §7Whitelist:§r §2Offline✔§r\n§6Stuff',
    },
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


status_modded_online_old = PingResponse({
    'version': {'name': 'BungeeCord 1.8.x-1.12.x', 'protocol': 47},
    'players': {'max': 9001, 'online': 2},
    'description': {
        'extra': [
            {'color': 'dark_blue', 'text': 'TR Lobby'},
            {'color': 'aqua', 'obfuscated': True, 'text': '|!|!|'},
            {'color': 'aqua', 'underlined': True, 'text': 'TR HUB'},
        ],
        'text': '',
    },
    'modinfo': {'type': 'FML', 'modList': []}
})

status_modded_really_old = PingResponse({
    'description': 'Infamous Gaming - GTNH',
    'players': {'max': 20, 'online': 0, 'sample': []},
    'version': {'name': '1.7.10', 'protocol': 5},
})


class TestMinecraft(TestCase):
    def setup_class(self):
        self.mc = Minecraft(MinecraftServer=MagicMock)
        self.context = SimpleNamespace(
            message=SimpleNamespace(
                server=SimpleNamespace(id=42),
                channel=SimpleNamespace(id=5),
            )
        )

    @patch('builtins.open', new_callable=mock_open, read_data="{}")
    def test__get_mc_object_raises_key_error_for_empty_json(self, mock_open):
        with self.assertRaises(KeyError):
            Minecraft.get_minecraft_object_for_server_channel(self.context)

    @patch('builtins.open', new_callable=mock_open,
           read_data="""{"42": {"5": {"host": "fake_host", "port": 1234}}}""")
    def test__get_minecraft_object_can_read_host_and_port(self, mock_open):
        mc = Minecraft.get_minecraft_object_for_server_channel(self.context)
        assert mc.mc_server.host == "fake_host"
        assert mc.mc_server.port == 1234

    def test__really_old_protocol_empty_motds_are_supported(self):
        self.mc.mc_server.status.return_value = status_modded_really_old
        motd = self.mc.get_motd()
        assert motd == 'There is no MOTD :('

    def test__old_protocol_motds_are_supported(self):
        self.mc.mc_server.status.return_value = status_modded_online_old
        motd = self.mc.get_motd()
        assert motd == '`TR Lobby|!|!|TR HUB`'

    def test__handles_empty_motds(self):
        self.mc.mc_server.status.return_value = status_vanilla_empty
        motd = self.mc.get_motd()
        assert motd == 'There is no MOTD :('

    def test__removes_ansi_escapes_from_motd(self):
        self.mc.mc_server.status.return_value = status_modded_online
        motd = self.mc.get_motd()
        assert motd == '`||Stuff|| Whitelist: Offline✔\nStuff`'

    def test__can_handle_old_protocols_without_players_sample(self):
        self._modded_test(status_modded_online_old)

    def test__can_display_server_status_from_vanilla_server(self):
        status_re = re.compile(r'^players \d+/\d+$')
        self.mc.mc_server.status.return_value = status_vanilla_empty
        status_message = self.mc.get_formatted_status_message()
        assert status_re.match(status_message) is not None

    def test__forge_version_is_not_installed_on_vanilla(self):
        self.mc.mc_server.status.return_value = status_vanilla_empty
        forge_message = self.mc.get_forge_version_message()
        assert forge_message == 'The server does not have Forge installed.'

    def test__forge_version_message_matches_modid_forge_version(self):
        self.mc.mc_server.status.return_value = status_modded_online
        forge_message = self.mc.get_forge_version_message()
        assert forge_message == 'Forge is at version 14.22.0.2460'

    def test__can_fetch_modded_server_status(self):
        self._modded_test(status_modded_online)

    def _modded_test(self, status_dict):
        status_re = re.compile(
            r'^\d+ mods loaded, players \d+/\d+: `(.*(, )?)*`$'
        )
        self.mc.mc_server.status.return_value = status_dict
        status_message = self.mc.get_formatted_status_message()
        assert status_re.match(status_message) is not None
