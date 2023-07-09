import logging
import threading
import time

import numpy as np
import pyautogui
import webcolors
import winsound
from PIL import ImageGrab
from pynput.mouse import Controller as MouseController

LOGGER_FORMAT = "%(asctime)s %(levelname)s:%(message)s"
logging.basicConfig(level=logging.INFO, format=LOGGER_FORMAT)

BASE_WAIT_TIME = 0.1
FLASH_WAIT_TIME = 0.5

WHITE_COLOR = np.array([255, 255, 255])
COLOR_TO_DETECT = np.array([95, 41, 0])
H_COVERAGE = 0.1
V_COVERAGE = 1


def is_color_match(color, target_color, tolerance=0):
    return np.all(np.abs(color - target_color) <= tolerance, axis=-1)


class Bot:
    hexcolor_output = None

    def __init__(self, left_zones, right_zones):
        self.thread = threading.Thread(target=self.start)
        self.stop_detection_flag = False
        self.left_zones = left_zones
        self.right_zones = right_zones
        self.confirmations = {"droite": 0, "gauche": 0}
        self.mouse = MouseController()

    def visualize_zones(self):
        zones = self.left_zones + self.right_zones
        for zone in zones:
            self.mouse.position = (zone.x, zone.y)
            time.sleep(0.5)
            self.mouse.position = ((zone.x + zone.width), (zone.y + zone.height))
            time.sleep(1)

    def detect_zone(self, zone_params, target_color, screenshot, tolerance=0):
        zone = screenshot.crop(zone_params.rect)
        zone.save("zone.png")
        # zone.show()
        zone_np = np.array(zone)
        total_pixels = zone.width * zone.height
        matched_pixels = np.sum(is_color_match(zone_np, target_color, tolerance))
        coverage = matched_pixels / total_pixels
        detected_color = zone.getpixel((0, 0))
        color_hex = webcolors.rgb_to_hex(detected_color)
        Bot.hexcolor_output = color_hex
        return coverage >= zone_params.coverage

    def check_game_state(self, left_zones, right_zones, screenshot):
        left_detected_colors = [zone for zone in left_zones if self.detect_zone(zone, COLOR_TO_DETECT, screenshot)]
        right_detected_colors = [zone for zone in right_zones if self.detect_zone(zone, COLOR_TO_DETECT, screenshot)]
        left_active = len(left_detected_colors) > 0
        right_active = len(right_detected_colors) > 0

        if left_active and not right_active:
            return "droite", left_detected_colors[0].color
        elif right_active and not left_active:
            return "gauche", right_detected_colors[0].color
        return None, None

    def handle_game_state(self, state, color):
        beep_params = {
            "droite": (1000, 350, 1500, 350),
            "gauche": (1000, 350, 500, 350),
        }
        wait_times = {
            "droite": BASE_WAIT_TIME,
            "gauche": BASE_WAIT_TIME,
        }
        for i in range(0, len(beep_params[state]), 2):
            winsound.Beep(beep_params[state][i], beep_params[state][i + 1])
            time.sleep(0.01)
        logging.warning(f" - {state.capitalize()} - Couleur : {color}")
        time.sleep(wait_times[state])

    def start(self):
        while not self.stop_detection_flag:
            screenshot = ImageGrab.grab()
            game_state, color = self.check_game_state(self.left_zones, self.right_zones, screenshot)
            if game_state is not None:
                self.handle_game_state(game_state, color)

    def stop(self):
        self.stop_detection_flag = True
        if self.thread.is_alive():
            self.thread.join()

    def run(self):
        logging.info(" Démarrage du script")
        time.sleep(1)
        self.visualize_zones()
        self.thread.start()

    def press_key(self, key_to_press):
        if key_to_press == "gauche":
            pyautogui.press('left')
            logging.info("Touche gauche pressée")
        elif key_to_press == "droite":
            pyautogui.press('right')
            logging.info("Touche droite pressée")


class ZoneParams:
    def __init__(self, x, y, width, height, color, coverage):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.coverage = coverage
        self.rect = (x, y, x + width, y + height)
        self.confirmations = 0


def main():
    left_zones = [
        ZoneParams(int(755 * 1.25), int(460 * 1.25), 12, 1, COLOR_TO_DETECT, H_COVERAGE),
        ZoneParams(int(759 * 1.25), int(480 * 1.25), 1, 20, COLOR_TO_DETECT, V_COVERAGE),
        ZoneParams(int(755 * 1.25), int(515 * 1.25), 12, 1, COLOR_TO_DETECT, H_COVERAGE)
    ]
    right_zones = [
        ZoneParams(int(839 * 1.25), int(460 * 1.25), 12, 1, COLOR_TO_DETECT, H_COVERAGE),
        ZoneParams(int(843 * 1.25), int(480 * 1.25), 1, 20, COLOR_TO_DETECT, V_COVERAGE),
        ZoneParams(int(839 * 1.25), int(515 * 1.25), 12, 1, COLOR_TO_DETECT, H_COVERAGE)
    ]
    bot = Bot(left_zones, right_zones)
    bot.run()


if __name__ == "__main__":
    main()
