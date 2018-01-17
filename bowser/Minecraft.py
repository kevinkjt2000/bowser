from mcstatus import MinecraftServer
import json
import re


class Minecraft:
    def __init__(self, host='msb2.mynode.in', port=25565,
                 MinecraftServer=MinecraftServer):
        self.mc_server = MinecraftServer(host=host, port=port)

    def get_motd(self):
        status = self.mc_server.status()
        try:
            motd = status.description['text']
        except TypeError:
            return 'There is no MOTD :('
        if 'extra' in status.description:
            motd += ''.join([x['text'] for x in status.description['extra']])
        ansi_escape = re.compile(r'§[0-9a-z]')
        motd = ansi_escape.sub('', motd)
        if motd:
            return f'`{motd}`'
        return 'There is no MOTD :('

    def get_forge_version_message(self):
        status = self.mc_server.status()
        forge = None
        if 'modinfo' in status.raw:
            forge = next(filter(lambda mod: mod['modid'] == 'forge',
                                status.raw['modinfo']['modList']), None)
        if forge:
            return 'Forge is at version {}'.format(forge['version'])
        else:
            return 'The server does not have Forge installed.'

    def get_formatted_status_message(self):
        status = self.mc_server.status()
        if status.players.online > 0:
            sample = status.raw['players'].get('sample', [])
            online_players = ': `' + ', '.join(
                [p['name'] for p in sample]) + '`'
        else:
            online_players = ''
        online_count = status.players.online
        max_count = status.players.max
        status_message = ''
        if 'modinfo' in status.raw:
            mods_count = len(status.raw['modinfo']['modList'])
            status_message += '{} mods loaded, '.format(mods_count)
        status_message += 'players {}/{}{}'.format(
            online_count, max_count, online_players)
        return status_message

    @staticmethod
    def get_minecraft_object_for_server_channel(context):
        sid = str(context.message.server.id)
        cid = str(context.message.channel.id)
        minecrafts = {}
        with open('servers.json') as json_data:
            minecrafts = json.load(json_data)
        m = minecrafts[sid][cid]
        return Minecraft(host=m['host'], port=m['port'])
