import logging
import time
import pyautogui
import winsound

from PIL import ImageGrab
from init.const import WHITE, BROWN


def run(zones, i_flash, i_shaking, i_inactive, i_error):
    while True:
        check_zones, top_zones, bot_zones = zones
        l_check_zone, r_check_zone = check_zones
        l_top_verif_zone, r_top_verif_zone = top_zones
        l_bot_verif_zone, r_bot_verif_zone = bot_zones

        l_check_zone_img = ImageGrab.grab(l_check_zone.rect)
        r_check_zone_img = ImageGrab.grab(r_check_zone.rect)

        l_top_verif_zone_img = ImageGrab.grab(l_top_verif_zone.rect)
        l_bot_verif_zone_img = ImageGrab.grab(l_bot_verif_zone.rect)

        r_top_verif_zone_img = ImageGrab.grab(r_top_verif_zone.rect)
        r_bot_verif_zone_img = ImageGrab.grab(r_bot_verif_zone.rect)

        # l_check_zone_img.show()

        if check(BROWN, 0, 1, l_check_zone_img) != 100 and check(BROWN, 0, 1, r_check_zone_img) != 100:
            time.sleep(0.01)
            if check(WHITE, 16, 1, l_bot_verif_zone_img) == 100 and check(WHITE, 16, 1, r_bot_verif_zone_img) == 100:
                print(" Flash détecté")
                i_flash, i_shaking, i_inactive, i_error = reset("flash", i_flash, i_shaking, i_inactive, i_error)
                time.sleep(0.01)
                if i_flash == 3:
                    handle_action("FLASH")
                    i_flash = 0
                else:
                    i_flash += 1
                    print(f" Flash = {i_flash}")
                    time.sleep(0.08)
            elif check(BROWN, 0, 1, l_bot_verif_zone_img) > 10 or check(BROWN, 0, 1, r_bot_verif_zone_img) > 10:
                print(" Tremblements détectés")
                i_flash, i_shaking, i_inactive, i_error = reset("shaking", i_flash, i_shaking, i_inactive, i_error)
                print(" Flash non détecté")
                time.sleep(0.01)
                if i_shaking == 3:
                    handle_action("SHAKING")
                    i_shaking = 0
                else:
                    i_shaking += 1
                    print(f" Tremblements = {i_shaking}")
                    time.sleep(0.08)
            elif check(BROWN, 0, 1, l_bot_verif_zone_img) == 0 or check(BROWN, 0, 1, r_bot_verif_zone_img) == 0:
                print(" Jeu non détecté")
                i_flash, i_shaking, i_inactive, i_error = reset("inactive", i_flash, i_shaking, i_inactive, i_error)
                print(" Tremblements non détectés")
                time.sleep(0.01)
                if i_inactive == 3:
                    handle_action("INACTIVE")
                    i_inactive = 0
                else:
                    i_inactive += 1
                    print(f" Inactif = {i_inactive}")
                    time.sleep(0.08)
            else:
                i_flash = 0
                i_shaking = 0
                i_inactive = 0
                print(" Impossible de déterminer l'état du jeu...")
                time.sleep(0.01)
                if i_error == 3:
                    handle_action("ERROR")
                    i_error = 0
                else:
                    i_error += 1
                    print(f" Erreur = {i_error}")
                    time.sleep(0.08)
        elif check(BROWN, 0, 1, l_check_zone_img) == 100:
            print(" Branche détectée")
            handle_action("LEFT")
            reset_all()
        elif check(BROWN, 0, 1, r_check_zone_img) == 100:
            print(" Branche détectée")
            handle_action("RIGHT")
            reset_all()
        else:
            i_flash = 0
            i_shaking = 0
            i_inactive = 0
            print(" Impossible de déterminer l'état du jeu...")
            time.sleep(0.01)
            if i_error == 3:
                handle_action("ERROR")
                i_error = 0
            else:
                i_error += 1
                print(f" Erreur = {i_error}")
                time.sleep(0.08)


def reset_all():
    i_flash = 0
    i_shaking = 0
    i_inactive = 0
    i_error = 0
    return i_flash, i_shaking, i_inactive, i_error


def reset(i_name, i_flash, i_shaking, i_inactive, i_error):
    i_flash = 0 if i_name in ["shaking", "inactive"] else i_flash
    i_shaking = 0 if i_name in ["flash", "inactive"] else i_shaking
    i_inactive = 0 if i_name in ["flash", "shaking"] else i_inactive
    i_error = 0 if i_name in ["flash", "shaking", "inactive"] else i_error
    return i_flash, i_shaking, i_inactive, i_error


def check(color_to_check, tolerance, coverage, img):
    print(f" Vérification : {color_to_check}, Tolerance : {tolerance}, Couverture : {coverage}")
    total_pixels = img.width * img.height
    matched_pixels = sum(
        is_color_match(img.getpixel((x, y)), color_to_check, tolerance)
        for y in range(img.height)
        for x in range(img.width)
    )
    result = ((matched_pixels / total_pixels) / coverage) * 100
    print(f" Correspondance : {matched_pixels} = {result}%")
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
        time.sleep(0.25)
        pyautogui.press("left" if _case == "LEFT" else "right")
        logging.info(" Branche détectée à droite" if _case == "LEFT" else " Branche détectée à gauche")
    elif _case in ["FLASH", "SHAKING"]:
        time.sleep(1 if _case == "FLASH" else 0.25)
        # winsound.Beep(1500 if _case == "FLASH" else 500, 250)
        logging.info(" Flash en cours..." if _case == "FLASH" else " Tremblement en cours...")
    else:
        logging.info(" Jeu inactif..." if _case == "INACTIVE" else " - ERREUR -")
        time.sleep(3)
