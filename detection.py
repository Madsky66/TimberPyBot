import logging
import time

import pyautogui
import numpy as np
from PIL import Image
from mss import mss


class Zone:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = (x, y, x + width, y + height)


BROWN = np.array([95, 41, 0])

L_TOP = Zone(int(944), int(575), 10, 1).rect
R_TOP = Zone(int(1048), int(575), 10, 1).rect
L_MID = Zone(int(949), int(600), 1, 20).rect
R_MID = Zone(int(1053), int(600), 1, 20).rect


def grab_images(zone):
    with mss() as sct:
        return Image.frombytes("RGB", sct.grab(zone.rect).size, sct.grab(zone.rect).bgra, "raw", "BGRX")


def dispatch():
    logging.info(" Initialisation du bot...")
    time.sleep(0.5)

    logging.info(" Lancement de la détection...")
    time.sleep(0.5)

    while True:
        if check(BROWN, 0, 1, grab_images(L_MID)) == 100:
            pyautogui.press("left")
        elif check(BROWN, 0, 1, grab_images(R_MID)) == 100:
            pyautogui.press("right")


def check(color_to_check, tolerance, coverage, img):
    img_np = np.array(img)
    total_pixels = img_np.shape[0] * img_np.shape[1]
    matched_pixels = np.sum(np.all(np.abs(img_np - color_to_check) <= tolerance, axis=2))
    result = ((matched_pixels / total_pixels) / coverage) * 100
    return result


def is_color_match(pixel_to_check, decomposed_colors, tolerance):
    if not isinstance(pixel_to_check, tuple) or len(pixel_to_check) != len(decomposed_colors):
        return False
    return all(
        abs(pixel_to_check[i] - decomposed_colors[i]) <= tolerance
        for i in range(len(decomposed_colors))
    )
