import discord
import os
import json
from discord.ext import commands, tasks
from itertools import cycle
from dotenv import load_dotenv

# Path to file that stores bot's token
tokenPath = "./extensions/client-data/.env"
# Path to file that stores server's prefix
jsonPath = "./extensions/client-data/prefixes.json"

load_dotenv(dotenv_path=tokenPath)

# Activity and Status
activity = cycle(["with TemplateBot!", "Python 3.9.5", ".help", "Hello, World!"])
status = cycle([discord.Status.idle, discord.Status.online, discord.Status.do_not_disturb, discord.Status.online])
# Changing the status every specified amount of time
time = 10


def get_prefix(client, message):
	with open(jsonPath ,'r') as f:
		prefixes = json.load(f)

	return prefixes["guilds"][message.guild.name]["prefix"]

client = commands.Bot(command_prefix=get_prefix)
client.remove_command('help') 

@client.event
async def on_ready():
	changeActivity.start()
	print("\nClient's status:\n\nBot is ready.")

	#-- Load all server's info that the client is in, write it to the json file if the client possesses none of it
	with open(jsonPath, 'r') as database:
		joinedGuilds = json.load(database)

		for guild in client.guilds:
			if not guild.name in joinedGuilds["guilds"]:
				joinedGuilds["guilds"][guild.name] = {}

				joinedGuilds["guilds"][guild.name]["id"] = guild.id
				joinedGuilds["guilds"][guild.name]["prefix"] = "."

				with open(jsonPath, 'w') as database:
					json.dump(joinedGuilds, database, indent=4)
					
# Change this as you like
@tasks.loop(seconds=time)
async def changeActivity():
	await client.change_presence(activity=discord.Game(next(activity)), status=next(status))


#-- 
@client.event
async def on_guild_join(guild):
	with open(jsonPath, 'r') as f:
		prefixes = json.load(f)

	prefixes["guilds"][guild.name] = {}

	prefixes["guilds"][guild.name]["id"] = guild.id
	prefixes["guilds"][guild.name]["prefix"] = "."

	with open(jsonPath, 'w') as f:
		json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
	with open(jsonPath, 'r') as f:
		prefixes = json.load(f)

	prefixes["guilds"].pop(guild.name)

	with open(jsonPath, 'w') as f:
		json.dump(prefixes, f, indent=4)
#--


#-- Load and unload cogs commands
@client.command()
@commands.has_permissions(manage_messages=True)
async def load(ctx, extension):
	client.load_extension(f'cogs.{extension}')
	await ctx.send(f"Loaded `cogs.{extension}`")

@client.command()
@commands.has_permissions(manage_messages=True)
async def unload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')
	await ctx.send(f"Unloaded `cogs.{extension}`")



@client.command()
@commands.has_permissions(manage_messages=True)
async def loadAll(ctx):
	for filename in os.listdir('./cogs'):
		if filename.endswith('.py'):
			client.load_extension(f'cogs.{filename[:-3]}')
	await ctx.send("Loaded all extensions.")

@client.command()
@commands.has_permissions(manage_messages=True)
async def unloadAll(ctx):
	for filename in os.listdir('./cogs'):
		if filename.endswith('.py'):
			client.unload_extension(f'cogs.{filename[:-3]}')
	await ctx.send("Unloaded all extensions.")

# Load all cogs when booting up
for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')
#--


	
client.run(os.getenv("TOKEN"))
