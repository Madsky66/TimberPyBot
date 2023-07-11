import logging
import time
import pyautogui
import winsound

from PIL import ImageGrab
from case import Case

from const import WHITE_COLOR, BROWN_COLOR, SUCCESS_CONFIRMATIONS, FAIL_CONFIRMATIONS, SUCCESS_WAIT, FLASH_WAIT, SHAKE_WAIT, FAIL_WAIT, MAIN_COVERAGE, SHAKE_COVERAGE


def run(zones, left_main_zone, right_main_zone):
    confirmations_counter = {Case.LEFT: 0, Case.RIGHT: 0, Case.FLASH: 0, Case.SHAKE: 0, Case.ERROR: 0}
    while True:
        main_zones, shake_zones = zones
        if check("flash", WHITE_COLOR, main_zones, tolerance=16):
            handle_action(Case.FLASH, confirmations_counter)
        else:
            if check("left", BROWN_COLOR, [left_main_zone], tolerance=0):
                handle_action(Case.LEFT, confirmations_counter)
            elif check("right", BROWN_COLOR, [right_main_zone], tolerance=0):
                handle_action(Case.RIGHT, confirmations_counter)
            elif not check("shake", BROWN_COLOR, shake_zones, tolerance=0):
                handle_action(Case.SHAKE, confirmations_counter)
            else:
                handle_action(Case.ERROR, confirmations_counter)


def check(case, color_to_check, zones, tolerance):
    for zone_list in zones:
        for zone in zone_list:
            zone_image = ImageGrab.grab(zone.rect)

            total_pixels = zone_image.width * zone_image.height
            matched_pixels = sum(
                is_color_match(zone_image.getpixel((x, y)), color_to_check, tolerance)
                for y in range(zone_image.height)
                for x in range(zone_image.width)
            )

            if case == Case.SHAKE:
                if (matched_pixels / total_pixels) >= SHAKE_COVERAGE:
                    return True
            else:
                if (matched_pixels / total_pixels) >= MAIN_COVERAGE:
                    return True

    return False


def is_color_match(pixel_to_check, decomposed_colors, tolerance):
    if not isinstance(pixel_to_check, tuple) or len(pixel_to_check) != len(decomposed_colors):
        return False

    return all(
        abs(pixel_to_check[i] - decomposed_colors[i]) <= tolerance
        for i in range(len(decomposed_colors))
    )


def handle_action(case, counter):
    confirmations = {
        Case.LEFT: ("left", "right", " Branche détectée à droite", " DROITE -> "),
        Case.RIGHT: ("right", "left", " Branche détectée à gauche", " GAUCHE -> "),
        Case.FLASH: ("flash", None, " Flash en cours...", " FLASH -> "),
        Case.SHAKE: ("shake", None, " Tremblement en cours...", " SHAKE -> "),
        Case.ERROR: ("error", None, " - ERREUR -", " ERREUR -> "),
    }
    _action, _confirmed_message, _incremented_message = confirmations[case][1:]

    if counter[case] == (SUCCESS_CONFIRMATIONS if case in [Case.LEFT, Case.RIGHT] else FAIL_CONFIRMATIONS):
        logging.info(_confirmed_message)
        if case in [Case.LEFT, Case.RIGHT]:
            logging.info("Branche détectée")
            time.sleep(SUCCESS_WAIT)
            pyautogui.press(_action)
            counter[case] = 0
        elif case == Case.FLASH:
            logging.info("Flash détecté")
            winsound.Beep(1500, 250)
            time.sleep(FLASH_WAIT)
            counter[case] = 0
        elif case == Case.SHAKE:
            logging.info("Tremblement détecté")
            winsound.Beep(500, 250)
            time.sleep(SHAKE_WAIT)
            counter[case] = 0
        else:
            logging.info("Jeu non détecté")
            winsound.Beep(250, 250)
            time.sleep(FAIL_WAIT)
            counter[case] = 0
    else:
        counter[case] += 1
        for other_case in confirmations:
            if other_case != case:
                counter[other_case] = 0
        logging.info(_incremented_message + str(confirmations[case]))
