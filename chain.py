# --- Тут функции которые работают с данныеми блокчейна  --- #
import json

import config
import requests


def account_info(account):    # Получает информацию про аккаунт
    data = json.dumps({'account_name': account})
    respone = requests.post(config.INFO_POST_ACCOUNT, data=data).text
    return json.loads(respone)


def get_the_last_transaction():     # Получить 100 последних транзакций
    data = json.dumps({'account_name': "ygbni.wam",
                       'pos': -1,
                       'offset': -100})
    res = requests.post(config.GET_ACTIONS, data).text
    return json.loads(res)

