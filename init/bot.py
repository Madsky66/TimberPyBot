from collections import defaultdict


class Bot:
    def __init__(self, zones):
        self.stop_detection_flag = False
        self.confirmations = defaultdict(int)
        self.zones = zones
