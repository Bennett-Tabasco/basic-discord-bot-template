from json import load
from os import getcwd

jsonPath = f"{getcwd()}\\extensions\\client-data\\prefixes.json"

def get_guilds_id():
    with open(jsonPath, "r") as f:
        guildsId = load(f)

    arrGuildsId = [int(GuildId) for GuildId, ServerInfo in guildsId["guilds"].items()]

    return arrGuildsId

    