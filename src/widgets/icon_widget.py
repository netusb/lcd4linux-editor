from dataclasses import dataclass


@dataclass
class IconWidgetConfig:
    name: str = ""
    icon: str = ""
    expression: str = ""
    update: int = 1000
    visible: int = 1
