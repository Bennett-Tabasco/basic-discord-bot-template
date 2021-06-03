import discord
import json
import asyncio
from discord.ext import commands

class Settings(commands.Cog):
	def __init__(self, client):
		self.client = client

	class DurationConverter(commands.Converter):
		async def convert(self, context, arg):
			amount = arg[:-1]
			unit = arg[-1]
			if amount.isdigit() and unit in ['s', 'm', 'h']:
				return (int(amount), unit)

			raise commands.BadArgument(message='Not a valid duration.')

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
	async def clear(self, context, amount=5):
		await context.channel.purge(limit=amount)
		await context.send(f'Cleared {amount} message(s).')
		await asyncio.sleep(3)
		await context.channel.purge(limit=1)

	@commands.command()
	@commands.has_permissions(kick_members=True)
	async def kick(self, context, Member : commands.MemberConverter, *, reason=None):
		await Member.kick(reason=reason)
		await context.send(f'{Member} has been kicked.')

	@commands.command()
	@commands.has_permissions(kick_members=True, ban_members=True)
	async def tempban(self, context, Member : commands.MemberConverter, duration: DurationConverter):
		multiplier = {'s': 1, 'm': 60, 'h': '3600'}
		amount, unit = duration

		await context.guild.ban(Member)
		await context.send(f'{Member} has been temporarily banned for {amount}{unit}.')
		await asyncio.sleep(amount * multiplier[unit])
		await context.guild.unban(Member)
	
	@commands.command()
	@commands.has_permissions(kick_members=True,ban_members=True)
	async def ban(self, context, Member : commands.MemberConverter, *, reason=None):
		await Member.ban(reason=reason)
		await context.send(f'{Member} has been banned.')
		 
	@commands.command(aliases=['prefixSet', 'setPrefix'])
	@commands.has_permissions(administrator=True)
	async def change_prefix(self, context, prefix):
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)

		prefixes[str(context.guild.id)] = prefix

		with open('prefixes.json', 'w') as f:
			json.dump(prefixes, f, indent=4)

def setup(client):
	client.add_cog(Settings(client))