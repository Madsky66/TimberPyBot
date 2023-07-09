from pynput.mouse import Controller as MouseController
from PIL import ImageGrab
import threading
import time
import pyautogui


class ZoneParams:
    def __init__(self, x, y, width, height, sleep_time):
        self.rect = (x, y, x + width, y + height)
        self.sleep_time = sleep_time


class Bot:
    def __init__(self):
        self.mouse = MouseController()

        self.zones = [
            ZoneParams(1053, 575, 5, 1, 1),
            ZoneParams(843, 480, 1, 15, 1),
            ZoneParams(842, 515, 5, 1, 1)
        ]

        self.thread = threading.Thread(target=self.start)

    def move_mouse_to_zone(self, zone):
        target_x, target_y = zone.rect[0], zone.rect[1]
        self.mouse.position = (target_x, target_y)

    def start(self):
        time.sleep(3)

        for zone in self.zones:
            self.move_mouse_to_zone(zone)
            time.sleep(zone.sleep_time)
            color = check_color(zone.rect[0], zone.rect[1])
            print(f"Color at {zone.rect}: {color}")

    def run(self):
        self.thread.start()

    def stop(self):
        self.thread.join()


def check_color(x, y):
    bbox = (x, y, x + 1, y + 1)
    im = ImageGrab.grab(bbox=bbox)
    rgbim = im.convert('RGB')
    r, g, b = rgbim.getpixel((0, 0))
    print(f'COLOR: rgb{(r, g, b)} | HEX #{get_hex((r, g, b))}')
    return r, g, b


def get_hex(rgb):
    return ''.join(hex(c)[2:].zfill(2) for c in rgb)


if __name__ == '__main__':
    screen_width, screen_height = pyautogui.size()
    print(f"Résolution d'écran : {screen_width}x{screen_height}")
    print("Démarrage du script")
    bot = Bot()
    bot.run()