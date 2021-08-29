import discord
import json
import asyncio
import os
from discord.ext import commands

# Path to JSON file
jsonPath = f"{os.getcwd()}\\extensions\\client-data\\prefixes.json"

class Configuration(commands.Cog): 
	def __init__(self, client):
		self.client = client

	# Event
	@commands.Cog.listener()
	async def on_ready(self):
		print('Settings is ready.')

	# Commands
	@commands.command()
	async def ping(self, ctx):
		await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')
	
	@commands.command()
	@commands.has_permissions(manage_messages=True)
	async def clear(self, ctx, amount=5):
		if amount > 150:
			await ctx.send("Amount of messages to delete must be smaller than 150")
			return
		
		await ctx.channel.purge(limit=amount+1) 
		await ctx.send(f'Cleared {amount} message(s).')
		await asyncio.sleep(3)
		await ctx.channel.purge(limit=1)
	

	@commands.command(aliases=['prefixSet']) 
	@commands.has_permissions(administrator=True)
	async def change_prefix(self, ctx, prefix):
		valid_prefix = ['!', '@', '#', '$', '%', '^', '&', '*','-', '_', '+', '=', '~', '>', '<', '.', ',', '?', '\\', '`', '|', '/'] # allowed character for the new prefix
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
	
	# Error Handlers
	@clear.error
	async def clear_error(self, ctx, error):
		if isinstance(error, commands.MissingPermissions):
			await ctx.send("You don't have permissions to run this command.")
		elif isinstance(error, commands.BotMissingPermissions):
			await ctx.send("I don't have the required permission, please give me administrator permission in order to run this command.")
			
	@change_prefix.error
	async def change_prefix_error(self, ctx, error):
		if isinstance(error, commands.MissingPermissions):
			await ctx.send("You don't have permissions to run this command.")
		elif isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("Please specify a character for a new prefix.")

def setup(client):
	client.add_cog(Configuration(client))

