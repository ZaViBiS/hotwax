import logging
import threading

import person_data
import func
import config
import lottary

from telebot import TeleBot
from transaction_processor import tx_processor

# init
bot = TeleBot(person_data.TOKEN)
# обработчик транзакций
threading.Thread(target=tx_processor).start()   
# Проводит розыгрыши
threading.Thread(target=lottary.hold_draws_once_a_day).start()   
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s:%(message)s',
                    filename=config.LOG_FILE_NAME)


@bot.message_handler(['start'])
def start(message):
    bot.send_message(message.chat.id, config.START_TEXT)


@bot.message_handler(['test'])
def test(message):
    func.hash_update()


@bot.message_handler(['hash'])
def test(message):
    bot.send_message(message.chat.id, func.get_hash())

# Кнопки
@bot.callback_query_handler(func=lambda call: True)
def click_handler(call):
    if call.data == config.ADD_USER:    # Добавить пользователя
        if func.check_for_existence(call.message.text):
            if func.add_new_user(call.message.text, call.message.chat.id) == False:
                bot.send_message(call.message.chat.id, config.USER_EXIST)
            else:
                bot.send_message(call.message.chat.id,
                                 config.SUCCESSFUL_REGISTRATION)
        else:
            bot.send_message(call.message.chat.id, config.NO_ACCOUNT)
    elif call.data == config.BET:   # Ставка
        user_name = func.get_name_by_id(call.message.chat.id)
        func.adding_rate(user_name, call.message.text)

# Текст
@bot.message_handler(content_types=['text'])
def processing_text_responses(message):
    if func.if_text_is_a_number(message.text) == True:  # Сообщение это ставка
        bot.send_message(message.chat.id,
                         message.text,
                         reply_markup=func.keyboard_configur(config.BET))

    elif func.if_text_is_a_number(message.text) == config.SPAN_OF_NUMBERS:    # Сообщение это ставка с неправильным промежутком
        bot.send_message(message.chat.id, config.SPAN_OF_NUMBERS)

    else:   # Пользователь
        bot.send_message(message.chat.id,
                         message.text,
                         reply_markup=func.keyboard_configur(config.ADD_USER))


bot.polling(True)
