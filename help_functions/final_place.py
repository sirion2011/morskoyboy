import math
import random
import inspect
import logging


logger = logging.getLogger(__name__)


def place(field, longness, tryes, SHEEP:list):
    logger.info(f"Файл: {__file__}, Функция: {inspect.currentframe().f_code.co_name}")
    while True:
        tryes += 1
        a = random.choice(list(field.keys()))
        if field[a].isdigit():
            naprav = random.choice(['left', 'right', 'top', 'bottom'])
            ship = [a]
            if naprav == 'left':
                for i in range(longness - 1):
                    ship.append(ship[-1] - 1)
            elif naprav == 'right':
                for i in range(longness - 1):
                    ship.append(ship[-1] + 1)
            elif naprav == 'top':
                for i in range(longness - 1):
                    ship.append(ship[-1] + 5)
            elif naprav == 'bottom':
                for i in range(longness - 1):
                    ship.append(ship[-1] - 5)

            count = 0
            percent = 0 if naprav in ['top', 'bottom'] else 0
            for q in ship:
                if q < 1 or q > 25:
                    pass
                else:
                    count += 1

            if naprav in ['top', 'bottom']:
                skok = ship[0]%5
                for i in ship:
                    if i%5 == skok:
                        percent += 1
            else:
                one, two, three, four, five = 0, 0, 0, 0, 0
                for i in ship:
                    if i in [1, 2, 3, 4, 5]:
                        one += 1
                    elif i in [6, 7, 8, 9, 10]:
                        two += 1
                    elif i in [11, 12, 13, 14, 15]:
                        three += 1
                    elif i in [16, 17, 18, 19, 20]:
                        four += 1
                    elif i in [21, 22, 23, 24, 25]:
                        five += 1
                    for q in [one, two, three, four, five]:
                        if q == longness:
                            percent = longness

            ship_li = 0
            try:
                for i in ship:
                    if field[i].isdigit():
                        ship_li += 1
            except Exception as e:
                ship_li = 0

            if count == longness and percent == longness and ship_li == longness:
                ship = sorted(ship)
                break
            else:
                if tryes == 150:
                    return tryes, 0
        if tryes == 150:
            return tryes, 0


    bokovye_prav = []
    bokovye_lev = []
    bokovye_niz = []
    bokovye_vverh = []
    if naprav in ['top', 'bottom']:
        for q in ship:
            bokovye_prav.append(q+1) if q+1 <= math.ceil(q/5)*5 else -1
            bokovye_lev.append(q-1) if (q-1 <= math.ceil(q/5)*5 and q%5 != 1) else -1
        bokovye_niz.append(ship[-1]+5)
        bokovye_vverh.append(ship[0]-5)
        bokovye_niz.append(ship[-1]+5+1) if (ship[-1]+5 <= math.ceil((ship[-1]+5)/5)*5 and (ship[-1]+5)%5 != 0) else -1
        bokovye_niz.append(ship[0]-5+1) if (ship[0]-5 <= math.ceil((ship[0]-5)/5) * 5 and (ship[0]-5)%5 != 0 and (ship[0]-5) != 0) else -1

        bokovye_vverh.append(ship[-1]+5-1) if (ship[-1]+5 <= math.ceil((ship[-1]+5)/5)*5 and (ship[-1]+5)%5 != 1) else -1
        bokovye_vverh.append(ship[0]-5-1) if (ship[0]-5 <= math.ceil((ship[0]-5)/5)*5 and (ship[0]-5)%5 != 1) else -1

    elif naprav in ['left', 'right']:
        for q in ship:
            bokovye_vverh.append(q-5)
            bokovye_niz.append(q+5)

        bokovye_prav.append(ship[-1]-5+1) if (ship[-1]-5 <= math.ceil((ship[-1]-5)/5) * 5 and (ship[-1]-5)%5 != 0 and (ship[-1]-5) != 0) else -1
        bokovye_prav.append(ship[-1]+5+1) if (ship[-1]+5 <= math.ceil((ship[-1]+5)/5)*5 and (ship[-1]+5)%5 != 0) else -1

        bokovye_lev.append(ship[0]-5-1) if (ship[0]-5 <= math.ceil((ship[0]-5)/5)*5 and (ship[0]-5)%5 != 1) else -1
        bokovye_lev.append(ship[0]+5-1) if (ship[0]+5 <= math.ceil((ship[0]+5)/5)*5 and (ship[0]+5)%5 != 1) else -1

        bokovye_lev.append(ship[0]-1) if (ship[0]-1 <= math.ceil(ship[0]/5)*5 and ship[0]%5 != 1) else -1
        bokovye_prav.append(ship[-1]+1) if ship[-1]+1 <= math.ceil(ship[-1]/5)*5 else -1

    bokovye = bokovye_lev + bokovye_prav + bokovye_niz + bokovye_vverh
    bokovye = sorted(bokovye)
    bokovye = [num for num in bokovye if 1 <= num <= 25]
    for i in ship:
        field[i] = '❌'
    for i in bokovye:
        field[i] = '💦'
    for shi in ship:
        SHEEP.append(shi)

    return 0, 1, SHEEP


def final_place(field, tryes, ship_count, SHEEP):
    logger.info(f"Файл: {__file__}, Функция: {inspect.currentframe().f_code.co_name}")
    for i in range(1, 4)[::-1]:
        longness = i
        trye, ships, SHEEP = place(field, longness, tryes, SHEEP)
        ship_count += ships
        if trye == 150 or (i == 1 and ship_count != 3):
            tryes = 0
            field = {i: str(i) for i in range(1, 26)}
            ship_count = 0
            SHEEP = []
            final_place(field, tryes, ship_count, SHEEP)
