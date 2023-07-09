import logging
import threading
import time
from PIL import ImageGrab
from pynput.keyboard import Controller, Key

logging.basicConfig(level=logging.INFO)

COLOR_TO_DETECT = [(95, 41, 0)]
WHITE_COLOR = [(255, 255, 255)]
REQUIRED_CONFIRMATIONS = 3
FLASH_WAIT_TIME = 0.1
NONE_WAIT_TIME = 0.01


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
    return coverage >= zone_params.coverage


def check_game_state(left_zones, right_zones):
    left_active = any(detect_zone(zone, COLOR_TO_DETECT) for zone in left_zones)
    right_active = any(detect_zone(zone, COLOR_TO_DETECT) for zone in right_zones)
    if not left_active and not right_active:
        if all(detect_zone(zone, WHITE_COLOR) for zone in (left_zones + right_zones)):
            return "flash"
        else:
            return "none"
    elif left_active and right_active:
        print("Problème de détection : Les deux zones sont actives")
        return None
    elif left_active:
        print("Branche détectée à gauche")
        return "left"
    elif right_active:
        print("Branche détectée à droite")
        return "right"


class Bot:
    def __init__(self, left_zones, right_zones):
        self.keyboard = Controller()
        self.stop_detection_flag = False
        self.left_zones = left_zones
        self.right_zones = right_zones
        self.thread = threading.Thread(target=self.start)

    def start(self):
        none_confirmations = 0
        flash_confirmations = 0
        while not self.stop_detection_flag:
            try:
                game_state = check_game_state(self.left_zones, self.right_zones)
                if game_state == "left":
                    self.press_key(Key.right)
                elif game_state == "right":
                    self.press_key(Key.left)
                elif game_state == "flash":
                    flash_confirmations += 1
                    if flash_confirmations >= REQUIRED_CONFIRMATIONS:
                        print("Flash confirmé. Attente...")
                        flash_confirmations = 0
                        time.sleep(FLASH_WAIT_TIME)
                elif game_state == "none":
                    none_confirmations += 1
                    if none_confirmations >= REQUIRED_CONFIRMATIONS:
                        print("Jeu non détecté. Attente...")
                        none_confirmations = 0
                        time.sleep(NONE_WAIT_TIME)
                else:
                    flash_confirmations = 0
                    none_confirmations = 0
                time.sleep(1)
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
        self.thread.start()


if __name__ == "__main__":
    left_zones = [
        ZoneParams(1053, 575, 5, 1, COLOR_TO_DETECT, 0.1),
        ZoneParams(843, 480, 1, 15, COLOR_TO_DETECT, 0.75),
        ZoneParams(842, 515, 5, 1, COLOR_TO_DETECT, 0.1)
    ]
    right_zones = [
        ZoneParams(1051, 575, 5, 1, COLOR_TO_DETECT, 0.1),
        ZoneParams(843, 480, 1, 15, COLOR_TO_DETECT, 0.75),
        ZoneParams(842, 515, 5, 1, COLOR_TO_DETECT, 0.1)
    ]
    bot = Bot(left_zones, right_zones)
    bot.run()
