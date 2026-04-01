from dataclasses import dataclass


@dataclass
class TextWidgetConfig:
    name: str = ""
    expression: str = ""
    prefix: str = ""
    postfix: str = ""
    width: int = 10
    precision: int = 0
    align: str = "L"
    style: str = ""
    foreground: str = "000000"
    background: str = "ffffff"
    speed: int = 500
    update: int = 1000
