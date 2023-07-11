from detection import run
from launcher import Launcher


def main():
    launcher = Launcher()
    run(launcher.zones, launcher.left_main_zone, launcher.right_main_zone)


if __name__ == "__main__":
    main()
