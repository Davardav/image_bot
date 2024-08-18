import telebot
from config import *
from logic import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "cat")

@bot.message_handler(commands=['g'])
def handle_start(message):
    text = message.text.split()[-1]
    user_id = message.chat.id
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', APY_KEY, SECRET_KEY)
    model_id = api.get_model()
    uuid = api.generate(text, model_id)
    images = api.check_generation(uuid)[0]
    api.save_image(images,f"{user_id}.png")
    with open(f'{user_id}.png','rb') as map:
        bot.send_photo(user_id, map)


if __name__=="__main__":
    manager = Text2ImageAPI('https://api-key.fusionbrain.ai/', APY_KEY, SECRET_KEY)
    bot.polling()
