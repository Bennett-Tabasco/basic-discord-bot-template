import discord
from discord.ext import commands

class Help(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(aliases=['help', 'HELP'])
	async def Help(self, ctx):	
		embed=discord.Embed(title=":robot: TemplateBot" ,description= f"A list of commands if you don't know the commands.")
		embed.add_field(name="Entertain", value="Check out these commands if you're bored.", inline=False)
		embed.add_field(name="Config", value="List out bot's configuration commands.", inline=False)
		embed.add_field(name="Moderation", value="Provides basic moderation commands.", inline=False)
		embed.add_field(name="Music", value="Voice commands for playing music.", inline=False)

		await ctx.send(embed=embed)

	@commands.command(aliases=['helpSettings', 'helpSetting', "helpConfig", "helpConfiguration" , "Config"])
	async def help_settings(self, ctx):
		embed=discord.Embed(title='Configurations')
		embed.add_field(name="prefixSet", value="Set the old prefix to a new one.", inline=False)
		embed.add_field(name="ping", value="Show bot's latency", inline=False)
		embed.add_field(name="clear", value="Clear messages with a specific amount (Default is 5, Manage messages permission required).", inline=False)

		await ctx.send(embed=embed)

	@commands.command(aliases=['helpEntertain', "Entertain"])
	async def help_entertain(self, ctx):
		embed=discord.Embed(title='Entertaining stuff')

		embed.add_field(name="8ball", value="Ask this bot something and it will answer your question", inline=False)
		embed.add_field(name="HelloWorld", value="Print out 'hello world'", inline=False)

		await ctx.send(embed=embed)

	@commands.command(aliases=['helpSecurity', "helpModeration", "Moderation"])
	async def help_security(self, ctx):
		embed=discord.Embed(title='Moderation')

		embed.add_field(name="mute", value="`<prefix>mute <user> <reason>`", inline=False)
		embed.add_field(name="unmute", value="`<prefix>unmute <user>`", inline=False)
		embed.add_field(name="kick", value="`<prefix>kick <user> <reason>`", inline=False)
		embed.add_field(name="ban", value="`<prefix>ban <user> <reason>`", inline=False)
		embed.add_field(name="unban", value="`<prefix>unban <user: name#discriminator>`", inline=False)
		embed.add_field(name="tempban", value="`<prefix>tempban <user> <duration: (Length)(Unit: \"s\", \"m\", \"h\")> <reason>`", inline=False)

		await ctx.send(embed=embed)

	@commands.command(aliases=['helpMusic', "Music"])
	async def help_voice(self, ctx):
		embed=discord.Embed(title='Music')

		embed.add_field(name='join', value='Join the channel of whom invoked the command.', inline=False)
		embed.add_field(name='leave', value='Leave the voice channel.', inline=False)
		embed.add_field(name='play', value='Play a song from a given URL.', inline=False)
		embed.add_field(name='pause', value='Pause the current track.', inline=False)
		embed.add_field(name='resume', value='Continue playing the song.', inline=False)


		await ctx.send(embed=embed)

def setup(client):
	client.add_cog(Help(client))