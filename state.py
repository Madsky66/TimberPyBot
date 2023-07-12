class State:
    def __init__(self):
        self.flash = 0
        self.shaking = 0
        self.inactive = 0
        self.error = 0

    def reset(self, case):
        if case != "flash":
            self.flash = 0
        if case != "shaking":
            self.shaking = 0
        if case != "inactive":
            self.inactive = 0
        if case not in ["flash", "shaking", "inactive"]:
            self.error = 0

    def reset_all(self):
        self.__init__()
