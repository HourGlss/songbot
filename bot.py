import os  # for importing env vars for the bot to use
import twitchio
from twitchio.ext import commands
from winamp.winamp import Winamp
import env as config
import time

last_spoke = None
wina = None

bot = commands.Bot(
    # set up the bot
    irc_token=config.TMI_TOKEN,
    client_id=config.CLIENT_ID,
    nick=config.BOT_NICK,
    prefix=config.BOT_PREFIX,
    initial_channels=[config.CHANNEL]
)


@bot.event
async def event_ready():
    global last_spoke
    global wina
    while True:
        try:
            wina = Winamp()
            print("Found winamp, launching")
            break
        except:
            print("Start Winamp ya goober")
            print("Will retry 'soon' to finish launching bot")
        time.sleep(3)
    last_spoke = time.time()
    # 'Called once when the bot goes online.'
    # print(f"Winamp Song Bot is Running!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    # await ws.send_privmsg(config.CHANNEL, f"Use {config.BOT_PREFIX}song to see what song I'm listening to!")


@bot.event
async def event_message(message: twitchio.Message):
    # print(message.content)
    # print(f"message type {type(message)}")

    # If you override event_message you will need to handle_commands for commands to work.
    await bot.handle_commands(message)


@bot.command(name='song')
async def song(ctx):
    global last_spoke
    now = time.time()
    # print(str(ctx))
    if now - last_spoke > 2:
        last_spoke = now
        track_name = wina.getCurrentTrackName()
        trim = track_name.find("- Winamp")
        if trim != -1:
            track_name = track_name[:trim]
        await ctx.send(f'{track_name}')


if __name__ == "__main__":
    bot.run()
