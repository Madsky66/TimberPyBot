import logging
import time

from pynput import mouse
from detection import Zone, Bot, run


def main():
    logging.basicConfig(level=logging.INFO)

    logging.info(" Configuration des zones...")

    left_main_zone = Zone(int(759 * 1.25), int(480 * 1.25), 1, 20)
    right_main_zone = Zone(int(843 * 1.25), int(480 * 1.25), 1, 20)
    main_zones = left_main_zone, right_main_zone

    left_shake_zones = [Zone(int(755 * 1.25), int(460 * 1.25), 12, 1), Zone(int(755 * 1.25), int(515 * 1.25), 12, 1)]
    right_shake_zones = [Zone(int(839 * 1.25), int(460 * 1.25), 12, 1), Zone(int(839 * 1.25), int(515 * 1.25), 12, 1)]
    shake_zones = left_shake_zones, right_shake_zones

    zones = main_zones, shake_zones
    visualize_zones(main_zones)

    logging.info(" Initialisation du bot dans 1 seconde...")
    time.sleep(1)

    bot = Bot(zones, left_main_zone, right_main_zone, shake_zones)

    logging.info(" Bot initialisé")
    logging.info(" Lancement de la détection dans 1 seconde...")
    time.sleep(1)

    run(zones, left_main_zone, right_main_zone, shake_zones)


def visualize_zones(zones):
    logging.info(" Début de la visualisation des zones dans 3 secondes...")
    time.sleep(1)
    logging.info(" Début de la visualisation des zones dans 2 secondes...")
    time.sleep(1)
    logging.info(" Début de la visualisation des zones dans 1 secondes...")
    time.sleep(1)

    for zone in zones:
        mouse.position = (zone.x, zone.y)
        time.sleep(1)
        mouse.position = ((zone.x + zone.width), (zone.y + zone.height))
        time.sleep(2)


if __name__ == "__main__":
    main()
