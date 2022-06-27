import nextcord
from nextcord.ext import commands
import json
from music import Beats

def main() -> None:

    #We need these to join voice chats.
    intents = nextcord.Intents.default()
    intents.voice_states = True

    bot = commands.Bot(intents=intents)
    
    bot.add_cog(Beats(bot))

    #Read the bot token in from external JSON.
    with open("creds/creds.json") as credfile:
        creds = json.load(credfile)
        bot.run(creds["token"])

main()

