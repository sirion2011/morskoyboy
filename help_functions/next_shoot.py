import random
import math
import inspect
import logging


logger = logging.getLogger(__name__)


def next_shoot(prev_hod, player_sheep, dificulity, player_buttons):
    #logger.info(f"Файл: {__file__}, Функция: {inspect.currentframe().f_code.co_name}")
    shoot = prev_hod
    bokovye_for_shoot = []
    korabl = []
    zacryt = []
    bokovye_for_shoot.append(shoot+5) if shoot+5 in range(1, 26) else -1
    bokovye_for_shoot.append(shoot - 5) if shoot - 5 in range(1, 26) else -1
    bokovye_for_shoot.append(shoot + 1) if shoot + 1 <= math.ceil(shoot / 5) * 5 else -1
    bokovye_for_shoot.append(shoot - 1) if (shoot - 1 <= math.ceil(shoot / 5) * 5 and shoot % 5 != 1) else -1
    bokovye_for_shoot = [num for num in bokovye_for_shoot if 1 <= num <= 25]
    for i in bokovye_for_shoot:
        if i in player_sheep:
            korabl.append(i)

    for i in korabl:
        if i in bokovye_for_shoot:
            bokovye_for_shoot.remove(i)

    if dificulity == 1:
        for krest in bokovye_for_shoot:
            if player_buttons[krest-1].text == f'✖':
                zacryt.append(krest)
        bokovye_for_shoot = [i for i in bokovye_for_shoot if i not in zacryt]

        if not bokovye_for_shoot:
            if prev_hod == player_sheep[0] and player_buttons[player_sheep[1]-1].text == f'✖':
                shoot = player_sheep[2]
            elif prev_hod == player_sheep[2] and player_buttons[player_sheep[1]-1].text == f'✖':
                shoot = player_sheep[0]
            else:
                shoot = random.choice(korabl)
        else:
            shoot = random.choice(bokovye_for_shoot)

        return shoot

    elif dificulity == 2:
        for krest in bokovye_for_shoot:
            if player_buttons[krest-1].text == f'✖':
                zacryt.append(krest)
        bokovye_for_shoot = [i for i in bokovye_for_shoot if i not in zacryt]

        if not bokovye_for_shoot:
            if prev_hod == player_sheep[0] and player_buttons[player_sheep[1]-1].text == f'✖':
                shoot = player_sheep[2]
                return shoot
            elif prev_hod == player_sheep[2] and player_buttons[player_sheep[1]-1].text == f'✖':
                shoot = player_sheep[0]
                return shoot
            else:
                shoot = random.choice(korabl)
        else:
            shoot = random.choice(bokovye_for_shoot)

        if len(bokovye_for_shoot) == 3:
            choice_of_bok_hit = random.choice([0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
            shoot = random.choice(korabl) if choice_of_bok_hit == 1 else random.choice(bokovye_for_shoot)
        elif len(bokovye_for_shoot) == 2:
            choice_of_bok_hit = random.choice([0, 0, 0, 0, 0, 0, 0, 0, 1, 1])
            shoot = random.choice(korabl) if choice_of_bok_hit == 1 else random.choice(bokovye_for_shoot)

        return shoot

    elif dificulity == 3:
        for krest in bokovye_for_shoot:
            if player_buttons[krest - 1].text == f'✖':
                zacryt.append(krest)
        bokovye_for_shoot = [i for i in bokovye_for_shoot if i not in zacryt]

        if not bokovye_for_shoot or len(bokovye_for_shoot) == 1:
            if prev_hod == player_sheep[0] and player_buttons[player_sheep[1]-1].text == f'✖':
                shoot = player_sheep[2]
                return shoot
            elif prev_hod == player_sheep[2] and player_buttons[player_sheep[1]-1].text == f'✖':
                shoot = player_sheep[0]
                return shoot
        if not bokovye_for_shoot:
            shoot = random.choice(korabl)
        else:
            shoot = random.choice(bokovye_for_shoot)

        if len(bokovye_for_shoot) == 3:
            choice_of_bok_hit = random.choice([0, 0, 0, 0, 0, 0, 0, 1, 1, 1])
            shoot = random.choice(korabl) if choice_of_bok_hit == 1 else random.choice(bokovye_for_shoot)
        elif len(bokovye_for_shoot) == 2:
            choice_of_bok_hit = random.choice([0, 0, 0, 0, 0, 0, 1, 1, 1, 1])
            shoot = random.choice(korabl) if choice_of_bok_hit == 1 else random.choice(bokovye_for_shoot)
        elif len(bokovye_for_shoot) == 1:
            choice_of_bok_hit = random.choice([0, 0, 0, 1, 1, 1, 1, 1, 1, 1])
            shoot = random.choice(korabl) if choice_of_bok_hit == 1 else random.choice(bokovye_for_shoot)

        return shoot

    elif dificulity == 4:
        for krest in bokovye_for_shoot:
            if player_buttons[krest - 1].text == f'✖':
                zacryt.append(krest)
        bokovye_for_shoot = [i for i in bokovye_for_shoot if i not in zacryt]

        choice_of_bok_hit = random.choice([0, 0, 1])
        if (not bokovye_for_shoot) or (len(bokovye_for_shoot) == 1) or (len(bokovye_for_shoot) == 2 and choice_of_bok_hit == 1):
            if prev_hod == player_sheep[0] and player_buttons[player_sheep[1]-1].text == f'✖':
                shoot = player_sheep[2]
                return shoot
            elif prev_hod == player_sheep[2] and player_buttons[player_sheep[1]-1].text == f'✖':
                shoot = player_sheep[0]
                return shoot
        if not bokovye_for_shoot:
            shoot = random.choice(korabl)
        else:
            shoot = random.choice(bokovye_for_shoot)

        if len(bokovye_for_shoot) == 3:
            choice_of_bok_hit = random.choice([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])
            shoot = random.choice(korabl) if choice_of_bok_hit == 1 else random.choice(bokovye_for_shoot)
        elif len(bokovye_for_shoot) == 2:
            choice_of_bok_hit = random.choice([0, 0, 0, 0, 1, 1, 1, 1, 1, 1])
            shoot = random.choice(korabl) if choice_of_bok_hit == 1 else random.choice(bokovye_for_shoot)
        elif len(bokovye_for_shoot) == 1:
            choice_of_bok_hit = random.choice([0, 1, 1, 1, 1, 1, 1, 1, 1, 1])
            shoot = random.choice(korabl) if choice_of_bok_hit == 1 else random.choice(bokovye_for_shoot)

        return shoot

    elif dificulity == 5:
        len_bokovye = len(bokovye_for_shoot)
        for krest in bokovye_for_shoot:
            if player_buttons[krest - 1].text == f'✖':
                zacryt.append(krest)
        bokovye_for_shoot = [i for i in bokovye_for_shoot if i not in zacryt]

        choice_of_bok_hit = random.choice([0, 0, 0, 0, 0, 0, 1])
        if (not bokovye_for_shoot) or (len(bokovye_for_shoot) == 1) or (
                len(bokovye_for_shoot) == 2 and choice_of_bok_hit == 1):
            if prev_hod == player_sheep[0] and player_buttons[player_sheep[1] - 1].text == f'✖':
                shoot = player_sheep[2]
                return shoot
            elif prev_hod == player_sheep[2] and player_buttons[player_sheep[1] - 1].text == f'✖':
                shoot = player_sheep[0]
                return shoot
        if not bokovye_for_shoot:
            shoot = random.choice(korabl)
        else:
            shoot = random.choice(bokovye_for_shoot)

        if len(bokovye_for_shoot) == 3:
            choice_of_bok_hit = random.choice([0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
            shoot = random.choice(korabl) if choice_of_bok_hit == 1 else random.choice(bokovye_for_shoot)
        elif len(bokovye_for_shoot) == 2:
            choice_of_bok_hit = random.choice([0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
            shoot = random.choice(korabl) if choice_of_bok_hit == 1 else random.choice(bokovye_for_shoot)
        elif len(bokovye_for_shoot) == 1:
            choice_of_bok_hit = random.choice([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
            shoot = random.choice(korabl) if choice_of_bok_hit == 1 else random.choice(bokovye_for_shoot)

        return shoot


def moove(bot_sheep, last_sheep, shoots, bokovye):
    logger.info(f"Файл: {__file__}, Функция: {inspect.currentframe().f_code.co_name}")
    if last_sheep == bot_sheep[-1]:
        available_shoots = [i for i in shoots if i not in bokovye]
        bot_sheep[-1] = random.choice(available_shoots)

    elif last_sheep in bot_sheep[3:5]:
        if last_sheep == bot_sheep[3]:
            last_sheep2 = bot_sheep[4]
        else:
            last_sheep2 = bot_sheep[3]
        available_shoots = []
        available_shoots.append(last_sheep2 + 5) if last_sheep2 + 5 in range(1, 26) else -1
        available_shoots.append(last_sheep2 - 5) if last_sheep2 - 5 in range(1, 26) else -1
        available_shoots.append(last_sheep2 + 1) if last_sheep2 + 1 <= math.ceil(last_sheep2 / 5) * 5 else -1
        available_shoots.append(last_sheep2 - 1) if (last_sheep2 - 1 <= math.ceil(last_sheep2 / 5) * 5 and last_sheep2 % 5 != 1) else -1
        available_shoots = [num for num in available_shoots if 1 <= num <= 25]
        available_shoots.remove(last_sheep)
        available_shoots = [i for i in available_shoots if i not in bokovye]
        new_placement = random.choice(available_shoots) if available_shoots else last_sheep

        bot_sheep[bot_sheep.index(last_sheep)] = new_placement

    elif last_sheep in bot_sheep[:3]:
        if last_sheep == bot_sheep[0]:
            last_sheep2 = bot_sheep[2]
        else:
            last_sheep2 = bot_sheep[0]

        available_shoots = []
        available_shoots.append(last_sheep2 + 5) if last_sheep2 + 5 in range(1, 26) else -1
        available_shoots.append(last_sheep2 - 5) if last_sheep2 - 5 in range(1, 26) else -1
        available_shoots.append(last_sheep2 + 1) if last_sheep2 + 1 <= math.ceil(last_sheep2 / 5) * 5 else -1
        available_shoots.append(last_sheep2 - 1) if (
                    last_sheep2 - 1 <= math.ceil(last_sheep2 / 5) * 5 and last_sheep2 % 5 != 1) else -1
        available_shoots = [i for i in available_shoots if i not in bokovye]
        available_shoots = [num for num in available_shoots if 1 <= num <= 25]
        a1 = abs(bot_sheep[1] - bot_sheep[0])
        new_placement = last_sheep
        for i in available_shoots:
            a2 = abs(bot_sheep[1] - i)/2
            if a1 == int(a2):
                new_placement = i
        bot_sheep[bot_sheep.index(last_sheep)] = new_placement

    return bot_sheep


#print(f'1  2  3  4  5')
#print(f'6  7  8  9  10')
#print(f'11 12 13 14 15')
#print(f'16 17 18 19 20')
#print(f'21 22 23 24 25')
#print()
#print(moove([1, 2, 3, 16, 21, 15], 1, [1, 2, 3, 20, 21, 22, 23, 24, 25], [11, 12, 17, 22, 14, 9, 10, 19, 20]))
