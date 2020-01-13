defmodule Bowser.Discord.Nostrum do
  @behaviour Bowser.Discord
  @moduledoc "Wrapper of nostrum library"

  @impl Bowser.Discord
  def send_message(channel_id, msg) do
    Nostrum.Api.create_message!(channel_id, msg)
  end

  @impl Bowser.Discord
  def get_guild_by_id(guild_id) do
    Nostrum.Cache.GuildCache.get!(guild_id)
  end

  @impl Bowser.Discord
  def get_permissions_of_member(member, guild, channel_id) do
    Nostrum.Struct.Guild.Member.guild_channel_permissions(member, guild, channel_id)
  end
end
