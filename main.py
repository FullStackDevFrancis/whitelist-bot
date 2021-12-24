import psycopg2
import os
from discord.ext import commands
import discord

TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')
client = discord.Client()


@client.event
async def on_message(message):
    if message.guild:
        if not str('923579001010794527') in str(message.author.id):
            print(message.author.id)
            await message.channel.send(f"<@{message.author.id}>, please send me a private message...")

    else:
        if message.content == '>>help':
            await message.channel.send(getHelpMessage())
        elif message.content == '>>info':
            await message.channel.send(getInfoMessage())
        elif message.content == '>>check':
            result = readDatabase('check', message.author.id, message.content)
            if len(result) > 0:
                await message.channel.send('Your address is set: ' + str(result[0][0]))
            else:
                await message.channel.send('No address set yet.')
        elif str('>>set') in message.content:
            readDatabase('set', message.author.id, message.content.replace('>>set ', ''))
            await message.channel.send('Address is set! Use >>check to verify!>')


def getHelpMessage():
    welcomeMessage = f"\nWelcome to the Whitelist bot!\n" \
                     "**Commands**\n" \
                     "```>>info                : why is this BOT here?\n" \
                     ">>check               : will return the current token saved for your current ID\n" \
                     ">>set <token>         : will set the token for your current ID\n" \
                     ">>update <token>      : will update your token\n```"

    return welcomeMessage


def getInfoMessage():
    infoMessage = f"```This bot is made to set all whitelist addresses so you can get access to our presale of the VeeParrots-NFT collection.\n" \
                  "If you don't set a valid token, you will not be able to mint NFT's in our presale.```"
    return infoMessage


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


def readDatabase(type, value, value2):
    global connection
    try:
        connection = psycopg2.connect('Good try :)')
        cursor = connection.cursor()

        result = ''

        if type == 'check':
            query = 'SELECT address, name FROM public.whitelists w where name = \'' + str(value) + '\''
            cursor.execute(query)
            result = cursor.fetchall()
        elif type == 'set':
            postgres_insert_query = """ INSERT INTO public.whitelists(address, name) VALUES (%s, %s)"""
            record_to_insert = (value2, value)
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()
            result = cursor.rowcount

        print('res', result)
        return result


    except (Exception, psycopg2.Error) as error:
        print(error)
        return str(error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()


client.run(TOKEN)
