import logging
import time
import pyautogui
import winsound

from PIL import ImageGrab, Image
from init.const import WHITE, BROWN
from state import State


def grab_images(zones):
    start_zone, top_zones, mid_zones, bot_zones = zones
    l_top_zone, r_top_zone = top_zones
    l_mid_zone, r_mid_zone = mid_zones
    l_bot_zone, r_bot_zone = bot_zones
    return {
        "start_zone": ImageGrab.grab(start_zone.rect),
        "l_top": ImageGrab.grab(l_top_zone.rect),
        "r_top": ImageGrab.grab(r_top_zone.rect),
        "l_mid": ImageGrab.grab(l_mid_zone.rect),
        "r_mid": ImageGrab.grab(r_mid_zone.rect),
        "l_bot": ImageGrab.grab(l_bot_zone.rect),
        "r_bot": ImageGrab.grab(r_bot_zone.rect),
    }


def check_start(zones):
    start_base = Image.open("../res/img/zones/start/start_img.png")
    start_actual = grab_images(zones)["start_zone"]
    if list(start_base.getdata()) == list(start_actual.getdata()):
        winsound.Beep(1500, 250)
        time.sleep(1)
        pyautogui.press("space")


def dispatch(zones):
    state = State()
    while True:
        check_start(zones)
        l_mid_img = grab_images(zones)["l_mid"]
        r_mid_img = grab_images(zones)["r_mid"]

        if check(BROWN, 0, 1, l_mid_img) != 100 and check(BROWN, 0, 1, r_mid_img) != 100:
            handle_non_brown_mid_zones(state, zones, l_mid_img, r_mid_img)
        elif check(BROWN, 0, 1, l_mid_img) < 100:
            handle_brown_zone("LEFT")
            state.reset_all()
        elif check(BROWN, 0, 1, r_mid_img) < 100:
            handle_brown_zone("RIGHT")
            state.reset_all()
        else:
            handle_unknown_status(state)


def handle_non_brown_mid_zones(state, zones, l_mid_img, r_mid_img):
    zone_images = grab_images(zones)
    main_zones = ["l_top", "r_top", "l_mid", "r_mid", "l_bot", "r_bot"]
    for zone in main_zones:
        if check(WHITE, 16, 1, zone_images[zone]) == 100:
            print(f" Vérification : {WHITE}, Tolerance : {16}, Couverture : {1}")
            handle_flash(state)
            break
    else:
        if check(BROWN, 0, 1, l_mid_img) > 10 or check(BROWN, 0, 1, r_mid_img) > 10:
            handle_shaking(state)
        elif check(BROWN, 0, 1, l_mid_img) == 0 or check(BROWN, 0, 1, r_mid_img) == 0:
            handle_inactive(state)
        else:
            handle_unknown_status(state)


def handle_flash(game_status):
    print(" Flash détecté")
    game_status.reset("flash")
    if game_status.flash == 3:
        handle_action("FLASH")
        game_status.flash = 0
    else:
        game_status.flash += 1
        print(f" Flash = {game_status.flash}")
        time.sleep(0.05)


def handle_shaking(game_status):
    print(" Tremblements détectés")
    game_status.reset("shaking")
    print(" Flash non détecté")
    if game_status.shaking == 3:
        handle_action("SHAKING")
        game_status.shaking = 0
    else:
        game_status.shaking += 1
        print(f" Tremblements = {game_status.shaking}")
        time.sleep(0.01)


def handle_inactive(game_status):
    print(" Jeu non détecté")
    game_status.reset("inactive")
    print(" Tremblements non détectés")
    if game_status.inactive == 3:
        handle_action("INACTIVE")
        game_status.inactive = 0
    else:
        game_status.inactive += 1
        print(f" Inactif = {game_status.inactive}")
        time.sleep(0.01)


def handle_unknown_status(game_status):
    game_status.reset_all()
    print(" Impossible de déterminer l'état du jeu...")
    if game_status.error == 3:
        handle_action("ERROR")
        game_status.error = 0
    else:
        game_status.error += 1
        print(f" Erreur = {game_status.error}")
        time.sleep(0.01)


def handle_brown_zone(direction):
    print(" Branche détectée")
    handle_action(direction)


def check(color_to_check, tolerance, coverage, img):
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
        time.sleep(0.01)
        pyautogui.press("right" if _case == "LEFT" else "left")
        logging.info(" Branche détectée à gauche" if _case == "LEFT" else " Branche détectée à droite")
    elif _case in ["FLASH", "SHAKING"]:
        time.sleep(0.5 if _case == "FLASH" else 0.1)
        # winsound.Beep(1500 if _case == "FLASH" else 500, 250)
        logging.info(" Flash en cours..." if _case == "FLASH" else " Tremblement en cours...")
    else:
        logging.info(" Jeu inactif..." if _case == "INACTIVE" else " - ERREUR -")
        time.sleep(3)
