import discord
import json
import asyncio
from discord.ext import commands

class Settings(commands.Cog):
	def __init__(self, client):
		self.client = client

	# Event
	@commands.Cog.listener()
	async def on_ready(self):
		print('Settings is ready.')

	#def is_tak(self, context):
	#	return context.author.id == 724541596976283649

	# Commands
	@commands.command()
	async def ping(self, context):
		await context.send(f'Pong! {round(self.client.latency * 1000)}ms')

	#@commands.command()
	#@commands.check(is_tak)
	#async def kick(self, context, member : discord.Member, *, reason=None):
	#	await member.kick(reason=reason)
	
	#@commands.command()
	#@commands.check(is_tak)
	#async def kick(self, context, member : discord.Member, *, reason=None):
	#	await member.ban(reason=reason)
	
	@commands.command()
	#@commands.check(is_tak)
	async def clear(self, context, amount=5):
		await context.channel.purge(limit=amount)
		await context.send(f'Cleared {amount} message(s).')
		await asyncio.sleep(3)
		await context.channel.purge(limit=1)

	@commands.command(aliases=['prefixSet', 'setPrefix'])
	#@commands.check(is_tak)
	async def change_prefix(self, context, prefix):
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)

		prefixes[str(context.guild.id)] = prefix

		with open('prefixes.json', 'w') as f:
			json.dump(prefixes, f, indent=4)

def setup(client):
	client.add_cog(Settings(client))