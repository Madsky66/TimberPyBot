import logging
import threading
import time
import traceback

import numpy as np
import pyautogui
import webcolors
import winsound
from PIL import ImageGrab
from pynput.keyboard import Controller, Key
from pynput.mouse import Controller as MouseController

LOGGER_FORMAT = "%(asctime)s %(levelname)s:%(message)s"
LOGGER_FILE = "bot.log"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter(LOGGER_FORMAT)
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)

file_handler = logging.FileHandler(LOGGER_FILE)
file_handler.setLevel(logging.INFO)
file_format = logging.Formatter(LOGGER_FORMAT)
file_handler.setFormatter(file_format)
logger.addHandler(file_handler)

logging.basicConfig(filename=LOGGER_FILE, level=logging.INFO, format=LOGGER_FORMAT)

H_COVERAGE = 0.1
V_COVERAGE = 1

BASE_WAIT_TIME = 0.1
FLASH_WAIT_TIME = 0.1
NONE_WAIT_TIME = 0.01
BOTH_WAIT_TIME = 0.05

COLOR_TO_DETECT = np.array([95, 41, 0])
WHITE_COLOR = np.array([255, 255, 255])

global hexcolor_output


class ColorDetectionError(Exception):
    pass


def beep(frequency, duration):
    winsound.Beep(frequency, duration)


def is_color_match(color, target_color, tolerance=0):
    return np.all(np.abs(color - target_color) <= tolerance, axis=-1)


class Bot:
    hexcolor_output = None

    def __init__(self, left_zones, right_zones):
        self.thread = threading.Thread(target=self.start)
        self.keyboard = Controller()
        self.stop_detection_flag = False
        self.left_zones = left_zones
        self.right_zones = right_zones
        self.confirmations = {"flash": 0, "aucun": 0, "double": 0, "gauche": 0, "droite": 0}
        self.mouse = MouseController()

    def visualize_zones(self):
        zones = self.left_zones + self.right_zones
        for zone in zones:
            self.mouse.position = (zone.x, zone.y)
            time.sleep(0.5)
            self.mouse.position = ((zone.x + zone.width), (zone.y + zone.height))
            time.sleep(1)

    def detect_zone(self, zone_params, target_color, screenshot, tolerance=0):
        try:
            zone = screenshot.crop(zone_params.rect)
            zone_np = np.array(zone)
            total_pixels = zone.width * zone.height
            matched_pixels = np.sum(is_color_match(zone_np, target_color, tolerance))
            if np.array_equal(target_color, WHITE_COLOR):
                return matched_pixels / total_pixels > 0.75
            else:
                coverage = matched_pixels / total_pixels
                detected_color = zone.getpixel((0, 0))
                color_hex = webcolors.rgb_to_hex(detected_color)
                Bot.hexcolor_output = color_hex
                return coverage >= zone_params.coverage
        except Exception as e:
            logging.error(f"Erreur lors de la détection de la zone : {str(e)}")
            logging.error(traceback.format_exc())
            raise

    def check_game_state(self, left_zones, right_zones, screenshot):
        try:
            left_detected_colors = [zone for zone in left_zones if self.detect_zone(zone, COLOR_TO_DETECT, screenshot)]
            right_detected_colors = [zone for zone in right_zones if self.detect_zone(zone, COLOR_TO_DETECT, screenshot)]
            left_active = len(left_detected_colors) > 0
            right_active = len(right_detected_colors) > 0
            if not left_active and not right_active:
                if all(self.detect_zone(zone, WHITE_COLOR, screenshot, tolerance=128) for zone in (left_zones + right_zones)):
                    return "flash", None
                else:
                    return "aucun", "Jeu non actif"
            elif left_active and right_active:
                return "double", (left_detected_colors[0].color, right_detected_colors[0].color)
            elif left_active:
                return "droite", left_detected_colors[0].color
            elif right_active:
                return "gauche", right_detected_colors[0].color
        except Exception as e:
            logging.error(f"Erreur lors de la vérification de l'état du jeu : {str(e)}")
            logging.error(traceback.format_exc())
            raise

    def handle_game_state(self, state, color):
        try:
            CONFIRMATIONS_REQUIRED = {
                "droite": 1,
                "gauche": 1,
                "flash": 3,
                "aucun": 1,
                "double": 3,
            }

            beep_params = {
                "droite": (1000, 500, 1500, 250),
                "gauche": (1000, 500, 500, 250),
                "flash": (1500, 500, 1500, 250),
                "aucun": (250, 500),
                "double": (100, 500),
            }

            wait_times = {
                "droite": BASE_WAIT_TIME,
                "gauche": BASE_WAIT_TIME,
                "flash": FLASH_WAIT_TIME,
                "aucun": NONE_WAIT_TIME,
                "double": BOTH_WAIT_TIME,
            }

            keys_to_press = {
                "droite": Key.left,
                "gauche": Key.right,
            }

            self.confirmations[state] += 1
            if self.confirmations[state] >= CONFIRMATIONS_REQUIRED[state]:
                logging.warning(f" - {state.capitalize()} - Couleur : {color}")
                for i in range(0, len(beep_params[state]), 2):
                    beep(beep_params[state][i], beep_params[state][i + 1])
                    time.sleep(0.01)
                self.confirmations = {key: 0 for key in self.confirmations}
                time.sleep(wait_times[state])
            if state in keys_to_press and self.confirmations[state] >= CONFIRMATIONS_REQUIRED[state]:
                self.press_key(keys_to_press[state])
        except Exception as e:
            logging.error(f"Erreur lors de la gestion de l'état du jeu : {str(e)}")
            logging.error(traceback.format_exc())
            raise

    def start(self):
        while not self.stop_detection_flag:
            try:
                screenshot = ImageGrab.grab()
                game_state, color = self.check_game_state(self.left_zones, self.right_zones, screenshot)
                self.handle_game_state(game_state, color)
            except ColorDetectionError as e:
                logging.error(f"Une exception s'est produite lors de la détection de la couleur: {str(e)}")
                self.stop()
            except Exception as e:
                logging.error(f"Erreur lors de l'exécution du bot : {str(e)}")
                logging.error(traceback.format_exc())
                self.stop()

    def press_key(self, direction):
        try:
            if direction == Key.left:
                pyautogui.press('left')
                logging.info("Touche gauche pressée")
            elif direction == Key.right:
                pyautogui.press('right')
                logging.info("Touche droite pressée")
        except Exception as e:
            logging.error(f"Erreur lors de la pression de la touche {direction} : {str(e)}")
            logging.error(traceback.format_exc())
            raise

    def stop(self):
        self.stop_detection_flag = True
        if self.thread.is_alive():
            self.thread.join()

    def run(self):
        logging.info("Démarrage du script")
        time.sleep(1)
        self.visualize_zones()
        self.thread.start()
