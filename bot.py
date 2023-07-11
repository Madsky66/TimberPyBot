from collections import defaultdict
from pynput.keyboard import Controller
from pynput.mouse import Controller as MouseController


class Bot:
    def __init__(self, zones, left_main_zone, right_main_zone, shake_zones):
        self.stop_detection_flag = False
        self.mouse = MouseController()
        self.keyboard = Controller()
        self.confirmations = defaultdict(int)
        self.zones = zones
        self.left_main_zone = left_main_zone
        self.right_main_zone = right_main_zone
        self.shake_zones = shake_zones
