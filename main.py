import telebot
from config import *
from logic import *
import os
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def handle_start(message):
    bot.send_message(message.chat.id, "Данный бот генерирует картинки \n /g запрос - для генерации картинки \n Например: '/g кот' \n /help для получения информации")

@bot.message_handler(commands=['g'])
def handle_start(message):
    text = message.text.split()[-1]
    user_id = message.chat.id
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', APY_KEY, SECRET_KEY)
    model_id = api.get_model()
    if text == '/g':
        bot.send_message(message.chat.id, "Пожалуйста введите запрос \n Например: '/g кот'")
    else:
        bot.send_message(message.chat.id, text)
        msg = bot.send_message(message.chat.id, "Генерирую картинку..")
        bot.send_chat_action(message.chat.id, 'typing')
        
        uuid = api.generate(text, model_id)
        images = api.check_generation(uuid)[0]
        api.save_image(images,f"{user_id}.png")
        with open(f'{user_id}.png','rb') as map:
            bot.send_photo(user_id, map)
            bot.delete_message(message.chat.id, msg.message_id)
            map.close()
            os.remove(f'{user_id}.png')


if __name__=="__main__":
    manager = Text2ImageAPI('https://api-key.fusionbrain.ai/', APY_KEY, SECRET_KEY)
    bot.polling()
