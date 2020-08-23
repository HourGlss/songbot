import os # for importing env vars for the bot to use
from twitchio.ext import commands
from winamp.winamp import Winamp
wina = None

bot = commands.Bot(
    # set up the bot
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)

@bot.event
async def event_ready():
    global wina
    wina = Winamp()
    'Called once when the bot goes online.'
    print(f"{os.environ['BOT_NICK']} is online!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(os.environ['CHANNEL'], f"I'll give you the SONGS")


@bot.command(name='song')
async def song(ctx):
    await ctx.send(f'{wina.getCurrentTrackName()}')

if __name__ == "__main__":
    bot.run()