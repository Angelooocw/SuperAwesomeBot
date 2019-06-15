from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config.auth import token

import logging
import requests
import pandas
import csv
import io
import os
import psycopg2


os.environ['BOT_TOKEN'] = token

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('SuperAwesome2bot')

def start(bot, update):

    logger.info('Comando start recibido')
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Soy un robot beep-boop.'
    )

def random_dog(bot, update):
    logger.info('Comando random_dog recibido')
    contents = requests.get('https://random.dog/woof.json').json()
    print(update)
    print(contents)
    url= contents['url']

    print(url)

    bot.send_message(
        chat_id=update.message.chat_id,
        text='Random dog'
    )
    v_url=url.find('mp4')
    print (v_url)
    if(v_url==-1):
        bot.send_photo(
        chat_id=update.message.chat_id,
        photo=url)
    
    else:
        bot.send_video(
            chat_id=update.message.chat_id,
            video=url,
            supports_streaming=True)

def random_meme(bot, update):
    logger.info('Comando random_meme')
    contents = requests.get('https://meme-api.herokuapp.com/gimme').json()
    url = contents['url']

    bot.send_message(
        chat_id=update.message.chat_id,
        text=contents['title']
    )

    bot.send_photo(
        chat_id=update.message.chat_id,
        photo=url
    )

def conv_uppercase(bot, update):
    update.message.reply_text(update.message.text.upper())
    #brick= pandas.DataFrame(mm)

def msg_file(bot, update):
    print(update)
    logger.info('Comando msg_file')
    msg=update['message']['document']
    print(msg)
    file=[msg]
    print(file)
    fileid=file[0]['file_id']
    print(fileid)

    archivo= requests.get('https://api.telegram.org/bot'+token+'/getFile?file_id='+fileid).json()
    print(archivo)

    fp=archivo['result']['file_path']
    print(fp)

    dwnl=requests.get('https://api.telegram.org/file/bot'+token+'/'+fp)

    print('#############')
    print(dwnl)

    df= pandas.read_csv(io.StringIO(dwnl.text))
    #df=pandas.DataFrame(io.StringIO(dwnl.text), columns=['item','item','item'])
    #df= pandas.read_csv(dwnl.text)

    print(df)
    #adj_file=get_adjustment_file(fileid)
    #print(adj_file)
    #print('get_adjustment_file\n'+adj_file)
    

def get_adjustment_file(file_id):
    token = os.getenv('BOT_TOKEN')

    file = requests.get('https://api.telegram.org/bot'+token+'/getFile?file_id='+file_id).json()
    fp=file['result']['file_path']
    dwnl=requests.get('https://api.telegram.org/file/bot'+token+'/'+fp)
    adjustment_df=pandas.read_csv(io.StringIO(dwnl.text))
    return adjustment_df

def main():
    updater=Updater(token=token)
    dispatcher=updater.dispatcher
    dispatcher.add_handler(CommandHandler('start',start))
    dispatcher.add_handler(CommandHandler('random_dog',random_dog))
    dispatcher.add_handler(CommandHandler('meme',random_meme))

    upper_case=MessageHandler(Filters.text, conv_uppercase)
    ffile=MessageHandler(Filters.all,msg_file)

    dispatcher.add_handler(upper_case)
    dispatcher.add_handler(ffile)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
main()