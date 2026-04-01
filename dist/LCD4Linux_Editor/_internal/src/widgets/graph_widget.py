from dataclasses import dataclass


@dataclass
class GraphWidgetConfig:
    name: str = ""
    expression: str = ""
    width: int = 100
    height: int = 40
    min_val: float = 0
    max_val: float = 100
    update: int = 1000
    points: int = 50
    style: int = 0
    color: str = "00FF00"
    fill: str = "003300"
    bg: str = "000000"
    grid: str = "404040"

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
