from dataclasses import dataclass


@dataclass
class ImageWidgetConfig:
    name: str = ""
    file: str = ""
    update: int = 0
    reload: int = 0
    visible: int = 1
    inverted: int = 0
