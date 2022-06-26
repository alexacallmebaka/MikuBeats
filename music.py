from nextcord import slash_command, Interaction, FFmpegPCMAudio
from nextcord.ext import commands
from queue import Queue
from yt_dlp import YoutubeDL


class Beats(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot
        self.queue = Queue()
        self.ytdl=YoutubeDL({"quiet":True})
        self.voice=None
    
    async def _connect_voice(self, channel) -> None:
        self.voice = await channel.connect()

    def _create_source(self, url: str) -> FFmpegPCMAudio:
        song = self.ytdl.extract_info(url=url, download=False)
        return FFmpegPCMAudio(song['formats'][6]['url'])

    @slash_command(name="play", description="Play music using YouTube links.")
    async def play(self, inter: Interaction, url: str) -> None:
        
        if inter.user.voice == None:
           await inter.response.send_message("You are not in a voice channel!")
        else:
            self.queue.put(self._create_source(url))

            if self.voice == None or self.voice.is_connected() == False:
                await self._connect_voice(inter.user.voice.channel)
        
        #TODO: Check link validty/throw error when link bad.
        #If is playing is false, then call another function to enter play loop.
        #Command to view code

    async def loop(self, inter: Interaction) -> None:
        self.voice.play(self.queue.get())

        #commands for: pause, skip, disconnect
