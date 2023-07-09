import pyautogui
import time


def main():
    while True:
        x, y = pyautogui.position()
        print(f"Position de la souris : X={x}, Y={y}")
        time.sleep(1)


if __name__ == "__main__":
    main()