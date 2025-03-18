import settings
import discord
from discord.ext import commands
from discord import app_commands

import sqlite3

connection = sqlite3.connect('database/memories.db')
cursor = connection.cursor()

GUILD = discord.Object(id=settings.pagoda_server_id)

class Client(commands.Bot):
    #Initiation
    async def on_ready(self):
        print(f'Logged on as {self.user}')

        #Slash Command Sync
        try: 
            synced = await self.tree.sync(guild=GUILD)
            print(f'Synced {len(synced)} commands to guild {GUILD.id}')
        
        except Exception as e:
            print(f'Error syncing commands: {e}')
    
    #Message event reaction
    async def on_message(self, message):

        HI_TRIGGER = ('hi', 'hello')

        if message.author == self.user:
            return
        
        match message.content.lower():
            case 'excelsior':
                #Fetch random quote here, then send.
                result = cursor.execute('SELECT quote FROM quotes ORDER BY RANDOM() LIMIT 1')
                quote = result.fetchone()
                await message.channel.send(quote[0])
            case 'cookies':
                await message.channel.send('mmmmmmm')
            case 'front':
                await message.channel.send('One')
        
        if message.content.startswith(HI_TRIGGER):
            await message.channel.send('hey guy’s its me nickbot!')
        
        if 'mr mime' in message.content.lower():
            await message.channel.send('leave mr mimes name our of your Dirty fucking mouth and we wont have a problem')

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix='!', intents=intents)

#Slash Commands

#List Quotes
@client.tree.command(name="list", description="Lists all quotes", guild=GUILD)
async def listQuotes(interaction: discord.Integration):

    if interaction.user.id in settings.admin_ids:

        result = cursor.execute('SELECT * FROM quotes')
        quotes = result.fetchall()
        quoteList = []

        for quote in quotes:
            quoteList.append('ID: ' + str(quote[0]) + ' - "' + quote[1] + '"')
    
        await interaction.response.send_message('\n'.join(quoteList))

    else:
        await interaction.response.send_message('nuh uh')

#Add Quote
@client.tree.command(name="add", description="Adds a quote to excelsior database.", guild=GUILD)
async def addQuote(interaction: discord.Integration, quote: str):
    if interaction.user.id in settings.admin_ids:

        data = [quote]
        cursor.execute('INSERT INTO `quotes` (`quote`) VALUES (?)', data)
        connection.commit()

        await interaction.response.send_message(f'Quote added: "{quote}".')

    else:
        await interaction.response.send_message('nuh uh')
    
#Remove Quote
@client.tree.command(name="remove", description="Removes a quote from excelsior database.", guild=GUILD)
async def removeQuote(interaction: discord.Integration, id: int):
    if interaction.user.id in settings.admin_ids:

        data = [id]
        cursor.execute('DELETE FROM quotes WHERE id=?', data)
        connection.commit()

        await interaction.response.send_message('Quote removed.')

    else:
        await interaction.response.send_message('nuh uh')

#Starts this mess
client.run(settings.token)