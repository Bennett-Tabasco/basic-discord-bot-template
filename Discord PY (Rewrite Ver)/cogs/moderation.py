import discord
import asyncio
from discord.ext import commands

class Security(commands.Cog):
	def __init__(self, client):
		self.client = client

	class DurationConverter(commands.Converter): 
		async def convert(self, ctx, arg):
			amount = arg[:-1]
			unit = arg[-1]
			if amount.isdigit() and unit in ['s', 'm', 'h']:
				return (int(amount), unit)

			raise commands.BadArgument(message='Not a valid duration.')
    
	# Events
	@commands.Cog.listener()
	async def on_ready(self):
		print('Moderation is ready.')

	# Commands
	@commands.command()
	@commands.has_permissions(manage_messages=True)
	async def mute(self, ctx, Member : commands.MemberConverter, *, reason=None):
		if ctx.message.author == Member:
			await ctx.send("You can't mute yourself!")
			return
		
		guild = ctx.guild
		mutedRole = discord.utils.get(guild.roles, name='Muted')

		if not mutedRole:
			mutedRole = await guild.create_role(name='Muted')

			for channel in guild.channels:
				await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)

		await Member.add_roles(mutedRole, reason=reason)
		await ctx.send(f'Muted {Member}\nReason: {reason}')
		await Member.send(f'You were muted in {guild.name}\nReason: {reason}')

	@commands.command()
	@commands.has_permissions(manage_messages=True)
	async def unmute(self, ctx, Member : commands.MemberConverter):
		if ctx.message.author == Member:
			await ctx.send("You can't unmute yourself!")
			return

		mutedRole = discord.utils.get(ctx.guild.roles, name='Muted')

		await Member.remove_roles(mutedRole)
		await ctx.send(f'Unmuted {Member}')
		await Member.send(f"You were unmuted in {ctx.guild.name}.")

	@commands.command()
	@commands.has_permissions(kick_members=True) 
	async def kick(self, ctx, Member : commands.MemberConverter, *, reason=None):
		if ctx.message.author == Member:
			await ctx.send("You can't kick yourself!")
			return
		
		await Member.kick(reason=reason)
		await ctx.send(f'{Member} has been kicked\nReason: {reason}.')
		await Member.send(f'You were kicked in {ctx.guild.name}\nReason: {reason}')

	@commands.command()
	@commands.has_permissions(kick_members=True, ban_members=True,)  
	async def tempban(self, ctx, Member : commands.MemberConverter, duration: DurationConverter, *, reason=None):
		if ctx.message.author == Member:
			await ctx.send("You can't temporarily ban yourself!")
			return
		
		multiplier = {'s': 1, 'm': 60, 'h': 3600}
		amount, unit = duration

		await Member.ban(reason=reason)
		await ctx.send(f'{Member.mention} has been temporarily banned for {amount}{unit}\nReason: {reason}')
		await asyncio.sleep(amount * multiplier[unit])
		await ctx.guild.unban(Member)

	@commands.command()
	@commands.has_permissions(kick_members=True, ban_members=True)
	async def unban(self, ctx, *, member):
		banned_users = await ctx.guild.bans()
		member_name, member_discriminator = member.split('#')

		for ban_entry in banned_users:
			user = ban_entry.user

			if (user.name, user.discriminator) == (member_name, member_discriminator):
				await ctx.guild.unban(user)
				await ctx.send(f'{user.name}#{user.discriminator} has been unbanned.')
				return
		else:
			await ctx.send("Member not found.")		
	
	# Error Handlers
	@commands.command()
	@commands.has_permissions(kick_members=True,ban_members=True)
	async def ban(self, ctx, Member : commands.MemberConverter, *, reason=None):
		if ctx.message.author == Member:
			await ctx.send("You can't ban yourself!")
			return
		
		guild = ctx.guild
		await Member.ban(reason=reason)
		await ctx.send(f'{Member} has been banned\nReason: {reason}.')
		await Member.send(f'You were banned in {guild.name}\nReason: {reason}')



	# ERRORS HANDLERS
	@kick.error
	async def kick_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('Please fill in the required arguments.') 
		if isinstance(error, commands.MissingPermissions):
			await ctx.send(f"You don't have permissions to run this command.") 
		if isinstance(error, commands.BotMissingPermissions):
			await ctx.send(f"I don't have the required permission, please give me administrator permission in order to run this command.")  
	

	@ban.error
	async def ban_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('Please fill in the required arguments.')
		if isinstance(error, commands.MissingPermissions):
			await ctx.send(f"You don't have permissions to run this command.")
		if isinstance(error, commands.BotMissingPermissions):
			await ctx.send(f"I don't have the required permission, please give me administrator permission in order to run this command.")

	@unban.error
	async def unban_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('Please fill in the required arguments.')
		if isinstance(error, commands.MissingPermissions):
			await ctx.send(f"You don't have permissions to run this command.")
		if isinstance(error, commands.BotMissingPermissions):
			await ctx.send(f"I don't have the required permission, please give me administrator permission in order to run this command.")

	@tempban.error
	async def tempban_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('Please fill in the required arguments.')
		if isinstance(error, commands.MissingPermissions):
			await ctx.send(f"You don't have permissions to run this command.")
		if isinstance(error, commands.BotMissingPermissions):
			await ctx.send(f"I don't have the required permission, please give me administrator permission in order to run this command.")

	@mute.error
	async def mute_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('Please fill in the required arguments.')
		if isinstance(error, commands.MissingPermissions):
			await ctx.send(f"You don't have permissions to run this command.")
		if isinstance(error, commands.BotMissingPermissions):
			await ctx.send(f"I don't have the required permission, please give me administrator permission in order to run this command.")

	@unmute.error
	async def unmute_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('Please fill in the required arguments.')
		if isinstance(error, commands.MissingPermissions):
			await ctx.send(f"You don't have permissions to run this command.")
		if isinstance(error, commands.BotMissingPermissions):
			await ctx.send(f"I don't have the required permission, please give me administrator permission in order to run this command.")


def setup(client):
	client.add_cog(Security(client))
