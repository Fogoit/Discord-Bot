import settings
import discord
from discord.ext import commands
from discord import app_commands

DEV_GUILD = discord.Object(id=settings.dev_server_id)

class Client(commands.Bot):
    async def on_ready(self):
        #Initiation
        game = discord.Game("your mom")
        await self.change_presence(status=discord.Status.idle, activity=game)
        print(f'Logged on as {self.user}')

        #Slash Command Sync
        try: 
            synced = await self.tree.sync(guild=DEV_GUILD)
            print(f'Synced {len(synced)} commands to guild {DEV_GUILD.id}')
        
        except Exception as e:
            print(f'Error syncing commands: {e}')
    
    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content.startswith('hello'):
            await message.channel.send(f'Hi there, {message.author.display_name}.')


intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix='!', intents=intents)

#Slash Commands
@client.tree.command(name="hello", description="Says hello to you :)", guild=DEV_GUILD)
async def sayHello(interaction: discord.Integration):
    await interaction.response.send_message("Hi there!")

@client.tree.command(name="printer", description="Will print shit!", guild=DEV_GUILD)
async def printer(interaction: discord.Integration, printer: str):
    await interaction.response.send_message(printer)

#Starts this mess
client.run(settings.token)