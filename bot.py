import logging

import person_data
import func
import config

from telebot import TeleBot


bot = TeleBot(person_data.TOKEN)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s',
                    filename=config.LOG_FILE_NAME)


@bot.message_handler(['start'])
def start(message):
    bot.send_message(message.chat.id, config.START_TEXT)


@bot.message_handler(['test'])
def test(message):
    if func.adding_rate('yamle.wam', 12):
        bot.send_message(message.chat.id, 'добавленна')
    else:
        bot.send_message(message.chat.id, 'уже существует')


@bot.message_handler(['hash'])
def test(message):
    bot.send_message(message.chat.id, func.get_hash())


@bot.message_handler(content_types=['text'])
def processing_text_responses(message):
    # func.if_text_is_a_number(message.text)
    if False:
        pass
        
    else:
        if func.check_for_existence(message.text):
            if func.add_new_user(message.text, message.chat.id) == False:
                bot.send_message(message.chat.id, config.USER_EXIST)
            else:
                bot.send_message(message.chat.id, 
                                config.SUCCESSFUL_REGISTRATION)
        else:
            bot.send_message(message.chat.id, config.NO_ACCOUNT)


bot.polling(True)
