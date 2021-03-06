defmodule Protocols.Minecraft do
  @moduledoc "Minecraft server protocol handler"

  alias Protocols.ProtocolError

  defp remove_ascii_escape_codes(str) do
    Regex.replace(~r/§[0-9a-z]/, str, "")
  end

  def get_forge_version(host, port \\ 25_565) do
    info = get_info_object!(host, port)

    try do
      [forge] = info["modinfo"]["modList"] |> Enum.filter(&(&1["modid"] == "forge"))
      "Forge is at version `#{forge["version"]}`."
    rescue
      _ ->
        "`#{host}:#{port}` does not have forge installed."
    end
  end

  def get_motd(host, port \\ 25_565) do
    info = get_info_object!(host, port)
    "`#{remove_ascii_escape_codes(info["description"]["text"])}`"
  end

  def get_status_message(host, port \\ 25_565) do
    info = get_info_object!(host, port)

    if Map.has_key?(info, "modinfo") do
      "#{length(info["modinfo"]["modList"])} mods loaded, "
    else
      ""
    end <>
      "players #{info["players"]["online"]}/#{info["players"]["max"]}" <>
      if info["players"]["online"] > 0 and info["players"]["sample"] do
        ": `" <> (info["players"]["sample"] |> Enum.map(& &1["name"]) |> Enum.join(", ")) <> "`"
      else
        ""
      end
  end

  defp get_info_object!(host, port) do
    mc_info =
      try do
        MCPing.get_info(host, port)
      rescue
        MatchError ->
          reraise ProtocolError, message: "The server seems to be running too old of a version."
      end

    case mc_info do
      {:ok, info} ->
        info

      {:error, :nxdomain} ->
        raise ProtocolError, message: "Unable to contact `#{host}`."

      {:error, :econnrefused} ->
        raise ProtocolError, message: "`#{host}` refused the connection to port #{port}."

      {:error, :timeout} ->
        raise ProtocolError, message: "Connection to `#{host}` timed out."

      {:error, err} ->
        raise "Failed to get server info for #{host}:#{port} (#{err})"
    end
  end
end
