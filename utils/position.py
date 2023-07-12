import pyautogui
import time

from launcher import Launcher
from detection import grab_images


def get_mous_pos(zones):
    # time.sleep(3)
    # start_verif = grab_images(zones)["start_zone"]
    # start_verif.save("../res/img/zones/start/start_img.png")
    while True:
        x, y = pyautogui.position()
        print(f"Position de la souris : X={x}, Y={y}")
        time.sleep(0.25)


if __name__ == "__main__":
    launcher = Launcher()
    get_mous_pos(launcher.zones)
