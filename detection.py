import logging
import time
import numpy as np
import pyautogui
import winsound

from PIL import ImageGrab
from case import Case

from const import WHITE_COLOR, BROWN_COLOR, SUCCESS_CONFIRMATIONS, FAIL_CONFIRMATIONS, SUCCESS_WAIT, FLASH_WAIT, SHAKE_WAIT, FAIL_WAIT, MAIN_COVERAGE, SHAKE_COVERAGE


def run(zones, left_main_zone, right_main_zone):
    while True:
        main_zones, shake_zones = zones
        if check("flash", WHITE_COLOR, main_zones, 32):
            handle_action(Case.FLASH)
        else:
            if check("left", BROWN_COLOR, [left_main_zone], 0):
                handle_action(Case.LEFT)
            elif check("right", BROWN_COLOR, [right_main_zone], 0):
                handle_action(Case.RIGHT)
            elif not check("shake", BROWN_COLOR, shake_zones, 0):
                handle_action(Case.SHAKE)
            else:
                handle_action(Case.ERROR)


def check(case, color_to_check, zones_to_check, tolerance):
    with ImageGrab.grab() as screenshot:
        for zone in zones_to_check:
            zone = screenshot.crop(zone.rect)
            zone.show()
            zone.save("zone.png")
            total_pixels = zone.width * zone.height
            np_zone = np.array(zone)
            if tolerance > 0:
                matched_pixels = np.sum(np.all((np_zone == color_to_check) <= tolerance, -1))
            else:
                matched_pixels = np.sum(np.all(np_zone == color_to_check, -1))
            if case == "shake":
                if (matched_pixels / total_pixels) >= SHAKE_COVERAGE:
                    return True
            else:
                if (matched_pixels / total_pixels) >= MAIN_COVERAGE:
                    return True
        return False


def handle_action(case):
    confirmations_counter = {Case.LEFT: 0, Case.RIGHT: 0, Case.FLASH: 0, Case.SHAKE: 0, Case.ERROR: 0}
    confirmations = {
        Case.LEFT: ("left", "right", " Branche détectée à droite", " DROITE -> "),
        Case.RIGHT: ("right", "left", " Branche détectée à gauche", " GAUCHE -> "),
        Case.FLASH: ("flash", None, " Flash en cours...", " FLASH -> "),
        Case.SHAKE: ("shake", None, " Tremblement en cours...", " SHAKE -> "),
        Case.ERROR: ("error", None, " - ERREUR -", " ERREUR -> "),
    }
    _type, _action, _confirmed_message, _incremented_message = confirmations[case]
    if confirmations[_type] == (SUCCESS_CONFIRMATIONS if case in [Case.LEFT, Case.RIGHT] else FAIL_CONFIRMATIONS):
        logging.info(_confirmed_message)
        if case in [Case.LEFT, Case.RIGHT]:
            time.sleep(SUCCESS_WAIT)
            pyautogui.press(_action)
            confirmations_counter[_type] = 0
        elif case == Case.FLASH:
            winsound.Beep(1500, 250)
            time.sleep(FLASH_WAIT)
            confirmations_counter[_type] = 0
        elif case == Case.SHAKE:
            winsound.Beep(500, 250)
            time.sleep(SHAKE_WAIT)
            confirmations_counter[_type] = 0
        else:
            winsound.Beep(250, 250)
            time.sleep(FAIL_WAIT)
            confirmations_counter[_type] = 0
    else:
        confirmations_counter[_type] += 1
        for other_case in confirmations:
            if other_case != case:
                confirmations[confirmations[other_case][0]] = 0
        logging.info(_incremented_message + str(confirmations[_type]))
