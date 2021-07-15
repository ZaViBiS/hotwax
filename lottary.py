import random

import func
import config



def decides_who_won():
    win = random.randint(1, 10000)
    winners = winner(win)


def winner(win):
    winners = {}
    how_much = 0
    users = func.json_reader(config.USER_FILE_NAME)
    for user_name in users:
        for bet in users[user_name]['bets']:
            if bet == win:
                winners[user_name] = users[user_name]['bets'][bet]
                how_much += 1
                break
    winners['how_much'] = how_much
    return winners
