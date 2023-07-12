import logging
import time
import pyautogui
import winsound

from PIL import ImageGrab
from init.case import Case
from init.const import WHITE, BROWN


def run(zones, count):
    while True:

        check_zones, verif_zones = zones
        left_check_zone, right_check_zone = check_zones
        if check(BROWN, check_zones, 0, 1) >= 50:
            print(" Condition 1 : check(BROWN, check_zones, 0, 1) >= 50 is True")
            time.sleep(0.001)
            if check(BROWN, [left_check_zone], 0, 1) == 100:
                logging.info(" Condition 2 : check(BROWN, [left_check_zone], 0, 1) == 100 is True")
                time.sleep(0.001)
                handle_action(Case.LEFT)
            elif check(BROWN, [right_check_zone], 0, 1) == 100:
                logging.info(" Condition 2 : check(BROWN, [right_check_zone], 0, 1) == 100 is True")
                time.sleep(0.001)
                handle_action(Case.RIGHT)
        else:
            logging.info(" Condition 1 : check(BROWN, check_zones, 0, 1) >= 50 is False")
            if check(WHITE, check_zones, 16, 1) == 100:
                logging.info(" Condition 2 : check(WHITE, check_zones, 16, 1) == 100 is True")
                time.sleep(0.001)
                if count == 3:
                    count += 1
                    handle_action(Case.FLASH)
                    count -= 3
                else:
                    count += 1
                    print(f" Flash = {count}")
            elif check(BROWN, verif_zones, 0, 1) >= 10:
                logging.info(" Condition 2 : check(BROWN, verif_zones, 0, 1) >= 10 is True")
                time.sleep(0.001)
                if count == 3:
                    count += 1
                    handle_action(Case.SHAKING)
                    count -= 3
                else:
                    count += 1
                    print(f" Tremblements = {count}")
            elif check(BROWN, verif_zones, 0, 1) == 0:
                logging.info(" Condition 2 : check(BROWN, verif_zones, 0, 1) == 0 is True")
                time.sleep(0.001)
                handle_action(Case.INACTIVE)
            else:
                logging.info(" Condition 2 : check(BROWN, verif_zones, 0, 1) >= 10 is False")
                handle_action(Case.ERROR)


def check(color_to_check, zones, tolerance, coverage):
    for zone in zones:
        print(zone, zones)
        print(f" Vérification en cours : {color_to_check}, Zone(s) : {str(zones)}, Tolerance : {tolerance}, Couverture : {coverage}")
        zone_image = ImageGrab.grab(zone.rect)
        total_pixels = zone_image.width * zone_image.height
        matched_pixels = sum(
            is_color_match(zone_image.getpixel((x, y)), color_to_check, tolerance)
            for y in range(zone_image.height)
            for x in range(zone_image.width)
        )
        result = ((matched_pixels / total_pixels) / coverage) * 100
        print(f" Zone vérifiée. Correspondance : {matched_pixels} = {result}%")
        # zone_image.show()
        time.sleep(0.001)
        return result
    return False


def is_color_match(pixel_to_check, decomposed_colors, tolerance):
    if not isinstance(pixel_to_check, tuple) or len(pixel_to_check) != len(decomposed_colors):
        return False
    return all(
        abs(pixel_to_check[i] - decomposed_colors[i]) <= tolerance
        for i in range(len(decomposed_colors))
    )


def handle_action(_case):
    if _case in [Case.LEFT, Case.RIGHT]:
        time.sleep(0.75)
        pyautogui.press("right" if _case == Case.LEFT else "left")
        logging.info(" Branche détectée à droite" if _case == Case.LEFT else " Branche détectée à gauche")
    elif _case in [Case.FLASH, Case.SHAKING]:
        time.sleep(0.5)
        winsound.Beep(1500 if _case == Case.FLASH else 500, 250)
        logging.info(" Flash en cours..." if _case == Case.FLASH else " Tremblement en cours...")
    else:
        logging.info(" Jeu inactif..." if _case == Case.INACTIVE else " - ERREUR -")
        time.sleep(1)
