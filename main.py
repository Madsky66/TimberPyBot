from bot import Bot, get_color_to_detect


class ZoneParams:
    def __init__(self, x, y, width, height, color, coverage):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.coverage = coverage
        self.rect = (x, y, x + width, y + height)
        self.confirmations = 0


def main():
    color_to_detect = get_color_to_detect()
    left_zones = [
        ZoneParams(int(755 * 1.25), int(460 * 1.25), 12, 1, color_to_detect, 0.1),
        ZoneParams(int(759 * 1.25), int(480 * 1.25), 1, 20, color_to_detect, 0.75),
        ZoneParams(int(755 * 1.25), int(515 * 1.25), 12, 1, color_to_detect, 0.1)
    ]
    right_zones = [
        ZoneParams(int(839 * 1.25), int(460 * 1.25), 12, 1, color_to_detect, 0.1),
        ZoneParams(int(843 * 1.25), int(480 * 1.25), 1, 20, color_to_detect, 0.75),
        ZoneParams(int(839 * 1.25), int(515 * 1.25), 12, 1, color_to_detect, 0.1)
    ]
    bot = Bot(left_zones, right_zones)
    bot.run()


if __name__ == "__main__":
    main()
