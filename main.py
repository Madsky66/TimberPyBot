import logging
import sys

from detection import run
from launcher import Launcher


def main():
    launcher = Launcher()
    try:
        run(launcher.zones, launcher.left_main_zone, launcher.right_main_zone, launcher.shake_zones)
    except Exception as e:
        logging.error(f"Impossible de démarrer la détection : {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
