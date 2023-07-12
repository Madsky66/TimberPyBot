from detection import dispatch
from launcher import Launcher


def main():
    launcher = Launcher()
    dispatch(launcher.zones)


if __name__ == "__main__":
    main()
