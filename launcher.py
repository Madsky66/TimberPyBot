import logging
import time

from pynput import mouse

from bot import Bot
from zone import Zone


class Launcher:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)

        logging.info(" Configuration des zones...")

        self.left_main_zone = Zone(int(759 * 1.25), int(480 * 1.25), 1, 20)
        self.right_main_zone = Zone(int(843 * 1.25), int(480 * 1.25), 1, 20)
        self.main_zones = self.left_main_zone, self.right_main_zone

        self.left_shake_zones = [Zone(int(755 * 1.25), int(460 * 1.25), 12, 1), Zone(int(755 * 1.25), int(515 * 1.25), 12, 1)]
        self.right_shake_zones = [Zone(int(839 * 1.25), int(460 * 1.25), 12, 1), Zone(int(839 * 1.25), int(515 * 1.25), 12, 1)]
        self.shake_zones = self.left_shake_zones, self.right_shake_zones

        self.zones = self.main_zones, self.shake_zones

        self.visualize_zones()

        logging.info(" Initialisation du bot dans 1 seconde...")
        time.sleep(1)

        self.bot = Bot(self.zones, self.left_main_zone, self.right_main_zone, self.shake_zones)

        logging.info(" Bot initialisé")
        logging.info(" Lancement de la détection dans 1 seconde...")
        time.sleep(1)

    def visualize_zones(self):
        logging.info(" Début de la visualisation des zones dans 3 secondes...")
        time.sleep(1)
        logging.info(" Début de la visualisation des zones dans 2 secondes...")
        time.sleep(1)
        logging.info(" Début de la visualisation des zones dans 1 seconde...")
        time.sleep(1)

        for zone in self.main_zones:
            mouse.position = (zone.x, zone.y)
            time.sleep(1)
            mouse.position = ((zone.x + zone.width), (zone.y + zone.height))
            time.sleep(2)
