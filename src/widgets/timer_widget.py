from dataclasses import dataclass


@dataclass
class TimerWidgetConfig:
    name: str = ""
    expression: str = ""
    format: str = "%H:%M:%S"
    update: int = 1000
    visible: int = 1
