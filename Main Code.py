import discord
from discord.ext import commands, tasks
import os
from discord.flags import Intents
from discord.utils import get
from random import randint
import youtube_dl
import random

client = commands.Bot(command_prefix = '.', help_command=None, Intents=Intents)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('what ever status you want'))
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
  try:
    if "discord.gg" in message.content.lower():
      role = discord.utils.get(message.guild.roles, name = 'Discord')
      if role not in message.author.roles:
        await message.delete()
        await message.channel.send("WHat ever you want to say to the person trying to post discord links ")
      else:
        return
  except:
     return

  await client.process_commands(message)

@client.command()
async def ping(ctx):
    await ctx.send(f"Ping is {round(client.latency * 1000)}ms")

@client.command(aliases=['8ball', "test"])
async def _8ball(ctx, *, question):
    responses = ["It is certain.",
                 "It is decidedly so.",
                 "Without a doubt.",
                 "Yes - definitely.",
                 "You may rely on it.",
                 "As I see it, yes.",
                 "Most likely.",
                 "Outlook good.",
                 "Yes.",
                 "Signs point to yes.",
                 "Reply hazy, try again.",
                 "Ask again later.",
                 "Better not tell you now.",
                 "Cannot predict now.",
                 "Concentrate and ask again.",
                 "Don't count on it.",
                 "My reply is no.",
                 "My sources say no.",
                 "Outlook not so good.",
                 "Very doubtful."]
    await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

@client.command()
async def blackhole(ctx, amount=1000000):
    await ctx.channel.purge(limit=amount)

@client.command()
async def whipehard(ctx, amount=100):
    await ctx.channel.purge(limit=amount)

@client.command()
async def whipe(ctx, amount=50):
    await ctx.channel.purge(limit=amount)

@client.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return

    await ctx.send("Getting everything ready now")

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 1.00

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")

@client.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f"Joined {channel}")

@client.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f'left {channel.mention}')

@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")

@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("the audio is not paused.")

@client.command()
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
    else:
        await ctx.send('There is no music to stop...')

@client.group(invoke_without_command=True)
async def help(ctx):

    random = randint(0, 0xffffff)


    em = discord.Embed(title = 'Bot Commands', color=random)

    em.add_field(name = "Moderation", value = 'what ever you name the commands' )

    em.add_field(name = "Fun", value = 'what ever you name the commands')

    em.add_field(name = "Music", value = "what ever you name the commands")

    em.add_field(name="CREATOR", value="**Your name**")

    await ctx.send(embed = em)

@client.command()
async def poll(ctx,*,message):
    emb=discord.Embed(title=" POLL", description=f"{message}")
    msg=await ctx.channel.send(embed=emb)
    await msg.add_reaction('👌')
    await msg.add_reaction('🚫')

@client.command(description="Bans a member")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)

    random = randint(0, 0xffffff)

    em = discord.Embed(title = 'BANNED', color=random)

    em.add_field(name="BANNED", value=f"{member.mention} was banned for {reason}")

    await ctx.send(embed = em)

    await ctx.send("Your favorite gif")

@client.command(description="Kicks a member")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member} was kicked!")

@client.command(description="Unbans a member")
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    bannedUsers = await ctx.guild.bans()
    name, discriminator = member.split("#")

    for ban in bannedUsers:
        user = ban.user

        if(user.name, user.discriminator) == (name, discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} was unbanned.")
            return

@client.command()
async def userinfo(ctx, member: discord.Member):

    roles = [role for role in member.roles]

    embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)

    embed.set_author(name=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Guild name:", value=member.display_name)

    embed.add_field(name="Created at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p EST"))
    embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p EST"))

    embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
    embed.add_field(name="Top role:", value=member.top_role.mention)

    embed.add_field(name="BOT?", value=member.bot)

    embed.add_field(name="CREATOR", value="**Your name**")

    await ctx.send(embed=embed)

@client.command()
async def mute(ctx, member: discord.Member=None):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not member:
        await ctx.send("Please specify a member")
        return
    await member.add_roles(role)
    em = discord.Embed(title = "Mute", timestamp = ctx.message.created_at, color=discord.Color.blue())
    em.add_field(name = "Answer", value = f"{member.mention} is now Muted")

    await ctx.send(embed = em)

@client.command()
async def unmute(ctx, member: discord.Member=None, reason=None):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not member:
        await ctx.send("Please specify a member")
        return
    await member.remove_roles(role)
    em = discord.Embed(title = "Unmute", timestamp = ctx.message.created_at, color=discord.Color.blue())
    em.add_field(name = "Answer", value = f"{member.mention} is now Unmuted")
    await ctx.member.send(f"You have been mute for {reason}")

    await ctx.send(embed = em)

@client.command()
async def discordrole(ctx):
    await ctx.author.send("message")

client.run("TOKEN")