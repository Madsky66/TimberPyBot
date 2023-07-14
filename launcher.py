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

        self.l_top_zone = Zone(int(944), int(575), 10, 1)
        self.r_top_zone = Zone(int(1048), int(575), 10, 1)

        self.l_mid_zone = Zone(int(949), int(600), 1, 20)
        self.r_mid_zone = Zone(int(1053), int(600), 1, 20)

        self.top_zones = self.l_top_zone, self.r_top_zone
        self.mid_zones = self.l_mid_zone, self.r_mid_zone
        self.zones = self.top_zones, self.mid_zones

        logging.info(" Initialisation du bot...")
        time.sleep(0.5)
        self.bot = Bot(self.zones)

        logging.info(" Lancement de la détection...")
        time.sleep(0.5)
