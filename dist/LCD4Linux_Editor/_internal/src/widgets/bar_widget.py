from dataclasses import dataclass


@dataclass
class BarWidgetConfig:
    name: str = ""
    expression: str = ""
    expression2: str = ""
    length: int = 10
    min_val: int = 0
    max_val: int = 100
    direction: str = "E"
    style: str = ""
    foreground: str = "000000"
    background: str = "ffffff"
    update: int = 1000
    barcolor0: str = "ff0000"
    barcolor1: str = "00ff00"

    @property
    def min(self):
        return self.min_val

    @min.setter
    def min(self, value):
        self.min_val = value

    @property
    def max(self):
        return self.max_val

    @max.setter
    def max(self, value):
        self.max_val = value
