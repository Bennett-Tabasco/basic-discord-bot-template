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

	# Commands
	@commands.command()
	async def ping(self, context):
		await context.send(f'Pong! {round(self.client.latency * 1000)}ms')
	
	@commands.command()
	@commands.has_permissions(manage_messages=True)
	async def clear(self, context, amount=5): # <-- clear message command
		await context.channel.purge(limit=amount+1) 
		await context.send(f'Cleared {amount} message(s).')
		await asyncio.sleep(3)
		await context.channel.purge(limit=1)
	
	#new version
	@commands.command(aliases=['prefixSet']) 
	@commands.has_permissions(administrator=True)
	async def change_prefix(self, context, prefix):
		valid_prefix = ['!', '@', '#', '$', '%', '^', '&', '*','-', '_', '+', '=', '~', '>', '<', '.', ',', '(', ')', '[', ']', '{', '}', '?', '\\', '`', '|', '/']
		if prefix not in valid_prefix: #if they don't give a valid prefix, also the list above contains valid prefixes
			await context.send('That is not a valid prefix!')
			return #the bot won't change the prefix if it's invalid
		if prefix in valid_prefix: #if they give a valid prefix
			with open('prefixes.json', 'r') as f:
				prefixes = json.load(f)

			prefixes[str(context.guild.id)] = prefix

			with open('prefixes.json', 'w') as f:
				json.dump(prefixes, f, indent=4)
			await context.send(f'**Prefix changed to** `{prefix}`')
	
	#old version
	#@commands.command(aliases=['prefixSet', 'setPrefix'])
	#@commands.has_permissions(administrator=True)
	#async def change_prefix(self, context, prefix):  # <-- set prefix command
	#	with open('prefixes.json', 'r') as f:
	#		prefixes = json.load(f)

	#	prefixes[str(context.guild.id)] = prefix

	#	with open('prefixes.json', 'w') as f:
	#		json.dump(prefixes, f, indent=4)
	#	await context.send(f'**Prefix set to** `{prefix}`')
	
	
	@clear.error
	async def clear_error(self, context, error):
		if isinstance(error, commands.MissingPermissions):
			await context.send("You don't have permissions to run this command.")
		if isinstance(error, commands.BotMissingPermissions):
			await context.send("I don't have the required permission, please give me administrator permission in order to run this command.")

def setup(client):
	client.add_cog(Settings(client))

'''
about 'commands.has_permission()'
check out more here: https://www.youtube.com/watch?v=imH1PCzCWP0
permissions: https://discordpy.readthedocs.io/en/stable/api.html?highlight=permissions#discord.Permissions
'''
