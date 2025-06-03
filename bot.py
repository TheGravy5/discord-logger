import discord
from discord import app_commands
import time
from pathlib import Path

t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)

# setup loggingchannel on init
loggingid: int = 0
lguildid: int = 0
with Path('./ids.txt').open() as f: 
    loggingid = int(f.readline())
    lguildid = int(f.readline())

# human readable time for logging messages
from datetime import datetime, timedelta, timezone
def human_readable_time(dt: datetime, now: datetime = None) -> str:
    if not now:
        now = datetime.now(tz=timezone.utc)

    date_part = ''
    today = now.date()
    yesterday = today - timedelta(days=1)

    if dt.date() == today:
        date_part = 'Today'
    elif dt.date() == yesterday:
        date_part = 'Yesterday'
    elif now.year > dt.year:
        date_part = dt.strftime('%B %d, %Y')
    else:
        date_part = dt.strftime('%B %d')

    time_part = dt.strftime('%H:%M')
    return f'{date_part} at {time_part}'

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name = "ping", description = "pings the bot", guild=discord.Object(id=lguildid))
async def ping(interaction: discord.Interaction):
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(f'{current_time} | {interaction.user} used /ping')
    await interaction.response.send_message(f'Pong :ping_pong: `{round(client.latency * 1000)}ms`', ephemeral=True)

@tree.command(name="set", description="set up the logging", guild=discord.Object(id=lguildid))
async def set(interaction: discord.Interaction, channel: discord.TextChannel):
    if (interaction.permissions.manage_guild):
        with Path('./ids.txt').open("w", encoding="utf-8") as f:
            loggingid = channel.id
            f.writelines([str(loggingid), '\n', str(lguildid)])
            global loggingchannel
            loggingchannel = channel # type: ignore
        await interaction.response.send_message(f"Set logging channel to <#{channel.id}>")
    else: 
        await interaction.response.send_message(f"You do not have permissions to run this command.\n> Missing permission `MANAGE GUILD`", ephemeral=True)

@tree.command(name="help", description="Gives information on how to configure the bot.", guild=discord.Object(id=lguildid))
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(f"This bot is a simple bot for logging messages and images within a single server.\n"+
                                            "* Messages from other bots are not logged.\n"+
                                            "* To prevent logging in specific channels, deny the bot access.\n"+
                                            "* To set the channel used for logging, use /set [channel]\n"+
                                            "* You can self-host this bot for your own server by copying the code from https://github.com/TheGravy5/discord-logger and following the steps in the readme. Python path must be configured correctly and the required packages must be installed.", ephemeral=True)


@client.event
async def on_ready():
    guildtemp = client.get_guild(lguildid)
    if (guildtemp):
        global lguild
        lguild = guildtemp
    else:
        print(f"guild {lguildid} not found; terminating bot")
        exit(1)
    global loggingchannel
    loggingchannel = lguild.get_channel(loggingid) # type: ignore
    await tree.sync(guild=lguild)
    print("Bot ready.")

@client.event
async def on_message_delete(message: discord.Message):
    if (message.guild.id == lguildid and not message.author.bot):
        emb = discord.Embed(color=discord.Color.from_rgb(255, 0, 0), title=f"Message Deleted in {message.channel} {message.channel.mention}", description=message.content)
        emb.set_author(icon_url=message.author.display_avatar.url, name=message.author)
        emb.set_footer(text = f"User ID: {message.author.id} | Time (UTC): {human_readable_time(message.created_at)}")
        if (len(message.attachments) > 0):
            formattedFiles = []
            for attachment in message.attachments:
                print(attachment.content_type)
                if (attachment.content_type.startswith("image")):
                    formattedFiles.append(await attachment.to_file(use_cached=True))
            if (len(formattedFiles) == 1):
                await loggingchannel.send("Contains image:", embed=emb, file=formattedFiles[0])
            else:
                await loggingchannel.send("Contains images:", embed=emb, files=formattedFiles)
        else:
            await loggingchannel.send(embed=emb)


client.run(Path.open("token.txt").readline())