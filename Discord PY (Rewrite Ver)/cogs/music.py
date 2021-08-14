import discord
import youtube_dl
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Music is ready.\n\nLogged messages and errors:")

    # Commands
    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel.")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
            await ctx.send(f"Joined `{voice_channel}`.")
        else:
            await ctx.send("Already in a voice channel.")

    @commands.command()
    async def leave(self, ctx):
        
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel.")

        elif ctx.voice_client is None:
            await ctx.send("I'm not in any voice channel.")

        if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
            voice_channel = ctx.author.voice.channel
            await ctx.voice_client.disconnect()
            await ctx.send(f"Disconnected from `{voice_channel}`.")
        else:
            await ctx.send("You're in a different voice channel!")
        

    @commands.command()
    async def play(self, ctx, url: str):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel.")

        elif ctx.voice_client is None:
            await ctx.send("I'm not in any voice channel, specify a channel for me to join.")
            return

        if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
            ctx.voice_client.stop()

            await ctx.send("Getting the requested song, please wait...")

            FFMPEG_OPTIONS = {
                "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                "options": "-vn"
            }

            YDL_OPTIONS = {"formats": "bestaudio"}
            vc = ctx.voice_client

            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                url2 = info["formats"][0]["url"]
                src = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)

                vc.play(src)

                await ctx.send(f"Playing {url}")
        else:
            await ctx.send("You're in a different voice channel!")


    @commands.command()
    async def pause(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel.")

        elif ctx.voice_client is None:
            await ctx.send("I'm not in any voice channel.")

        if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
            if not ctx.voice_client.is_paused():
                await ctx.channel.send("Paused.")
                ctx.voice_client.pause()
                return
            elif not ctx.voice_client.is_playing():
                await ctx.channel.send("Currently no audio is playing.")
                return
            elif ctx.voice_client.is_paused():
                await ctx.channel.send("Already paused.")
        else:
            await ctx.send("You're in a different voice channel!")

    @commands.command()
    async def resume(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel.")

        elif ctx.voice_client is None:
            await ctx.send("I'm not in any voice channel.")

        if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
            if ctx.voice_client.is_paused():
                await ctx.channel.send("Resumed.")  
                ctx.voice_client.resume()
                return
            elif not ctx.voice_client.is_playing():
                await ctx.channel.send("Currently no audio is playing.")
                return
            elif not ctx.voice_client.is_paused():
                await ctx.channel.send("The audio is not paused yet.")
        else:
            await ctx.send("You're in a different voice channel!")

    

    # ERROR HANDLERS
    @play.error
    async def play_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please pass in a URL in order to play a song.")

def setup(client):
    client.add_cog(Music(client))