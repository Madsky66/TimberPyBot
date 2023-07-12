from detection import run
from launcher import Launcher


def main():
    launcher = Launcher()
    run(launcher.zones, 1)


if __name__ == "__main__":
    main()
