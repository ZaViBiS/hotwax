import time
import random

import config
import chain
import func

from func import сheck_trx_id_for_presence_in_the_database as сheck_trx


def tx_processor():
    while True:
        tx = chain.get_the_last_transaction()
        users = func.json_reader(config.USER_FILE_NAME)
        for user_name in users:
            for txs in func.find_all_transactions_with_a_user(user_name, tx):
                tranx = func.get_tx(txs)

                if сheck_trx(tranx) == False:
                    if chain.get_transaction_amount_by_trx_id(tranx) == '0.01 WAX':
                        memo = func.get_memo(txs)
                        user_name = func.get_user_name(txs)
                        # Добавить пользователя если его нет
                        func.add_new_user(user_name, random.random())

                        # Если в memo есть ставка
                        if func.if_text_is_a_number(memo) == True:
                            func.adding_rate(user_name, memo)
                        elif func.to_the_first_bet_that_comes_across(user_name, tranx):
                            pass
                        else:
                            for _ in range(10000):
                                bet = random.randint(1, 10000)
                                func.adding_rate(user_name, bet)

        time.sleep(10)
