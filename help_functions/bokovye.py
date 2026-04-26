import math
import inspect
import logging


logger = logging.getLogger(__name__)


def bokkovye(ship: list):
    logger.info(f"Файл: {__file__}, Функция: {inspect.currentframe().f_code.co_name}")
    if len(ship) == 3:
        percent = abs(ship[-1] - ship[-2])
    elif len(ship) == 2:
        percent = abs(ship[-1] - ship[0])
    else:
        percent = 0

    if percent == 5:
        naprav = 'top'
    elif percent == 1:
        naprav = 'left'
    else:
        naprav = 'top'
    bokovye_prav = []
    bokovye_lev = []
    bokovye_niz = []
    bokovye_vverh = []
    if naprav in ['top', 'bottom']:
        for q in ship:
            bokovye_prav.append(q + 1) if q + 1 <= math.ceil(q / 5) * 5 else -1
            bokovye_lev.append(q - 1) if (q - 1 <= math.ceil(q / 5) * 5 and q % 5 != 1) else -1
        bokovye_niz.append(ship[-1] + 5)
        bokovye_vverh.append(ship[0] - 5)
        bokovye_niz.append(ship[-1] + 5 + 1) if (
                    ship[-1] + 5 <= math.ceil((ship[-1] + 5) / 5) * 5 and (ship[-1] + 5) % 5 != 0) else -1
        bokovye_niz.append(ship[0] - 5 + 1) if (
                    ship[0] - 5 <= math.ceil((ship[0] - 5) / 5) * 5 and (ship[0] - 5) % 5 != 0 and (
                        ship[0] - 5) != 0) else -1

        bokovye_vverh.append(ship[-1] + 5 - 1) if (
                    ship[-1] + 5 <= math.ceil((ship[-1] + 5) / 5) * 5 and (ship[-1] + 5) % 5 != 1) else -1
        bokovye_vverh.append(ship[0] - 5 - 1) if (
                    ship[0] - 5 <= math.ceil((ship[0] - 5) / 5) * 5 and (ship[0] - 5) % 5 != 1) else -1

    elif naprav in ['left', 'right']:
        for q in ship:
            bokovye_vverh.append(q - 5)
            bokovye_niz.append(q + 5)

        bokovye_prav.append(ship[-1] - 5 + 1) if (
                    ship[-1] - 5 <= math.ceil((ship[-1] - 5) / 5) * 5 and (ship[-1] - 5) % 5 != 0 and (
                        ship[-1] - 5) != 0) else -1
        bokovye_prav.append(ship[-1] + 5 + 1) if (
                    ship[-1] + 5 <= math.ceil((ship[-1] + 5) / 5) * 5 and (ship[-1] + 5) % 5 != 0) else -1

        bokovye_lev.append(ship[0] - 5 - 1) if (
                    ship[0] - 5 <= math.ceil((ship[0] - 5) / 5) * 5 and (ship[0] - 5) % 5 != 1) else -1
        bokovye_lev.append(ship[0] + 5 - 1) if (
                    ship[0] + 5 <= math.ceil((ship[0] + 5) / 5) * 5 and (ship[0] + 5) % 5 != 1) else -1

        bokovye_lev.append(ship[0] - 1) if (ship[0] - 1 <= math.ceil(ship[0] / 5) * 5 and ship[0] % 5 != 1) else -1
        bokovye_prav.append(ship[-1] + 1) if ship[-1] + 1 <= math.ceil(ship[-1] / 5) * 5 else -1

    bokovye = bokovye_lev + bokovye_prav + bokovye_niz + bokovye_vverh
    bokovye = sorted(bokovye)
    bokovye = [num for num in bokovye if 1 <= num <= 25]
    return bokovye
