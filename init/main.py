import logging

from detection import dispatch


def main():
    logging.basicConfig(level=logging.INFO)
    dispatch()


if __name__ == "__main__":
    main()
