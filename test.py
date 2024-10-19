from telebot.async_telebot import AsyncTeleBot
import asyncio
import os
import urllib.request

def read_token() -> str:
    with open('token.txt', 'r') as file:
        return file.read()

###############################
# BOT PARAMETERS
###############################
API_TOKEN = read_token()

idle_mod = False
wait_file = False
table_path = './Clean.xlsx'
###############################

bot = AsyncTeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
async def send_greeting(message):
    greeting = '''
Type /info to get proper info about bot functions.
'''
    await bot.send_message(message.chat.id, greeting)

@bot.message_handler(commands=['info'])
async def send_info(message):
    info = '''
Feature status:
    - IDLE_MODE: {0}
Available commands:
    - /start - get start message
    - /info - get this window
    - /idle - switch idle mode
    - /update - send new .xlsx table
'''
    await bot.send_message(message.chat.id, info.format('ACTIVATED' if idle_mod else 'DEACTIVATED'))

@bot.message_handler(commands=['idle'])
async def send_notice(message):
    global idle_mod
    idle_mod = not idle_mod
    if idle_mod:
        await bot.send_message(message.chat.id, 'IDLE MOD ACTIVATED')
    else:
        await bot.send_message(message.chat.id, 'IDLE MOD DEACTIVATED')
    while idle_mod:
        await bot.send_message(message.chat.id, 'I am here')
        await asyncio.sleep(10)

@bot.message_handler(commands=['update'])
async def send_rules(message):
    await bot.send_message(message.chat.id, 'Send new *.xlsx file...')
    await wait_for_file(message)

@bot.message_handler(content_types=['document'])
async def get_new_xlsx(message):
    global wait_file
    if(wait_file):
        wait_file = False
        xlsx_file_id = message.document.file_id
        file_url = await bot.get_file_url(file_id=xlsx_file_id)
        os.remove(table_path)
        urllib.request.urlretrieve(file_url, table_path)
        await bot.send_message(message.chat.id, 'File was updated')

async def wait_for_file(message):
    global wait_file
    wait_file = True
    while wait_file:
        await asyncio.sleep(5)
        await bot.send_message(message.chat.id, 'Still waiting for file...')
    
def main() -> None:
    asyncio.run(bot.infinity_polling())

if __name__ == '__main__':
    main()
