import os # for importing env vars for the bot to use
from twitchio.ext import commands
from winamp.winamp import Winamp
wina = None
import time
last_spoke = None

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
    global last_spoke
    global wina
    wina = Winamp()
    last_spoke = time.time() - 20
    'Called once when the bot goes online.'
    print(f"{os.environ['BOT_NICK']} is online!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(os.environ['CHANNEL'], f"I'll give you the SONGS")


@bot.command(name='song')
async def song(ctx):
    global last_spoke
    now = time.time()
    if now - last_spoke > 30:
        last_spoke = now
        await ctx.send(f'{wina.getCurrentTrackName()}')

if __name__ == "__main__":
    bot.run()