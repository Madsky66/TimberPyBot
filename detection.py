import logging
import pyautogui
import winsound

from PIL import Image, ImageGrab
from mss import mss

from init.const import BROWN
from state import State


def grab_images(zones):
    start_zone, top_zones, mid_zones, bot_zones = zones
    l_top_zone, r_top_zone = top_zones
    l_mid_zone, r_mid_zone = mid_zones
    l_bot_zone, r_bot_zone = bot_zones
    with mss() as sct:
        return {
            "start_zone": Image.frombytes("RGB", sct.grab(start_zone.rect).size, sct.grab(start_zone.rect).bgra, "raw", "BGRX"),
            "l_top": Image.frombytes("RGB", sct.grab(l_top_zone.rect).size, sct.grab(l_top_zone.rect).bgra, "raw", "BGRX"),
            "r_top": Image.frombytes("RGB", sct.grab(r_top_zone.rect).size, sct.grab(r_top_zone.rect).bgra, "raw", "BGRX"),
            "l_mid": Image.frombytes("RGB", sct.grab(l_mid_zone.rect).size, sct.grab(l_mid_zone.rect).bgra, "raw", "BGRX"),
            "r_mid": Image.frombytes("RGB", sct.grab(r_mid_zone.rect).size, sct.grab(r_mid_zone.rect).bgra, "raw", "BGRX"),
            "l_bot": Image.frombytes("RGB", sct.grab(l_bot_zone.rect).size, sct.grab(l_bot_zone.rect).bgra, "raw", "BGRX"),
            "r_bot": Image.frombytes("RGB", sct.grab(r_bot_zone.rect).size, sct.grab(r_bot_zone.rect).bgra, "raw", "BGRX"),
        }


def check_start(zones):
    start_base = Image.open("../res/img/zones/start/start_img.png")
    start_actual = grab_images(zones)["start_zone"]
    if list(start_base.getdata()) == list(start_actual.getdata()):
        winsound.Beep(1500, 250)
        pyautogui.press("space")


def dispatch(zones):
    state = State()
    while True:
        check_start(zones)
        l_mid_img = grab_images(zones)["l_mid"]
        r_mid_img = grab_images(zones)["r_mid"]
        if check(BROWN, 0, 1, l_mid_img) == 100:
            pyautogui.press("left")
            logging.info(" Branche détectée à droite")
            state.reset_all()
        elif check(BROWN, 0, 1, r_mid_img) == 100:
            pyautogui.press("right")
            logging.info(" Branche détectée à gauche")
            state.reset_all()


def check(color_to_check, tolerance, coverage, img):
    total_pixels = img.width * img.height
    matched_pixels = sum(
        is_color_match(img.getpixel((x, y)), color_to_check, tolerance)
        for y in range(img.height)
        for x in range(img.width)
    )
    result = ((matched_pixels / total_pixels) / coverage) * 100
    return result


def is_color_match(pixel_to_check, decomposed_colors, tolerance):
    if not isinstance(pixel_to_check, tuple) or len(pixel_to_check) != len(decomposed_colors):
        return False
    return all(
        abs(pixel_to_check[i] - decomposed_colors[i]) <= tolerance
        for i in range(len(decomposed_colors))
    )
