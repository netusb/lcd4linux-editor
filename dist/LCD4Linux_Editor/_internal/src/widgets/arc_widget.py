from dataclasses import dataclass


@dataclass
class ArcWidgetConfig:
    name: str = ""
    expression: str = ""
    width: int = 80
    height: int = 50
    min_val: float = 0
    max_val: float = 100
    update: int = 1000
    style: str = "semi"
    ticks: int = 5
    minor: int = 5
    thickness: int = 8
    arc: str = "404040"
    needle: str = "FF0000"
    center: str = "808080"
    bg: str = "000000"

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
