import discord
import json

GUILD_ID = None
ROLE_ID = None
token = None

with open("token.json", "r") as f:
    js = json.load(f)
    GUILD_ID = int(js['GUILD_ID'])
    ROLE_ID = int(js['ROLE_ID'])
    token = js['token']

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == "Bennett's Heart":
            break
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

async def update_role(user_id):
    guild = client.get_guild(GUILD_ID)
    member = await guild.fetch_member(user_id)
    role = guild.get_role(ROLE_ID)
    if member and role:
        await member.add_roles(role)
        print(f"Updated roles for {member.name}")
    else:
        print("Member or role not found")

client.run(token)