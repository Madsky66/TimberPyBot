import logging
import time
import pyautogui
import winsound

from PIL import ImageGrab
from init.case import Case

from init.const import WHITE, BROWN


def run(zones):
    while True:
        i = 0
        check_zones, verif_zones = zones
        left_check_zone, right_check_zone = check_zones

        if check(BROWN, check_zones, 0, 1) >= 50:
            if check(BROWN, [left_check_zone], 0, 1) == 100:
                handle_action(Case.LEFT)
            elif check(BROWN, [right_check_zone], 0, 1) == 100:
                handle_action(Case.RIGHT)

        else:
            if check(WHITE, check_zones, 16, 1) == 100:
                while i < 3:
                    i += 1
                    print(f"Flash = {i}")
                    handle_action(Case.FLASH, i)

            else:
                if check(BROWN, verif_zones, 0, 1) == 0:
                    handle_action(Case.INACTIVE)
                elif check(BROWN, verif_zones, 0, 1) >= 10:
                    while i < 3:
                        i += 1
                        print(f"Tremblement = {i}")
                        handle_action(Case.SHAKING, i)
                else:
                    handle_action(Case.ERROR)


def check(color_to_check, zones, tolerance, coverage):
    for zones_list in zones:
        for zone in zones_list:
            zone_image = ImageGrab.grab(zone.rect)
            total_pixels = zone_image.width * zone_image.height
            matched_pixels = sum(
                is_color_match(zone_image.getpixel((x, y)), color_to_check, tolerance)
                for y in range(zone_image.height)
                for x in range(zone_image.width)
            )
            result = ((matched_pixels / total_pixels) / coverage) * 100
            print(f"{matched_pixels}, {total_pixels}, {coverage}, = {result}")
            # zone_image.show()
            return result
    return False


def is_color_match(pixel_to_check, decomposed_colors, tolerance):
    if not isinstance(pixel_to_check, tuple) or len(pixel_to_check) != len(decomposed_colors):
        return False
    return all(
        abs(pixel_to_check[i] - decomposed_colors[i]) <= tolerance
        for i in range(len(decomposed_colors))
    )


def handle_action(case, i=0):
    _action, _confirmed_message, _beep_frequency = Case[case]
    i[case] += 1

    def handle_case(_case):
        if _case in [Case.FLASH, Case.SHAKING, Case.INACTIVE, Case.ERROR]:
            duration = 740 if _case == Case.ERROR else 250
            winsound.Beep(_beep_frequency, duration)
        if _case in [Case.LEFT, Case.RIGHT]:
            pyautogui.press(_action)

    if i == (3 if case in [Case.FLASH, Case.SHAKING] else 1):
        i[case] = 0
        if case in [Case.LEFT, Case.RIGHT]:
            time.sleep(1)
        elif case in [Case.FLASH, Case.SHAKING]:
            time.sleep(0.5)
        else:
            time.sleep(0.01)
        handle_case(case)
        logging.info(_confirmed_message)
