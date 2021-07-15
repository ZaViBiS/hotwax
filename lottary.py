import datetime
import time
import json
import logging

import func
import config


def decides_who_won():
    win = func.json_reader(config.HASH_FILE_NAME)['num']
    winners = winner(str(win))
    if winners:
        # призовой фонд / количесто учасноков
        payout = what_is_the_prize_fund() / winners['how_much']
        # выплата -5% и округление до 3 знаков после запятой
        payout = round(payout - ((payout / 100) * 5), 3)
        winners['how_much'] = payout

        func.accounting_for_the_prize_fund(False)
        func.json_writer(winners, config.WINNERS_FILE_NAME)
    else:
        func.json_writer({}, config.WINNERS_FILE_NAME)
    func.hash_update()
    return winners


def winner(win: str):
    winners = {}
    how_much = 0
    users = func.json_reader(config.USER_FILE_NAME)
    for user_name in users:
        for bet in users[user_name]['bets']:
            bet_data = users[user_name]['bets'][bet]

            if bet == win and bet_data != False:
                winners[user_name] = bet_data
                how_much += 1
                break
    if winners == {}:
        return False
    winners['how_much'] = how_much
    return winners


def what_is_the_prize_fund():
    return func.json_reader(config.PRIZE_FUND)[0]


def hold_draws_once_a_day():
    while True:
        timen = datetime.datetime.now().strftime("%H:%M")
        print(timen)
        if timen == '10:00':
            winners = decides_who_won()
            logging.info('розыгрыш провден')
            logging.info(json.dumps(winners))
            time.sleep(1380) # 23 часа
        time.sleep(1)


if __name__ == '__main__':
    hold_draws_once_a_day()
