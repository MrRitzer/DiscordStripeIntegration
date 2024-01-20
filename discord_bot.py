import discord

client = discord.Client()

# Replace with your actual server and role IDs
GUILD_ID = 1196859182419284079
ROLE_ID = 1196890520761405500

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

async def update_role(user_id):
    guild = client.get_guild(GUILD_ID)
    member = await guild.fetch_member(user_id)
    role = guild.get_role(ROLE_ID)
    if member and role:
        await member.add_roles(role)
        print(f"Updated roles for {member.name}")
    else:
        print("Member or role not found")

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
token = 'MTE5NzU5NDI5MTY5NTAwOTgwMw.GhK2bQ.wqLILzMJhRFDoWPt76ubfd3qFI0UTw7A08J6aQ'
client.run(token)