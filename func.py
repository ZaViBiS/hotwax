import io
import os
import json
import hashlib

import config
import keyboa
import requests


def creates_a_hash_of_the_winning_number(num):
    salt = os.urandom(64).hex()
    data = f'{num} {salt}'
    return hashlib.sha256(data.encode()).hexdigest()


def add_new_user(user_wallet, user_id):
    memo = get_new_memo()
    users = json_reader(config.USER_FILE_NAME)
    if check_for_telegram_id(user_id, users):
        return False
    if check_the_user_for_availability(user_wallet, users):
        users[user_wallet] = {'memo': memo,
                              'bets': [],
                              'telegram_id': user_id}
        json_writer(users, config.USER_FILE_NAME)


# True - Это ползователя нет, а False - это он есть
def check_the_user_for_availability(name, users):
    for x in users:
        if x == name:
            return False
    else:
        return True


def check_for_telegram_id(telegram_id, users):
    for x in users.values():
        if x['telegram_id'] == telegram_id:
            return True


def get_new_memo():
    while True:
        memo = os.urandom(4).hex()
        if checking_memo_for_uniqueness(memo):
            break
    return memo


def if_text_is_a_number(text):
    try:
        if 0 > int(text) <= 10000:
            return True
        else:
            return False
    except:
        return False


def checking_memo_for_uniqueness(memo):
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


def clearing_bets_after_playing():
    users = json_reader(config.USER_FILE_NAME)
    for x in users:
        users[x]['bets'].clear()
    json_writer(users, config.USER_FILE_NAME)


def adding_rate(user_name, bet):
    users = json_reader(config.USER_FILE_NAME)
    for listt in users[user_name]['bets']:
        for dictt in listt:
            if dictt == str(bet):
                return False
    else:
        users[user_name]['bets'].append({bet: False})
        json_writer(users, config.USER_FILE_NAME)
        return True


def get_name_by_id(telegram_id):
    users = json_reader(config.USER_FILE_NAME)
    for x in users:
        if users[x]['telegram_id'] == telegram_id:
            return x


# Получает информацию про аккаунт
def account_info(account):
    data = json.dumps({'account_name': account})
    respone = requests.post(config.INFO_POST_ACCOUNT, data=data).text
    return json.loads(respone)


def check_for_existence(account):
    try:
        account_info(account)['account_name']
        return True
    except:
        return False


def get_hash():
    return json_reader(config.HASH_FILE_NAME)['hash']


# (list)
def keyboard_configur(*args):
    return keyboa.Keyboa(args[0]).keyboard

