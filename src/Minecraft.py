from mcstatus import MinecraftServer


class Minecraft:
    def __init__(self, host='msb2.mynode.in', port=25565,
                 MinecraftServer=MinecraftServer):
        self.mc_server = MinecraftServer(host=host, port=port)

    def get_forge_version_message(self):
        status = self.mc_server.status()
        forge = None
        if 'modinfo' in status.raw:
            forge = next(filter(lambda mod: mod['modid'] == 'forge',
                                status.raw['modinfo']['modList']), None)
        if forge:
            return 'Forge is at version {}'.format(forge['version'])
        else:
            return 'The server does not have Forge installed'

    def get_formatted_status_message(self):
        status = self.mc_server.status()
        if status.players.online > 0:
            online_players = ': `' + ', '.join(
                [p.name for p in status.players.sample]) + '`'
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
