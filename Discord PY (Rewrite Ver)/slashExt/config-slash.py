import json
from extensions.utils.Tools import *
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option


class Config_Slash(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Slash Commands Extensions:\n\nSlash Config is ready.")

    @cog_ext.cog_slash(name="ping", description="Shows client's latency.", guild_ids=get_guilds_id())
    async def ping(self, ctx:SlashContext):
        await ctx.send(f"Pong! {round(self.client.latency * 1000)}ms")

    @cog_ext.cog_slash(
        name="clear", 
        description="Delete an amount of specified message(s).", 
        guild_ids=get_guilds_id(),
        options=[
                create_option(
                    name="amount",
                    description="Amount of message(s) to delete.",
                    required=False,
                    option_type=4
                )
            ]
    )
    async def clear(self, ctx:SlashContext, amount=5):
        if amount > 100:
            await ctx.send("Amount of message(s) to delete must be smaller than 100.")
            return
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f"Deleted {amount} message(s).")

    @cog_ext.cog_slash(
        name = "prefixSet",
        description = "Set new custom server's prefix.",
        guild_ids = get_guilds_id(),
        options = [
		create_option (
		    name="prefix",
		    description='New custom prefix.',
		    required=True,
		    option_type=3
        	)
	]
    )
    async def prefixSet(self, ctx: SlashContext, prefix):
        valid_prefix = ['!', '@', '#', '$', '%', '^', '&', '*','-', '_', '+', '=', '~', '>', '<', '.', ',', '?', '\\', '`', '|', '/']
        if prefix not in valid_prefix:
            await ctx.send('That is not a valid prefix!')
            return
        if prefix in valid_prefix:
            with open(jsonPath, 'r') as f:
                prefixes = json.load(f)

            prefixes["guilds"][str(ctx.guild.id)] = {}
            prefixes["guilds"][str(ctx.guild.id)]["name"] = ctx.guild.name
            prefixes["guilds"][str(ctx.guild.id)]["prefix"] = prefix

            with open(jsonPath, 'w') as f:
                json.dump(prefixes, f, indent=4)
                await ctx.send(f'**Prefix changed to** `{prefix}`')

def setup(client):
	client.add_cog(Config_Slash(client))
