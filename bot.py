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
client.remove_command('help') # remove the current help command and replace it with a new one (check help_commands.py file)

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

#this will handle 'command not found' error
@client.event
async def on_command_error(context, error):
	if isinstance(error, commands.CommandNotFound):
		await context.send("Command doesn't exist, try again.")


client.run('') # bot's token here (make sure that you don't show your token to anyone)
