from nextcord import slash_command, Interaction, FFmpegPCMAudio, VoiceClient, VoiceChannel
from nextcord.ext import commands
from collections import deque
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

#Simple object to store data about a song.
class Song:

    def __init__(self,source: FFmpegPCMAudio,name: str) -> None:
        self.name = name
        self.source = source

#Handles song queue, as well as player state.
#Use a deque here for performance reasons, also I'm lazy and don't want to write my own queue right now.
class Player:
    def __init__(self,voice_client: VoiceClient) -> None:
        self.queue = deque()
        self.current_song = None
        self.vc = voice_client
   
    #The player "loop", which plays songs from the queue one-by-one.
    #The error parameter is required for loop to be usable with "play" later on.
    async def loop(self,error=None) -> None:
        #Exit if no more music or Miku is the only one in the channel.
        if len(self.queue) == 0 or len(self.vc.channel.members) == 1:
            await self.vc.disconnect()
            return

        #Play the song, and after you are done run this function again.
        self.current_song = self.queue.popleft()
        self.vc.play(self.current_song.source,after=self.loop)

    def skip(self) -> None:
        if self.vc.is_playing():
            
            #Names are deceiving! Stop acts just like a skip.
            self.vc.stop()

    def toggle_pause(self) -> str:
        if self.vc.is_playing():
            self.vc.pause()
            return "Paused"

        elif self.vc.is_paused():
            self.vc.resume()
            return "Unpaused"

#Actual slash commands live here.
class Beats(commands.Cog):

    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot
        self.ytdl = YoutubeDL({'quiet':True})
        self.voice = None
        self.player = None
   
    #Connect to a voice channel and get a new player.
    async def _connect_voice(self, channel: VoiceChannel) -> None:
        self.voice = await channel.connect()
        self.player = Player(self.voice)

    #This is used to get streaming info from YouTube.
    def _get_song(self, url: str) -> Song:
        info = self.ytdl.extract_info(url=url, download=False)

        #Grab the m4a stream with medium quality.
        source = FFmpegPCMAudio(info['formats'][6]['url'])

        return Song(source, info['title'])

    @slash_command(name='play', description='Play music using YouTube links.')
    async def play(self, inter: Interaction, url: str) -> None:
        if inter.user.voice == None:
           await inter.response.send_message('You are not in a voice channel!')
        else:
            try:
                song = self._get_song(url)
            except DownloadError:
                msg = 'There was an error getting that video. Please make sure it is a valid YouTube URL and try again'
                await inter.response.send_message(msg)
                return

            #Connect to a channel if there is no voice client or not connected.
            if self.voice == None or not self.voice.is_connected():
                await self._connect_voice(inter.user.voice.channel)
          
            #Append to right of deque.
            self.player.queue.append(song)
            
            await inter.response.send_message(f'Added *{song.name}* to the queue.')

            #If not already in loop, start loop.
            if not self.voice.is_playing():
                await self.player.loop()

    @slash_command(name='tp', description='Pause/Unpause music.')
    async def pause(self, inter: Interaction) -> None:
        if inter.user.voice == None:
            await inter.response.send_message('You are not in a voice channel!')
        else:
            state=self.player.toggle_pause()
            await inter.response.send_message(f'{state} music.')

    @slash_command(name='skip', description='Skip to next song in queue.')
    async def skip(self, inter: Interaction) -> None:
        if inter.user.voice == None:
           await inter.response.send_message('You are not in a voice channel!')
        else:
            song = self.player.current_song.name
            self.player.skip()
            await inter.response.send_message(f'Skipped *{song}*.')

    #Spits out the current song a visualization of the queue
    @slash_command(name='status', description='Print the queue and now playing.')
    async def print_queue(self, inter: Interaction) -> None:
        if self.voice.is_connected():

            #Get a list of all song names in queue, in order.
            songs = [ f'*{x.name}*\n' for x in self.player.queue ]
            await inter.response.send_message(f'**Currently playing:** *{self.player.current_song.name}*\n\n**NEXT: ** {"".join(songs)}**END**')
        else:
            await inter.response.send_message("I am not active.")


    @slash_command(name='byebye', description='Miku will leave the voice channel.')
    async def disconnect(self, inter: Interaction) -> None:
        await self.voice.disconnect()
        await inter.response.send_message("Goodbye!")
