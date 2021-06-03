import discord
import random
import json
from discord.ext import commands, tasks

class Entertaining_Stuff(commands.Cog):
	def __init__(self, client):
		self.client = client
	# Event
	@commands.Cog.listener()
	async def on_ready(self):
		print('\nEntertaining stuff is ready.')
	# Commands

	@commands.command(aliases=['HelloWorld'])
	async def hello_world(self, context):
		await context.send('>>> hello world')

	#@commands.command()
	#async def rollDice(self, context, *, first_num, second_num):		<--- still in work
	#	await context.send(random.randint(first_num,second_num))

	@commands.command(aliases=['8ball'])
	async def _8ball(self, context, *, question):
		responses = [
		"It is certain.",
		"It is decidedly so.",
		"Without a doubt.",
		"Yes - definitely.",
		"You may rely on it.",
		"As I see it, yes.",
		"Most likely.",
		"Outlook good.",
		"Yes.",
		"Signs point to yes.",
		"Reply hazy, try again.",
		"Ask again later.",
		"Better not tell you now.",
		"Cannot predict now.",
		"Concentrate and ask again.",
		"Don't count on it.",
		"My reply is no.",
		"My sources say no.",
		"Outlook not so good.",
		"Very doubtful."]
		await context.send(f'Question: {question}\n Answer: {random.choice(responses)}')


def setup(client):
	client.add_cog(Entertaining_Stuff(client))
