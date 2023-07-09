import logging
import threading
import webcolors

from PIL import ImageGrab

from pynput.keyboard import Controller, Key
from pynput.mouse import Controller as MouseController

import winsound
import time

logging.basicConfig(level=logging.INFO)

COLOR_TO_DETECT = [(95, 41, 0)]
WHITE_COLOR = [(255, 255, 255)]
REQUIRED_CONFIRMATIONS = 3
BASE_WAIT_TIME = 0.1
FLASH_WAIT_TIME = 0.1
NONE_WAIT_TIME = 0.01
BOTH_WAIT_TIME = 0.05

global hexcolor_output


def beep(frequency, duration):
    winsound.Beep(frequency, duration)


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


def is_color_match(color, target_colors, threshold=1):
    return any(
        abs(color[0] - target_color[0]) <= threshold and
        abs(color[1] - target_color[1]) <= threshold and
        abs(color[2] - target_color[2]) <= threshold
        for target_color in target_colors
    )


def detect_zone(zone_params, target_colors):
    zone = ImageGrab.grab(bbox=zone_params.rect)
    total_pixels = zone.width * zone.height
    matched_pixels = sum(
        is_color_match(zone.getpixel((x, y)), target_colors)
        for y in range(zone.height)
        for x in range(zone.width)
    )
    coverage = matched_pixels / total_pixels
    detected_color = zone.getpixel((0, 0))
    color_hex = webcolors.rgb_to_hex(detected_color)
    Bot.hexcolor_output = color_hex
    return coverage >= zone_params.coverage


def check_game_state(left_zones, right_zones):
    left_detected_colors = [zone for zone in left_zones if detect_zone(zone, COLOR_TO_DETECT)]
    right_detected_colors = [zone for zone in right_zones if detect_zone(zone, COLOR_TO_DETECT)]
    left_active = len(left_detected_colors) > 0
    right_active = len(right_detected_colors) > 0
    if not left_active and not right_active:
        if all(detect_zone(zone, WHITE_COLOR) for zone in (left_zones + right_zones)):
            return "flash", None
        else:
            return "none", None
    elif left_active and right_active:
        left_color = left_detected_colors[0].color if left_detected_colors else None
        right_color = right_detected_colors[0].color if right_detected_colors else None
        return "both", (left_color, right_color)
    elif left_active:
        return "left", left_detected_colors[0].color
    elif right_active:
        return "right", right_detected_colors[0].color


class Bot:
    hexcolor_output = None

    def __init__(self, left_zones, right_zones):
        self.keyboard = Controller()
        self.stop_detection_flag = False
        self.left_zones = left_zones
        self.right_zones = right_zones
        self.thread = threading.Thread(target=self.start)
        self.confirmations = {"flash": 0, "none": 0, "both": 0, "left": 0, "right": 0}
        self.mouse = MouseController()

    def visualize_zones(self):
        zones = self.left_zones + self.right_zones
        for zone in zones:
            self.mouse.position = (zone.x / 1.25, zone.y / 1.25)
            time.sleep(0.5)
            self.mouse.position = ((zone.x + zone.width) / 1.25, (zone.y + zone.height) / 1.25)
            time.sleep(1)

    def handle_game_state(self, state, color):
        beep_params = {
            "left": (1000, 500, 1500, 250),
            "right": (1000, 500, 500, 250),
            "flash": (1500, 500, 1500, 250),
            "none": (250, 500),
            "both": (100, 500),
        }

        wait_times = {
            "left": BASE_WAIT_TIME,
            "right": BASE_WAIT_TIME,
            "flash": FLASH_WAIT_TIME,
            "none": NONE_WAIT_TIME,
            "both": BOTH_WAIT_TIME,
        }
        keys_to_press = {
            "left": Key.right,
            "right": Key.left,
        }

        self.confirmations[state] += 1
        if self.confirmations[state] >= REQUIRED_CONFIRMATIONS:
            logging.warning(f" - {state.capitalize()} - Couleur : {color}")
            for i in range(0, len(beep_params[state]), 2):
                beep(beep_params[state][i], beep_params[state][i+1])
                time.sleep(0.01)
            self.confirmations = {key: 0 for key in self.confirmations}
            time.sleep(wait_times[state])

        if state in keys_to_press and self.confirmations[state] >= REQUIRED_CONFIRMATIONS:
            self.press_key(keys_to_press[state])

    def start(self):
        while not self.stop_detection_flag:
            try:
                game_state, color = check_game_state(self.left_zones, self.right_zones)
                self.handle_game_state(game_state, color)
            except Exception as e:
                print(f"Une exception s'est produite : {e}")

    def press_key(self, key):
        self.keyboard.press(key)
        time.sleep(0.01)
        self.keyboard.release(key)

    def stop(self):
        self.stop_detection_flag = True
        if self.thread.is_alive():
            self.thread.join()

    def run(self):
        logging.info("Démarrage du script")
        time.sleep(1)
        self.visualize_zones()
        self.thread.start()


def main():
    left_zones = [
        ZoneParams(int(753 * 1.25), int(460 * 1.25), int(10), int(1), COLOR_TO_DETECT, 0.1),
        ZoneParams(int(758 * 1.25), int(480 * 1.25), int(1), int(20), COLOR_TO_DETECT, 0.75),
        ZoneParams(int(753 * 1.25), int(515 * 1.25), int(10), int(1), COLOR_TO_DETECT, 0.1)
    ]

    right_zones = [
        ZoneParams(int(838 * 1.25), int(460 * 1.25), int(20), int(1), COLOR_TO_DETECT, 0.1),
        ZoneParams(int(843 * 1.25), int(480 * 1.25), int(1), int(20), COLOR_TO_DETECT, 0.75),
        ZoneParams(int(838 * 1.25), int(515 * 1.25), int(20), int(1), COLOR_TO_DETECT, 0.1)
    ]
    bot = Bot(left_zones, right_zones)
    bot.run()


if __name__ == "__main__":
    main()