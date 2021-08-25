import discord
import youtube_dl
from extensions.utils.Tools import *
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option

class Music_Slash(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music-Slash is ready.")

    @cog_ext.cog_slash(
        name="join",
        description="Join the voice channel of whom invoked the command.",
        guild_ids=get_guilds_id(),
    )
    async def join(self, ctx:SlashContext):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel.")
            return
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
            await ctx.send(f"Joined `{voice_channel}`.")
            return
        else:
            await ctx.send("Already in a voice channel.")
            return

    @cog_ext.cog_slash(
        name='leave',
        description="Disconnect from the current voice channel.",
        guild_ids=get_guilds_id()
    )
    async def leave(self, ctx:SlashContext):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel.")
            return

        elif ctx.voice_client is None:
            await ctx.send("I'm not in any voice channel.")
            return

        if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
            voice_channel = ctx.author.voice.channel
            await ctx.voice_client.disconnect()
            await ctx.send(f"Disconnected from `{voice_channel}`.")
            return
        else:
            await ctx.send("You're in a different voice channel!")
            return

    @cog_ext.cog_slash(
        name="play",
        description="Play a song using a specifed YouTube URL.",
        guild_ids=get_guilds_id(),
        options=[
            create_option(
                name="url",
                description="The YouTube URL to play the song.",
                required=True,
                option_type=3
            )
        ]
    )
    async def play(self, ctx:SlashContext, url):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel.")
            return

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
            return

    @cog_ext.cog_slash(
        name="pause",
        description="Pause the current track.",
        guild_ids=get_guilds_id()
    )
    async def pause(self, ctx:SlashContext):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel.")
            return

        elif ctx.voice_client is None:
            await ctx.send("I'm not in any voice channel.")
            return

        if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
            if ctx.voice_client.is_paused():
                await ctx.channel.send("Already paused.")
                return
            elif not ctx.voice_client.is_playing():
                await ctx.channel.send("Currently no audio is playing.")
                return
            elif not ctx.voice_client.is_paused():
                await ctx.channel.send("Paused.")
                ctx.voice_client.pause()
                return
           
        else:
            await ctx.send("You're in a different voice channel!")
            return

    @cog_ext.cog_slash(
        name="resume",
        description="Continue playing the song.",
        guild_ids=get_guilds_id()
    )
    async def resume(self, ctx:SlashContext):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel.")
            return

        elif ctx.voice_client is None:
            await ctx.send("I'm not in any voice channel.")
            return

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
                return
        else:
            await ctx.send("You're in a different voice channel!")
            return

def setup(client):
    client.add_cog(Music_Slash(client))
    