import time

import config
import chain
import func

from func import сheck_trx_id_for_presence_in_the_database as сheck_trx


def transaction_processor():
    while True:
        tx = chain.get_the_last_transaction()
        users = func.json_reader(config.USER_FILE_NAME)
        for user_name in users:
            for txs in func.find_all_transactions_with_a_user(user_name, tx):
                if сheck_trx(func.get_tx(txs)) == False:
                    pass





        time.sleep(3600)