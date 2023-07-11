import logging
import sys
import time
import numpy as np
import pyautogui
import winsound

from enum import Enum
from PIL import ImageGrab
from collections import defaultdict
from pynput.keyboard import Controller
from pynput.mouse import Controller as MouseController

from const import WHITE_COLOR, BROWN_COLOR, SUCCESS_CONFIRMATIONS, FAIL_CONFIRMATIONS, SUCCESS_WAIT, FLASH_WAIT, SHAKE_WAIT, FAIL_WAIT, MAIN_COVERAGE, SHAKE_COVERAGE


class Case(Enum):
    ERROR = "error"
    LEFT = "left"
    RIGHT = "right"
    FLASH = "flash"
    SHAKE = "shake"


class Zone:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = (x, y, x + width, y + height)


class Bot:
    def __init__(self, zones, left_main_zone, right_main_zone, shake_zones):
        self.stop_detection_flag = False
        self.mouse = MouseController()
        self.keyboard = Controller()
        self.confirmations = defaultdict(int)
        self.zones = zones
        self.left_main_zone = left_main_zone
        self.right_main_zone = right_main_zone
        self.shake_zones = shake_zones


def run(zones, left_main_zone, right_main_zone, shake_zones):
    try:
        if check("flash", zones, WHITE_COLOR, 32):
            handle_action(Case.FLASH)
        else:
            if check("left", left_main_zone, BROWN_COLOR, 0):
                handle_action(Case.LEFT)
            elif check("right", right_main_zone, BROWN_COLOR, 0):
                handle_action(Case.RIGHT)
            elif not check("shake", shake_zones, BROWN_COLOR, 0):
                handle_action(Case.SHAKE)
            else:
                handle_action(Case.ERROR)
    except Exception as e:
        logging.error(f"Une erreur est survenue : {e}")
        sys.exit(1)


def check(case, color_to_check, zone_to_check, tolerance):
    try:
        screenshot = ImageGrab.grab()
        zone = screenshot.crop(zone_to_check)
        zone.show()
        zone.save("zone.png")
        total_pixels = zone.width * zone.height
        np_zone = np.array(zone)
        if tolerance > 0:
            matched_pixels = np.sum(np.all((np_zone == color_to_check) <= tolerance, -1))
        else:
            matched_pixels = np.sum(np.all(np_zone == color_to_check, -1))
        if case == "shake":
            return (matched_pixels / total_pixels) >= SHAKE_COVERAGE
        else:
            return (matched_pixels / total_pixels) >= MAIN_COVERAGE
    except Exception as e:
        logging.error(f"Une erreur est survenue : {e}")
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
    if confirmations_counter[_type] == (SUCCESS_CONFIRMATIONS if case in [Case.LEFT, Case.RIGHT] else FAIL_CONFIRMATIONS):
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
