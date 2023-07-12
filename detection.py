import logging
import time
import pyautogui
import winsound

from PIL import ImageGrab
from init.const import WHITE, BROWN


def run(zones, count):
    while True:
        check_zones, verif_zones = zones
        l_check_zone, r_check_zone = check_zones
        l_verif_zone_a, l_verif_zone_b, r_verif_zone_a, r_verif_zone_b = verif_zones
        l_check_zone_img = ImageGrab.grab(l_check_zone.rect)
        r_check_zone_img = ImageGrab.grab(r_check_zone.rect)
        l_verif_zone_a_img = ImageGrab.grab(l_verif_zone_a.rect)
        l_verif_zone_b_img = ImageGrab.grab(l_verif_zone_b.rect)
        r_verif_zone_a_img = ImageGrab.grab(r_verif_zone_a.rect)
        r_verif_zone_b_img = ImageGrab.grab(r_verif_zone_b.rect)
        l_check_zone_img.show()
        r_check_zone_img.show()
        if check(BROWN, l_check_zone, 0, 1, l_check_zone_img) != 100 and check(BROWN, r_check_zone, 0, 1, r_check_zone_img) != 100:
            time.sleep(0.001)
            if check(WHITE, l_verif_zone_a, 16, 1, l_verif_zone_a_img) == 100 and check(WHITE, l_verif_zone_b, 16, 1, l_verif_zone_b_img) == 100 and check(WHITE, r_verif_zone_a, 16, 1, r_verif_zone_a_img) == 100 and check(WHITE, r_verif_zone_b, 16, 1, r_verif_zone_b_img) == 100:
                time.sleep(0.001)
                if count == 3:
                    handle_action("FLASH")
                    count -= 3
                else:
                    count += 1
                    print(f" Flash = {count}")
            elif check(BROWN, l_verif_zone_a, 0, 1, l_verif_zone_a_img) >= 10 or check(BROWN, l_verif_zone_b, 0, 1, l_verif_zone_b_img) >= 10 and check(BROWN, r_verif_zone_a, 0, 1, r_verif_zone_a_img) >= 10 or check(BROWN, r_verif_zone_b, 0, 1, r_verif_zone_b_img) >= 10:
                time.sleep(0.001)
                if count == 3:
                    handle_action("SHAKING")
                    count -= 3
                else:
                    count += 1
                    print(f" Tremblements = {count}")
            elif check(BROWN, l_verif_zone_a, 0, 1, l_verif_zone_a_img) == 0 or check(BROWN, l_verif_zone_b, 0, 1, l_verif_zone_b_img) == 0 and check(BROWN, r_verif_zone_a, 0, 1, r_verif_zone_a_img) == 0 or check(BROWN, r_verif_zone_b, 0, 1, r_verif_zone_b_img) == 0:
                time.sleep(0.001)
                handle_action("INACTIVE")
            else:
                handle_action("ERROR")
        elif check(BROWN, l_check_zone, 0, 1, l_check_zone_img) == 100:
            time.sleep(0.001)
            handle_action("LEFT")
        elif check(BROWN, r_check_zone, 0, 1, r_check_zone_img) == 100:
            time.sleep(0.001)
            handle_action("RIGHT")
        else:
            handle_action("ERROR")


def check(color_to_check, zone, tolerance, coverage, img):
    print(f" Vérification en cours : {color_to_check}, Zone : {str(zone)}, Tolerance : {tolerance}, Couverture : {coverage}")
    total_pixels = img.width * img.height
    matched_pixels = sum(
        is_color_match(img.getpixel((x, y)), color_to_check, tolerance)
        for y in range(img.height)
        for x in range(img.width)
    )
    result = ((matched_pixels / total_pixels) / coverage) * 100
    print(f" Zone vérifiée. Correspondance : {matched_pixels} = {result}%")
    # img.show()
    time.sleep(0.001)
    return result


def is_color_match(pixel_to_check, decomposed_colors, tolerance):
    if not isinstance(pixel_to_check, tuple) or len(pixel_to_check) != len(decomposed_colors):
        return False
    return all(
        abs(pixel_to_check[i] - decomposed_colors[i]) <= tolerance
        for i in range(len(decomposed_colors))
    )


def handle_action(_case):
    if _case in ["LEFT", "RIGHT"]:
        time.sleep(0.75)
        pyautogui.press("left" if _case == "LEFT" else "right")
        logging.info(" Branche détectée à droite" if _case == "LEFT" else " Branche détectée à gauche")
    elif _case in ["FLASH", "SHAKING"]:
        time.sleep(0.5)
        winsound.Beep(1500 if _case == "FLASH" else 500, 250)
        logging.info(" Flash en cours..." if _case == "FLASH" else " Tremblement en cours...")
    else:
        logging.info(" Jeu inactif..." if _case == "INACTIVE" else " - ERREUR -")
        time.sleep(1)
