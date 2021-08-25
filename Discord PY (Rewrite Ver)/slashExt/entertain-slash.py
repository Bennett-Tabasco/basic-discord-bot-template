from discord.ext import commands
from random import randrange
from extensions.utils.Tools import *
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option

class Entertain_Slash(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Entertain-Slash is ready.")

    @cog_ext.cog_slash(name="8ball", 
    description="Ask the bot something and the bot will answer your question.",
    guild_ids=get_guilds_id(),
    options=[
        create_option(
            name="question",
            description="Question to ask.",
            option_type=3,
            required=True
        )
        ]
    )

    async def _8ball(self, ctx:SlashContext, question):
        responses = [
		"It is certain.",
		"It is decidedly so.",
		"Without a doubt.",
		"Yes - definitely.",
		"You may rely on it.",
		"As I see it, yes.",
		"Most likely."
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
        await ctx.send(f"Question: {question}\nAnswer: {responses[randrange(0, len(responses)-1)]}")

def setup(client):
    client.add_cog(Entertain_Slash(client))