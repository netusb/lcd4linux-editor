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
    name: str = "dpf"
    driver: str = "DPF"
    port: str = "usb0"
    font: str = "6x8"
    orientation: int = 0
    backlight: int = 7
    foreground: str = "ffffff"
    background: str = "000000"
    basecolor: str = "ff0000"
    width: int = 320
    height: int = 240


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
