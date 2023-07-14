import pyautogui
import time

from PIL import ImageGrab

from detection import Launcher


def get_mous_pos(zones):
    # time.sleep(3)
    while True:
        x, y = pyautogui.position()
        bbox = (x, y, x + 1, y + 1)
        im = ImageGrab.grab(bbox=bbox)
        rgbim = im.convert('RGB')
        r, g, b = rgbim.getpixel((0, 0))
        color = r, g, b
        print(f"Position de la souris : X={x}, Y={y} | Couleur : {color} | HEX #{get_hex((r, g, b))}")
        time.sleep(0.25)


def get_hex(rgb):
    return ''.join(hex(c)[2:].zfill(2) for c in rgb)


if __name__ == "__main__":
    launcher = Launcher()
    get_mous_pos(launcher.zones)
