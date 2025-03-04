import discord, random
from discord import app_commands
from discord.ext import commands

# this class is the definition for the bot itself, it inherits discord's prebuilt client class.
class MyClient(discord.AutoShardedClient):
    def __init__(self, *args, intents, **kwargs,) -> None:
        super().__init__(*args, intents=intents, **kwargs)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        await self.wait_until_ready()
        print("online")

# instantiated the bot with 1 shard, meaning 1 instance, with default intents, which tell discord it wants to be able to read and write messages.
client = MyClient(shards=1,intents= discord.Intents.default())

# this is the simple version of dice rolling, the user tells the bot the number of dice and size of dice and it rolls it. 
# I found this too simplistic for my taste as multiple sizes of dice being rolled at the same time isn't supported, so the V2 version was built
@client.tree.command(name="roll")
@app_commands.describe(numberofdice = "Number of dice you'd like to roll", dicesize = "Size of the dice you'd like to roll")
async def roll(interaction: discord.Interaction,numberofdice:int,dicesize:int):
    total = ""
    for i in range(numberofdice):
        total += str(random.randint(1,dicesize)) + " "
    await interaction.response.send_message(f"{total}")

# this command allows the user to enter a comma seperated list of dice and the bot will roll them for the user and send them the results
@client.tree.command(name="rollv2")
@app_commands.describe(listofdice = "List of the dice you're rolling, seperated by a comma, i.e (1d4,2d12)")
async def rollv2(interaction: discord.Interaction,listofdice:str):
    listofdice = listofdice.replace(" ","").split(",")
    total = ""
    for i in range(len(listofdice)):
        listofdice[i] = listofdice[i].split("d")
        if int(listofdice[i][0]) > 0:
            total += str(listofdice[i]).strip("[]").replace("'","").replace(",","d").replace(" ","") + " ="
            for o in range(int(listofdice[i][0])):
                total += " "
                total += str(random.randint(1,int(listofdice[i][1])))
            if i != len(listofdice)-1:
                total += ", "
        else:
            total += "Not a valid dice"
            if i != len(listofdice)-1:
                total += ", "
    totalSend = []
    while len(total) > 2000:
        totalSend.append(total[:2000])
        total = total[2000:]
    totalSend.append(total)
    # should the list of results be too long for discord's message size limit, the bot will send a follow up message, 
    # replying to its first message so that there's a trail of the answers.
    for i in range(len(totalSend)):
        if i == 0:
            await interaction.response.send_message(f"{totalSend[i]}")
        else:
            await interaction.followup.send(f"{totalSend[i]}")

# Depreciated Sync command, previously used to verify the bot will respond, removed for now
# @client.tree.command(name="sync", description="Owner only")
# async def sync(interaction: discord.Interaction):
#     if :
#         await client.tree.sync()
#         await interaction.response.send_message(f"Synced!", ephemeral=True)
#     else:
#         await interaction.response.send_message(f"Only the owner of the bot can run this command", ephemeral=True)

# actually run the bot, the unique ID is passed here.
client.run("")