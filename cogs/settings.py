import discord
import json
import asyncio
from discord.ext import commands

class Settings(commands.Cog):  # <-- time converter for tempban command
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
	async def clear(self, context, amount=5): # <-- clear message command
		await context.channel.purge(limit=amount+1) 
		await context.send(f'Cleared {amount} message(s).')
		await asyncio.sleep(3)
		await context.channel.purge(limit=1)
	
	@commands.command()
	@commands.has_permissions(manage_messages=True)
	async def mute(self, context, Member : commands.MemberConverter, *, reason=None):  # <-- mute command
		guild = context.guild
		mutedRole = discord.utils.get(guild.roles, name='Muted')

		if not mutedRole:
			mutedRole = await guild.create_role(name='Muted')

			for channel in guild.channels:
				await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)

		await Member.add_roles(mutedRole, reason=reason)
		await context.send(f'Muted {Member}\nReason: {reason}')
		await Member.send(f'You were muted in {guild.name}\nReason: {reason}')

	@commands.command()
	@commands.has_permissions(manage_messages=True)
	async def unmute(self, context, Member : commands.MemberConverter):  # <--unmute command
		mutedRole = discord.utils.get(context.guild.roles, name='Muted')

		await Member.remove_roles(mutedRole)
		await context.send(f'Unmuted {Member}')
		await Member.send(f"You were unmuted in {guild.name}")
		
	@commands.command()
	@commands.has_permissions(kick_members=True)
	async def kick(self, context, Member : commands.MemberConverter, *, reason=None):  # <-- kick command
		await Member.kick(reason=reason)
		await context.send(f'{Member} has been kicked.')

	@commands.command()
	@commands.has_permissions(kick_members=True, ban_members=True)
	async def tempban(self, context, Member : commands.MemberConverter, duration: DurationConverter):  # <-- tempban command
		multiplier = {'s': 1, 'm': 60, 'h': '3600'}
		amount, unit = duration

		await context.guild.ban(Member)
		await context.send(f'{Member} has been temporarily banned for {amount}{unit}.')
		await asyncio.sleep(amount * multiplier[unit])
		await context.guild.unban(Member)
		
	@commands.command()
	@commands.has_permissions(kick_members=True, ban_members=True)
	async def unban(self, context, *, member):			# <-- unban command
		banned_users = await context.guild.bans()
		member_name, member_discriminator = member.split('@')

		for ban_entry in banned_users:
			user = ban_entry.username

			if (user.name, user.discriminator) == (member_name, member_discriminator):
				await context.guild.unban(user)
				await context.send(f'{user.name}#{user.discriminator} has been unbanned.')
				return
	
	@commands.command()
	@commands.has_permissions(kick_members=True,ban_members=True)
	async def ban(self, context, Member : commands.MemberConverter, *, reason=None):  # <-- ban command
		await Member.ban(reason=reason)
		await context.send(f'{Member} has been banned.')
		 
	@commands.command(aliases=['prefixSet', 'setPrefix'])
	@commands.has_permissions(administrator=True)
	async def change_prefix(self, context, prefix):  # <-- set prefix command
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)

		prefixes[str(context.guild.id)] = prefix

		with open('prefixes.json', 'w') as f:
			json.dump(prefixes, f, indent=4)
	
	# Error handling stuff
	@kick.error
	async def kick_error(self, context, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await context.send('Please specify a user to kick.')  # <-- this line will excute when users don't specify a user to kick
		if isinstance(error, commands.MissingPermissions):
			await context.send(f"You don't have permissions to run this command.") # <-- this line will execute when users don't have permission to access this command
		if isinstance(error, commands.BotMissingPermissions):
			await context.send(f"I don't have the required permission, please give me administrator permission in order to run this command.")  # <-- this line will execute when the users don't give permissions to this bot
  	# the same thing goes to other commands
	
	@ban.error
	async def ban_error(self, context, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await context.send('Please specify a user to ban.')
		if isinstance(error, commands.MissingPermissions):
			await context.send(f"You don't have permissions to run this command.")
		if isinstance(error, commands.BotMissingPermissions):
			await context.send(f"I don't have the required permission, please give me administrator permission in order to run this command.")

	@unban.error
	async def unban_error(self, context, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await context.send('Please specify a user to unban.')
		if isinstance(error, commands.MissingPermissions):
			await context.send(f"You don't have permissions to run this command.")
		if isinstance(error, commands.BotMissingPermissions):
			await context.send(f"I don't have the required permission, please give me administrator permission in order to run this command.")

	@tempban.error
	async def tempban_error(self, context, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await context.send('Please specify a user to tempban.')
		if isinstance(error, commands.MissingPermissions):
			await context.send(f"You don't have permissions to run this command.")
		if isinstance(error, commands.BotMissingPermissions):
			await context.send(f"I don't have the required permission, please give me administrator permission in order to run this command.")

	@clear.error
	async def clear_error(self, context, error):
		if isinstance(error, commands.MissingPermissions):
			await context.send("You don't have permissions to run this command.")
		if isinstance(error, commands.BotMissingPermissions):
			await context.send("I don't have the required permission, please give me administrator permission in order to run this command.")

	@mute.error
	async def clear_error(self, context, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await context.send('Please specify a user to mute.')
		if isinstance(error, commands.MissingPermissions):
			await context.send("You don't have permissions to run this command.")
		if isinstance(error, commands.BotMissingPermissions):
			await context.send("I don't have the required permission, please give me administrator permission in order to run this command.")

	@unmute.error
	async def clear_error(self, context, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await context.send('Please specify a user to unmute.')
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
