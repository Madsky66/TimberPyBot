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
        self.check_zones = self.left_check_zone, self.right_check_zone
        self.left_verif_zone_a = Zone(int(755 * 1.25), int(460 * 1.25), 10, 1)
        self.left_verif_zone_b = Zone(int(755 * 1.25), int(515 * 1.25), 10, 1)
        self.right_verif_zone_a = Zone(int(840 * 1.25), int(460 * 1.25), 10, 1)
        self.right_verif_zone_b = Zone(int(839 * 1.25), int(515 * 1.25), 10, 1)
        self.verif_zones = self.left_verif_zone_a, self.left_verif_zone_b, self.right_verif_zone_a, self.right_verif_zone_b
        self.zones = self.check_zones, self.verif_zones
        logging.info(" Initialisation du bot...")
        time.sleep(0.5)
        self.bot = Bot(self.zones, self.left_check_zone, self.right_check_zone, self.verif_zones)
        logging.info(" Lancement de la détection...")
        time.sleep(0.5)
