from bot import Bot, COLOR_TO_DETECT, H_COVERAGE, V_COVERAGE


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
    left_zones = [
        ZoneParams(int(755 * 1.25), int(460 * 1.25), 12, 1, COLOR_TO_DETECT, H_COVERAGE),
        ZoneParams(int(759 * 1.25), int(480 * 1.25), 1, 20, COLOR_TO_DETECT, V_COVERAGE),
        ZoneParams(int(755 * 1.25), int(515 * 1.25), 12, 1, COLOR_TO_DETECT, H_COVERAGE)
    ]
    right_zones = [
        ZoneParams(int(839 * 1.25), int(460 * 1.25), 12, 1, COLOR_TO_DETECT, 0.1),
        ZoneParams(int(843 * 1.25), int(480 * 1.25), 1, 20, COLOR_TO_DETECT, 0.75),
        ZoneParams(int(839 * 1.25), int(515 * 1.25), 12, 1, COLOR_TO_DETECT, 0.1)
    ]
    bot = Bot(left_zones, right_zones)
    bot.run()


if __name__ == "__main__":
    main()
