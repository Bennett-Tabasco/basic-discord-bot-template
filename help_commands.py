import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    # new help command using embeds (check out more in here https://python.plainenglish.io/send-an-embed-with-a-discord-bot-in-python-61d34c711046)
    @commands.command(aliases=['help', 'HELP'])
    async def Help(self, context):	
	    embed=discord.Embed(title=":robot: TemplateBot" ,description= f"A list of commands if you don't know the commands (Default prefix is '%')")
	    embed.add_field(name="helpEntertain", value="Check out these commands if you're bored.", inline=False)
	    embed.add_field(name="helpSettings", value="Used to setting some stuff.", inline=False)
	    embed.add_field(name="helpSecurity", value="These commands are mostly for server's mods and admins.", inline=False)
	    embed.add_field(name="helpVoice", value="Vibe to the music mate.", inline=False)

	    await context.send(embed=embed)

    @commands.command(aliases=['helpSettings', 'helpSetting'])
    async def help_settings(self, context):
	    embed=discord.Embed(title='Settings')
	    embed.add_field(name="prefixSet", value="Set the old prefix to a new one.", inline=False)
	    embed.add_field(name="ping", value="Show bot's latency", inline=False)
	    embed.add_field(name="clear", value="Clear messages with a specific amount (Default is 5, Manage messages permission required).", inline=False)

	    await context.send(embed=embed)

    @commands.command(aliases=['helpEntertain'])
    async def help_entertain(self, context):
	    embed=discord.Embed(title='Entertaining stuff')

	    embed.add_field(name="8ball", value="Ask this bot something and it will answer your question", inline=False)
	    embed.add_field(name="HelloWorld", value="Print out 'hello world'", inline=False)

	    await context.send(embed=embed)

    @commands.command(aliases=['helpSecurity'])
    async def help_security(self, context):
	    embed=discord.Embed(title='Security')

	    embed.add_field(name="mute", value="Used to mute someone", inline=False)
	    embed.add_field(name="unmute", value="Used to unmute someone", inline=False)
	    embed.add_field(name="kick", value="Kick someone out of server (Administrator permission required).", inline=False)
	    embed.add_field(name="ban", value="Ban someone out of server (Administrator permission required).", inline=False)
	    embed.add_field(name="tempban", value="Temp ban someone out of server (Administrator permission required).", inline=False)

	    await context.send(embed=embed)

    @commands.command(aliases=['helpVoice'])
    async def help_voice(self, context):
	    embed=discord.Embed(title='Voice Chat')

	    embed.add_field(name='coming soon!', value='blah blah blah', inline=True)

	    await context.send(embed=embed)

def setup(client):
    client.add_cog(Help(client))
