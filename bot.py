import discord
import os
import json
from discord.ext import commands, tasks
activity = discord.Game(name="with TemplateBot.")
# getting prefix on the current server
def get_prefix(client, message):
		with open('prefixes.json' ,'r') as f:
			prefixes = json.load(f)

		return prefixes[str(message.guild.id)]
client = commands.Bot(command_prefix=get_prefix, activity=activity, status=discord.Status.idle)
client.remove_command('help') # remove the current help command and replace it with a new one (check line 51)
# load and set prefix
@client.event
async def on_guild_join(guild):
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)

	prefixes[str(guild.id)] = '%'

	with open('prefixes.json', 'w') as f:
		json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)

	prefixes.pop(str(guild.id))

	with open('prefixes.json', 'w') as f:
		json.dump(prefixes, f, indent=4)
#--

# load and unload cogs
@client.command()
async def load(context, extension):
	client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(context, extension):
	client.unload_extension(f'cogs.{extension}')


for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')
#--

# custom help command using embeds (check out more here https://python.plainenglish.io/send-an-embed-with-a-discord-bot-in-python-61d34c711046)
@client.command(aliases=['help', 'HELP'])
async def Help(context):	
	embed=discord.Embed(title="TemplateBot" ,description= f"A list of commands if you don't know the commands (Default prefix is '%')", color=discord.Color.blue())
	embed.add_field(name="Entertaining stuff.", value="Check out these commands if you're bored.", inline=False)
	embed.add_field(name="8ball", value="Ask this bot something and it will answer your question", inline=True)
	embed.add_field(name="HelloWorld", value="Print out 'hello world'", inline=True)

	embed.add_field(name="Settings", value="Used to setting some stuff.", inline=False)
	embed.add_field(name="kick", value="Kick someone out of server (Administrator permission required).", inline=True)
	embed.add_field(name="ban", value="Ban someone out of server (Administrator permission required).", inline=True)
	embed.add_field(name="tempban", value="Temp ban someone out of server (Administrator permission required).", inline=True)
	embed.add_field(name="unban", value="Used to unban someone (Administrator permission required).", inline=True)
	embed.add_field(name="prefixSet", value="Set the old prefix to a new one.", inline=True)
	embed.add_field(name="ping", value="Checking for ping.", inline=True)
	embed.add_field(name="clear", value="Clear messages with a specific amount (Default is 5, Manage messages permission required).", inline=True)

	await context.send(embed=embed)

# Error handling stuff
@client.event
async def on_command_error(context, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await context.send("Missing required argument, try again.")


client.run('') # bot's token here (make sure that you don't show your token to anyone)
