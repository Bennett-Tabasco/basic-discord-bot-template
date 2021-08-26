from extensions.utils.Tools import *
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option

class Moderation_Slash(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation-Slash is ready.")
        
    # I'm lazy :P

def setup(client):
    client.add_cog(Moderation_Slash(client))
