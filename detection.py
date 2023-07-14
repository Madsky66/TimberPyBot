import pyautogui

from PIL import Image
from mss import mss

BROWN = (95, 41, 0)


def grab_images(zones):
    top_zones, mid_zones = zones
    l_top_zone, r_top_zone = top_zones
    l_mid_zone, r_mid_zone = mid_zones
    with mss() as sct:
        return {
            "l_top": Image.frombytes("RGB", sct.grab(l_top_zone.rect).size, sct.grab(l_top_zone.rect).bgra, "raw", "BGRX"),
            "r_top": Image.frombytes("RGB", sct.grab(r_top_zone.rect).size, sct.grab(r_top_zone.rect).bgra, "raw", "BGRX"),
            "l_mid": Image.frombytes("RGB", sct.grab(l_mid_zone.rect).size, sct.grab(l_mid_zone.rect).bgra, "raw", "BGRX"),
            "r_mid": Image.frombytes("RGB", sct.grab(r_mid_zone.rect).size, sct.grab(r_mid_zone.rect).bgra, "raw", "BGRX"),
        }


def dispatch(zones):
    while True:
        l_mid_img = grab_images(zones)["l_mid"]
        r_mid_img = grab_images(zones)["r_mid"]
        if check(BROWN, 0, 1, l_mid_img) == 100:
            pyautogui.press("left")
        elif check(BROWN, 0, 1, r_mid_img) == 100:
            pyautogui.press("right")


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
