import logging
import time

from pynput.keyboard import Controller
from pynput.mouse import Controller as MouseController
from init.bot import Bot
from init.zone import Zone


class Launcher:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.mouse = MouseController()
        self.keyboard = Controller()
        logging.info(" Configuration des zones...")

        self.left_check_zone = Zone(int(759 * 1.25), int(480 * 1.25), 1, 20)
        self.right_check_zone = Zone(int(843 * 1.25), int(480 * 1.25), 1, 20)

        self.l_top_verif_zone = Zone(int(755 * 1.25), int(460 * 1.25), 10, 1)
        self.l_bot_verif_zone = Zone(int(755 * 1.25), int(575 * 1.25), 10, 1)

        self.r_top_verif_zone = Zone(int(840 * 1.25), int(460 * 1.25), 10, 1)
        self.r_bot_verif_zone = Zone(int(839 * 1.25), int(555 * 1.25), 10, 1)

        self.check_zones = self.left_check_zone, self.right_check_zone
        self.top_zones = self.l_top_verif_zone, self.r_top_verif_zone
        self.bot_zones = self.l_bot_verif_zone, self.r_bot_verif_zone
        self.zones = self.check_zones, self.top_zones, self.bot_zones

        logging.info(" Initialisation du bot...")
        time.sleep(0.5)
        self.bot = Bot(self.zones, self.left_check_zone, self.right_check_zone, self.top_zones)

        logging.info(" Lancement de la détection...")
        time.sleep(0.5)
