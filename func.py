import io
import os
import json
import time
import random
import hashlib

import chain
import config
import keyboa


def creates_a_hash_of_the_winning_number(num):    # Создает хеш
    salt = os.urandom(64).hex()
    data = f'{num} {salt}'
    return hashlib.md5(data.encode()).hexdigest(), salt, num


def add_new_user(user_wallet, user_id):    # Добовляет нового пользователя
    memo = get_new_memo()
    users = json_reader(config.USER_FILE_NAME)
    if check_for_telegram_id(user_id, users):
        return False
    if check_the_user_for_availability(user_wallet, users):
        users[user_wallet] = {'memo': memo,
                              'bets': {},
                              'telegram_id': user_id}
        json_writer(users, config.USER_FILE_NAME)


# True - Это ползователя нет, а False - это он есть
def check_the_user_for_availability(name, users):
    for x in users:
        if x == name:
            return False
    else:
        return True


def check_for_telegram_id(telegram_id, users):    # Есть ли такой telegram id
    for x in users.values():
        if x['telegram_id'] == telegram_id:
            return True


def get_new_memo():    # Генерирует новое и уникальное memo
    while True:
        memo = os.urandom(4).hex()
        if checking_memo_for_uniqueness(memo):
            break
    return memo


def if_text_is_a_number(text: str):    # Сообщение это число или нет
    try:
        if int(text) > 10000 or int(text) < 0:
            return config.SPAN_OF_NUMBERS
        if 0 < int(text) <= 10000:
            return True
        else:
            return False
    except:
        return False


def checking_memo_for_uniqueness(memo):    # Проверяет memo на уникальность
    previous = json_reader(config.USER_FILE_NAME)
    for x in previous.values():
        if x['memo'] == memo:
            return False
    else:
        return True


def json_writer(data, file_name, encoding='utf8'):    # Запись в файл
    with io.open(file_name, 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False)


def json_reader(file_name):    # Чтение файла
    with io.open(file_name, encoding='utf8') as inputFile:
        data = json.load(inputFile)
    return data


def clearing_bets_after_playing():    # Очищяет ставки после игры
    users = json_reader(config.USER_FILE_NAME)
    # Сохранить данные
    data = json_reader(config.OLD_USERS_FILE_NAME)
    data[time.time()] = users
    json_writer(data, config.OLD_USERS_FILE_NAME)

    for x in users:
        users[x]['bets'].clear()

    json_writer(users, config.USER_FILE_NAME)


def adding_rate(user_name, bet):    # Добовляет ставку (пользователю)
    users = json_reader(config.USER_FILE_NAME)
    for listt in users[user_name]['bets']:
        if listt == str(bet):
            return False
    else:
        users[user_name]['bets'][bet] = False
        json_writer(users, config.USER_FILE_NAME)
        return True


def get_name_by_id(telegram_id):    # Найти имя пользователя по id telegram
    users = json_reader(config.USER_FILE_NAME)
    for x in users:
        if users[x]['telegram_id'] == telegram_id:
            return x


def check_for_existence(account):    # Проверка аккаунта на существования
    try:
        chain.account_info(account)['account_name']
        return True
    except:
        return False


def get_hash():    # Возаращяет хеш
    return json_reader(config.HASH_FILE_NAME)['hash']


def keyboard_configur(*args):    # (list)
    return keyboa.Keyboa(args[0]).keyboard


def hash_update():    # Обновления хеша
    ran = random.randint(1, 10000)
    hashh, salt, num = creates_a_hash_of_the_winning_number(ran)
    # Сохранить старые хеши
    old = json_reader(config.OLD_HASHES_FILE_NAME)
    old[time.time()] = json_reader(config.HASH_FILE_NAME)
    json_writer(old, config.OLD_HASHES_FILE_NAME)
    # Записать новыйе значения
    data = {"num": num, "salt": salt, "hash": hashh}
    json_writer(data, config.HASH_FILE_NAME)


# Найти все транзакции с пользователем N
def find_all_transactions_with_a_user(user, txs):
    result = []
    for x in txs['actions']:
        data = x['action_trace']['act']['authorization'][0]['actor']
        if data == user:
            result.append(x)
    return result


# Проверить trx_id на наличие в базе
def сheck_trx_id_for_presence_in_the_database(tx):
    users = json_reader(config.USER_FILE_NAME)
    for x in users.values():
        for us_tx in x['bets']:
            if x['bets'][us_tx] == tx:
                return True
    else:
        return False


def get_memo(data):
    return data['action_trace']['act']['data']['memo']


def get_tx(data):
    return data['action_trace']['trx_id']


def get_quantity(data):
    return data['action_trace']['act']['data']['quantity']


def get_user_name(data):
    return data['action_trace']['act']['data']['from']


# Заменить false на trx_id
def replace_false_with_trx_id(user_name: str, bet: str, tx: str):
    users = json_reader(config.USER_FILE_NAME)
    try:    # Заменить false на trx_id
        if users[user_name]['bets'][bet] == False:
            users[user_name]['bets'][bet] = tx
        else:
            return False
    except:     # Добавить ставку
        users[user_name]['bets'][bet] = tx
        '''for x in users[user_name]['bets']:
            if x == bet:
                if users[user_name]['bets'][x] == False:
                    users[user_name]['bets'][x] = tx
                else:
                    return False'''
    json_writer(users, config.USER_FILE_NAME)


# Присваивать deposit к первой попавшейся ставки
def to_the_first_bet_that_comes_across(user_name, tx):
    users = json_reader(config.USER_FILE_NAME)
    for bet in users[user_name]['bets']:
        if users[user_name]['bets'][bet] == False:
            users[user_name]['bets'][bet] = tx
            return True
    else:
        return False


# True добовляет 0.01 | False Обнуляет 
def accounting_for_the_prize_fund(waht : bool):
    how_much = json_reader(config.PRIZE_FUND)
    if waht:
        how_much[0] += 0.01
    else:
        how_much[0] = 0
    json_writer(how_much, config.PRIZE_FUND)