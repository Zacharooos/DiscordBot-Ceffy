#revised/fixed version from https://youtu.be/xrHOqasnoyA

## ARQUIVO DO GITHUB DA COMANDTREE COM SLASH ##

import discord
from discord import app_commands 

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False #we use this so the bot doesn't sync commands more than once

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: #check if slash commands have been synced 
            await tree.sync(guild = discord.Object(id=994616556401197179)) #guild specific: leave blank if global (global registration can take 1-24 hours)
            self.synced = True
        print(f"We have logged in as {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)

@tree.command(guild = discord.Object(id=994616556401197179), name = 'testeceffy', description='Testando comando slash') #guild specific slash command
async def slash2(interaction: discord.Interaction):
    await interaction.response.send_message(f"Onii-chan o((>ω< ))o")

client.run('MTA3MjE2NTQ3NDUyMTA3MTcxNg.GCW2tt.Ndp7sIUfDrnXjoyzEuk3QOqTNMRY9rJo1T7Fq4')