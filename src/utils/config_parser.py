"""
Configuration Parser for lcd4linux
Parses lcd4linux.conf files into project configuration
"""

import re
from typing import Dict, Any, Optional, List, Tuple

from ..models import (
    ProjectConfig, DisplayConfig, LayoutConfig, LayoutPosition,
    WidgetPlacement, VariablesConfig, WidgetType
)
from ..widgets import (
    TextWidgetConfig, BarWidgetConfig, ImageWidgetConfig,
    TimerWidgetConfig, IconWidgetConfig
)


class ConfigParser:
    def __init__(self):
        self.current_section = None
        self.current_subsection = None
        self.current_widget = None

    def parse(self, content: str) -> ProjectConfig:
        project = ProjectConfig()

        lines = content.split("\n")
        i = 0

        while i < len(lines):
            line = lines[i].strip()

            if not line or line.startswith("#"):
                i += 1
                continue

            if line.startswith("Display "):
                project = self._parse_display(line, lines, i + 1, project)
                while i < len(lines) and not lines[i].strip().startswith("}"):
                    i += 1
                i += 1
                continue

            if line.startswith("Widget "):
                widget_data = self._parse_widget(line, lines, i + 1)
                widget_name, widget_config = self._create_widget_config(widget_data)
                widgets_dict = getattr(project, 'widgets', {})
                if not widgets_dict:
                    widgets_dict = {}
                    object.__setattr__(project, 'widgets', widgets_dict)
                widgets_dict[widget_name] = widget_config

                while i < len(lines) and not lines[i].strip().startswith("}"):
                    i += 1
                i += 1
                continue

            if line.startswith("Layout "):
                layout_data = self._parse_layout(line, lines, i + 1, project)
                project.layouts = [layout_data]
                while i < len(lines) and not lines[i].strip().startswith("}"):
                    i += 1
                i += 1
                continue

            if line.startswith("Variables "):
                project.variables = self._parse_variables(line, lines, i + 1)
                while i < len(lines) and not lines[i].strip().startswith("}"):
                    i += 1
                i += 1
                continue

            if line.startswith("Display '") or line.startswith('Display "'):
                match = re.search(r"Display ['\"](.+?)['\"]", line)
                if match:
                    project.display.name = match.group(1)
            elif line.startswith("Layout '") or line.startswith('Layout "'):
                match = re.search(r"Layout ['\"](.+?)['\"]", line)
                if match:
                    project.active_layout = match.group(1)

            i += 1

        return project

    def _parse_display(self, header: str, lines: List[str], start: int, project: ProjectConfig) -> ProjectConfig:
        display = DisplayConfig()

        match = re.search(r"Display\s+(\w+)", header)
        if match:
            display.name = match.group(1)

        i = start
        while i < len(lines):
            line = lines[i].strip()

            if line == "}":
                break

            if not line or line.startswith("#"):
                i += 1
                continue

            if "Driver" in line:
                match = re.search(r"Driver\s+['\"](.+?)['\"]", line)
                if match:
                    display.driver = match.group(1)

            elif "Port" in line:
                match = re.search(r"Port\s+['\"](.+?)['\"]", line)
                if match:
                    display.port = match.group(1)

            elif "Font" in line:
                match = re.search(r"Font\s+['\"](.+?)['\"]", line)
                if match:
                    display.font = match.group(1)

            elif "Orientation" in line:
                match = re.search(r"Orientation\s+(\d+)", line)
                if match:
                    display.orientation = int(match.group(1))

            elif "Backlight" in line:
                match = re.search(r"Backlight\s+(\d+)", line)
                if match:
                    display.backlight = int(match.group(1))

            elif "Foreground" in line:
                match = re.search(r"Foreground\s+['\"](.+?)['\"]", line)
                if match:
                    display.foreground = match.group(1)

            elif "Background" in line:
                match = re.search(r"Background\s+['\"](.+?)['\"]", line)
                if match:
                    display.background = match.group(1)

            elif "Basecolor" in line:
                match = re.search(r"Basecolor\s+['\"](.+?)['\"]", line)
                if match:
                    display.basecolor = match.group(1)

            i += 1

        project.display = display
        return project

    def _parse_widget(self, header: str, lines: List[str], start: int) -> Dict[str, str]:
        data = {}

        match = re.search(r"Widget\s+(\w+)", header)
        if match:
            data["name"] = match.group(1)

        i = start
        while i < len(lines):
            line = lines[i].strip()

            if line == "}":
                break

            if not line or line.startswith("#"):
                i += 1
                continue

            for key in ["class", "expression", "expression2", "prefix", "postfix",
                       "width", "precision", "align", "style", "file", "format",
                       "icon", "length", "min", "max", "direction", "update",
                       "reload", "visible", "inverted", "foreground", "background",
                       "BarColor0", "BarColor1"]:
                if line.startswith(key):
                    if key in ["expression", "expression2", "prefix", "postfix",
                              "class", "file", "format", "icon", "align", "style", "direction"]:
                        match = re.search(rf"{key}\s+['\"](.+?)['\"]", line)
                        if match:
                            data[key] = match.group(1)
                    else:
                        match = re.search(rf"{key}\s+(.+?)(?:\s|#|$)", line)
                        if match:
                            value = match.group(1).strip()
                            try:
                                data[key] = int(value)
                            except ValueError:
                                try:
                                    data[key] = float(value)
                                except ValueError:
                                    data[key] = value

            i += 1

        return data

    def _create_widget_config(self, data: Dict[str, str]) -> Tuple[str, Any]:
        name = data.get("name", "")
        widget_class = data.get("class", "Text").lower()

        if widget_class == "text":
            config = TextWidgetConfig(
                name=name,
                expression=data.get("expression", ""),
                prefix=data.get("prefix", ""),
                postfix=data.get("postfix", ""),
                width=int(data.get("width", 10)),
                precision=int(data.get("precision", 0)),
                align=data.get("align", "L"),
                style=data.get("style", ""),
                foreground=data.get("foreground", "000000"),
                background=data.get("background", "ffffff"),
                update=int(data.get("update", 1000))
            )
        elif widget_class == "bar":
            config = BarWidgetConfig(
                name=name,
                expression=data.get("expression", ""),
                expression2=data.get("expression2", ""),
                length=int(data.get("length", 10)),
                min_val=int(data.get("min", 0)),
                max_val=int(data.get("max", 100)),
                direction=data.get("direction", "E"),
                style=data.get("style", ""),
                foreground=data.get("foreground", "000000"),
                background=data.get("background", "ffffff"),
                update=int(data.get("update", 1000)),
                barcolor0=data.get("BarColor0", "ff0000"),
                barcolor1=data.get("BarColor1", "00ff00")
            )
        elif widget_class == "image":
            config = ImageWidgetConfig(
                name=name,
                file=data.get("file", ""),
                update=int(data.get("update", 0)),
                reload=int(data.get("reload", 0)),
                visible=int(data.get("visible", 1)),
                inverted=int(data.get("inverted", 0))
            )
        elif widget_class == "timer":
            config = TimerWidgetConfig(
                name=name,
                expression=data.get("expression", ""),
                format=data.get("format", "%H:%M:%S"),
                update=int(data.get("update", 1000)),
                visible=int(data.get("visible", 1))
            )
        elif widget_class == "icon":
            config = IconWidgetConfig(
                name=name,
                icon=data.get("icon", ""),
                expression=data.get("expression", ""),
                update=int(data.get("update", 1000)),
                visible=int(data.get("visible", 1))
            )
        else:
            config = TextWidgetConfig(name=name)

        return name, config

    def _parse_layout(self, header: str, lines: List[str], start: int, project: ProjectConfig) -> LayoutConfig:
        layout = LayoutConfig()

        match = re.search(r"Layout\s+(\w+)", header)
        if match:
            layout.name = match.group(1)

        widgets = getattr(project, 'widgets', {})

        i = start
        while i < len(lines):
            line = lines[i].strip()

            if line == "}":
                break

            if not line or line.startswith("#"):
                i += 1
                continue

            if line.startswith("Row"):
                placements = self._parse_row(line, widgets)
                layout.placements.extend(placements)

            elif line.startswith("Layer"):
                layer_num = self._parse_layer(line)
                j = i + 1
                while j < len(lines):
                    layer_line = lines[j].strip()
                    if layer_line == "}":
                        break
                    if layer_line.startswith("Row"):
                        placements = self._parse_row(layer_line, widgets)
                        for p in placements:
                            p.layer = layer_num
                        layout.placements.extend(placements)
                    j += 1

            elif "X" in line and "Y" in line:
                match = re.search(r"X(\d+)\.Y(\d+)\s+['\"](.+?)['\"]", line)
                if match:
                    x, y, widget_name = int(match.group(1)) - 1, int(match.group(2)) - 1, match.group(3)
                    if widget_name in widgets:
                        widget = widgets[widget_name]
                        widget_type = self._get_widget_type(widget)
                        current_layer = locals().get('layer_num', 1)
                        placement = WidgetPlacement(
                            widget_name=widget_name,
                            widget_type=widget_type,
                            position=LayoutPosition(x=x * 10, y=y * 20),
                            layer=current_layer
                        )
                        layout.placements.append(placement)

            i += 1

        return layout

    def _parse_row(self, line: str, widgets: Dict[str, Any]) -> List[WidgetPlacement]:
        placements = []

        match = re.search(r"Row(\d+)\s*\{(.+?)\}", line)
        if match:
            row_num = int(match.group(1))
            content = match.group(2)

            col_matches = re.findall(r"Col(\d+)\s+['\"](.+?)['\"]", content)
            for col, widget_name in col_matches:
                if widget_name in widgets:
                    widget = widgets[widget_name]
                    widget_type = self._get_widget_type(widget)
                    placement = WidgetPlacement(
                        widget_name=widget_name,
                        widget_type=widget_type,
                        position=LayoutPosition(x=(int(col) - 1) * 10, y=(row_num - 1) * 20),
                        layer=1
                    )
                    placements.append(placement)

        return placements

    def _parse_layer(self, line: str) -> int:
        match = re.search(r"Layer\s+(\d+)", line)
        return int(match.group(1)) if match else 1

    def _parse_variables(self, header: str, lines: List[str], start: int) -> VariablesConfig:
        variables = VariablesConfig()

        i = start
        while i < len(lines):
            line = lines[i].strip()

            if line == "}":
                break

            if not line or line.startswith("#"):
                i += 1
                continue

            if line.startswith("tick"):
                match = re.search(r"tick\s+(\d+)", line)
                if match:
                    variables.tick = int(match.group(1))
            else:
                match = re.match(r"(\w+)\s+(.+)", line)
                if match:
                    name, value = match.group(1), match.group(2)
                    try:
                        variables.custom_vars[name] = int(value)
                    except ValueError:
                        try:
                            variables.custom_vars[name] = float(value)
                        except ValueError:
                            variables.custom_vars[name] = value

            i += 1

        return variables

    def _get_widget_type(self, widget) -> WidgetType:
        widget_class = widget.__class__.__name__.replace("WidgetConfig", "")
        try:
            return WidgetType[widget_class.upper()]
        except KeyError:
            return WidgetType.TEXT
