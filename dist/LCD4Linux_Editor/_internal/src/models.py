"""
Data models for LCD4Linux Visual Editor
Contains shared data classes used across the application
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum


class WidgetType(Enum):
    TEXT = "Text"
    BAR = "Bar"
    IMAGE = "Image"
    TIMER = "Timer"
    ICON = "Icon"
    GRAPH = "Graph"
    ARC = "Arc"


class DriverType(Enum):
    DPF = "DPF"
    VNC = "VNC"
    SamsungSPF = "SamsungSPF"
    T6963 = "T6963"
    G15 = "G15"
    X11 = "X11"
    Framebuffer = "Framebuffer"
    HD44780 = "HD44780"
    Curses = "Curses"
    Image = "Image"
    NULL = "NULL"
    Sample = "Sample"
    AW4220 = "AW4220"
    BWCT = "BWCT"
    BeckmannEgle = "BeckmannEgle"
    Crystalfontz = "Crystalfontz"
    Cwlinux = "Cwlinux"
    D4D = "D4D"
    EA232graphic = "EA232graphic"
    EFN = "EFN"
    FW8888 = "FW8888"
    FutabaVFD = "FutabaVFD"
    GLCD2USB = "GLCD2USB"
    IRLCD = "IRLCD"
    LCD2USB = "LCD2USB"
    LCDLinux = "LCDLinux"
    LCDTerm = "LCDTerm"
    LEDMatrix = "LEDMatrix"
    LPH7508 = "LPH7508"
    LUIse = "LUIse"
    LW_ABP = "LW_ABP"
    M50530 = "M50530"
    MatrixOrbital = "MatrixOrbital"
    MatrixOrbitalGX = "MatrixOrbitalGX"
    MilfordInstruments = "MilfordInstruments"
    Newhaven = "Newhaven"
    Noritake = "Noritake"
    PHAnderson = "PHAnderson"
    PICGraphic = "PICGraphic"
    Pertelian = "Pertelian"
    RouterBoard = "RouterBoard"
    ShuttleVFD = "ShuttleVFD"
    SimpleLCD = "SimpleLCD"
    TeakLCM = "TeakLCM"
    Trefon = "Trefon"
    USBHUB = "USBHUB"
    USBLCD = "USBLCD"
    WincorNixdorf = "WincorNixdorf"
    mdm166a = "mdm166a"
    picoLCD = "picoLCD"
    picoLCDGraphic = "picoLCDGraphic"
    serdisplib = "serdisplib"
    st2205 = "st2205"
    ula200 = "ula200"


DRIVER_CATEGORIES = {
    "图形显示 (Graphic Displays)": [
        "DPF", "VNC", "SamsungSPF", "T6963", "G15", "X11", "Framebuffer",
        "EA232graphic", "GLCD2USB", "LCDLinux", "picoLCDGraphic", "Image"
    ],
    "字符显示 (Character Displays)": [
        "HD44780", "Curses", "M50530", "Newhaven", "Noritake",
        "SimpleLCD", "TeakLCM", "Pertelian", "PHAnderson", "CWlinux",
        "MatrixOrbital", "MatrixOrbitalGX", "MilfordInstruments", "Trefon"
    ],
    "USB设备 (USB Devices)": [
        "LCD2USB", "USBLCD", "USBHUB", "serdisplib", "IRLCD", "mdm166a"
    ],
    "VFD显示 (VFD Displays)": [
        "FutabaVFD", "ShuttleVFD"
    ],
    "LCD控制器 (LCD Controllers)": [
        "T6963", "PICGraphic", "LUIse", "AW4220", "BeckmannEgle", "Crystalfontz"
    ],
    "网络设备 (Network Devices)": [
        "VNC", "LCDTerm", "RouterBoard"
    ],
    "其他设备 (Other Devices)": [
        "NULL", "Sample", "LEDMatrix", "ula200", "picoLCD", "st2205",
        "LPH7508", "BWCT", "EFN", "FW8888", "D4D", "WincorNixdorf", "LW_ABP"
    ]
}


class Alignment(Enum):
    L = "L"
    C = "C"
    R = "R"
    M = "M"
    A = "A"
    PL = "PL"
    PC = "PC"
    PR = "PR"


class BarDirection(Enum):
    E = "E"
    W = "W"
    N = "N"
    S = "S"


class BarStyle(Enum):
    NONE = ""
    H = "H"


@dataclass
class DisplayConfig:
    name: str = "main"
    driver: str = "DPF"
    port: str = "usb0"
    font: str = ""
    font_size: int = 16
    orientation: int = 0
    backlight: int = 7
    foreground: str = "ffffff"
    background: str = "000000"
    basecolor: str = "ff0000"
    width: int = 320
    height: int = 240
    bpp: int = 4
    model: str = ""
    speed: int = 115200
    contrast: int = 127
    brightness: int = 100
    vnc_port: int = 5900
    x11_display: str = ":0"


@dataclass
class LayoutPosition:
    x: int = 0
    y: int = 0


@dataclass
class WidgetPlacement:
    widget_name: str
    widget_type: WidgetType
    position: LayoutPosition
    layer: int = 1


@dataclass
class LayoutConfig:
    name: str = "Default"
    placements: List[WidgetPlacement] = field(default_factory=list)


@dataclass
class VariablesConfig:
    tick: int = 500
    custom_vars: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProjectConfig:
    display: DisplayConfig = field(default_factory=DisplayConfig)
    layouts: List[LayoutConfig] = field(default_factory=list)
    active_layout: str = "Default"
    variables: VariablesConfig = field(default_factory=VariablesConfig)
    file_path: Optional[str] = None

    def __post_init__(self):
        if not self.layouts:
            self.layouts.append(LayoutConfig())
