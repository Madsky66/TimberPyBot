import logging
import threading
import webcolors
import winsound
import time
import numpy as np

from PIL import ImageGrab
from pynput.keyboard import Controller, Key
from pynput.mouse import Controller as MouseController

logging.basicConfig(level=logging.INFO)

COLOR_TO_DETECT = np.array([95, 41, 0])
WHITE_COLOR = np.array([255, 255, 255])
REQUIRED_CONFIRMATIONS = 3
BASE_WAIT_TIME = 0.1
FLASH_WAIT_TIME = 0.1
NONE_WAIT_TIME = 0.01
BOTH_WAIT_TIME = 0.05

global hexcolor_output


def beep(frequency, duration):
    winsound.Beep(frequency, duration)


class ColorDetectionError(Exception):
    pass


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


def is_color_match(color, target_color):
    return np.all(color == target_color, axis=-1)


def detect_zone(zone_params, target_color, screenshot):
    zone = screenshot.crop(zone_params.rect)
    # zone.save("zone.png")
    zone_np = np.array(zone)
    total_pixels = zone.width * zone.height
    matched_pixels = np.sum(is_color_match(zone_np, target_color))
    coverage = matched_pixels / total_pixels
    detected_color = zone.getpixel((0, 0))
    color_hex = webcolors.rgb_to_hex(detected_color)
    Bot.hexcolor_output = color_hex
    # zone.show()
    return coverage >= zone_params.coverage


def check_game_state(left_zones, right_zones, screenshot):
    left_detected_colors = [zone for zone in left_zones if detect_zone(zone, COLOR_TO_DETECT, screenshot)]
    right_detected_colors = [zone for zone in right_zones if detect_zone(zone, COLOR_TO_DETECT, screenshot)]
    left_active = len(left_detected_colors) > 0
    right_active = len(right_detected_colors) > 0
    if not left_active and not right_active:
        if all(detect_zone(zone, WHITE_COLOR, screenshot) for zone in (left_zones + right_zones)):
            return "flash", None
        else:
            return "aucun", "Jeu non actif"
    elif left_active and right_active:
        left_color = left_detected_colors[0].color if left_detected_colors else None
        right_color = right_detected_colors[0].color if right_detected_colors else None
        return "double", (left_color, right_color)
    elif left_active:
        return "gauche", left_detected_colors[0].color
    elif right_active:
        return "droite", right_detected_colors[0].color


class Bot:
    hexcolor_output = None

    def __init__(self, left_zones, right_zones):
        self.keyboard = Controller()
        self.stop_detection_flag = False
        self.left_zones = left_zones
        self.right_zones = right_zones
        self.confirmations = {"flash": 0, "aucun": 0, "double": 0, "gauche": 0, "droite": 0}
        self.mouse = MouseController()

    # def visualize_zones(self):
    #     zones = self.left_zones + self.right_zones
    #     for zone in zones:
    #         self.mouse.position = (zone.x / 1.25, zone.y / 1.25)
    #         time.sleep(0.5)
    #         self.mouse.position = ((zone.x + zone.width) / 1.25, (zone.y + zone.height) / 1.25)
    #         time.sleep(1)

    def handle_game_state(self, state, color):
        beep_params = {
            "gauche": (1000, 500, 1500, 250),
            "droite": (1000, 500, 500, 250),
            "flash": (1500, 500, 1500, 250),
            "aucun": (250, 500),
            "double": (100, 500),
        }

        wait_times = {
            "gauche": BASE_WAIT_TIME,
            "droite": BASE_WAIT_TIME,
            "flash": FLASH_WAIT_TIME,
            "aucun": NONE_WAIT_TIME,
            "double": BOTH_WAIT_TIME,
        }
        keys_to_press = {
            "gauche": Key.right,
            "droite": Key.left,
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
                screenshot = ImageGrab.grab()
                game_state, color = check_game_state(self.left_zones, self.right_zones, screenshot)
                self.handle_game_state(game_state, color)
            except Exception as e:
                raise ColorDetectionError("Une exception s'est produite lors de la détection de la couleur") from e

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
        # self.visualize_zones()
        self.thread = threading.Thread(target=self.start)
        self.thread.start()


def main():
    left_zones = [
        ZoneParams(int(755 * 1.25), int(460 * 1.25), int(12), int(1), COLOR_TO_DETECT, 0.1),
        ZoneParams(int(759 * 1.25), int(480 * 1.25), int(1), int(20), COLOR_TO_DETECT, 0.75),
        ZoneParams(int(755 * 1.25), int(515 * 1.25), int(12), int(1), COLOR_TO_DETECT, 0.1)
    ]

    right_zones = [
        ZoneParams(int(839 * 1.25), int(460 * 1.25), int(12), int(1), COLOR_TO_DETECT, 0.1),
        ZoneParams(int(843 * 1.25), int(480 * 1.25), int(1), int(20), COLOR_TO_DETECT, 0.75),
        ZoneParams(int(839 * 1.25), int(515 * 1.25), int(12), int(1), COLOR_TO_DETECT, 0.1)
    ]
    bot = Bot(left_zones, right_zones)
    bot.run()


if __name__ == "__main__":
    main()
