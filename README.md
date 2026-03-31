# LCD4Linux Visual Editor

Visual editor for lcd4linux configuration, designed for AX206 DPF displays.

## Features

- Visual layout editor with drag-and-drop support
- Multiple widget types: Text, Bar, Image, Timer, Icon, Graph, Arc
- Real-time preview of the display layout
- Configuration export for lcd4linux
- Project save/load functionality (.lcd4 format)
- AX206 DPF display support
- **Chinese UI**

## Installation

```bash
pip install pyinstaller
```

## Build Executable

```bash
pyinstaller lcd4linux_editor.spec
```

Executable location: `dist/LCD4Linux_Editor/LCD4Linux_Editor.exe`

## Usage

1. Configure Display settings (DPF driver, resolution)
2. Add widgets using the buttons (Text, Bar, Image, etc.)
3. Drag widgets to position them on the canvas
4. Export configuration to lcd4linux.conf

## Supported Widgets

- **Text**: Dynamic/static text with expressions
- **Bar**: Progress bars with min/max values
- **Image**: PNG image display
- **Timer**: Countdown/elapsed time
- **Icon**: Icon display based on expressions
- **Graph**: Line/area chart for historical data (AIDA64 style)
  - Parameters: expression, width, height, min, max, update, points, style (0=line, 1=fill), color, fill, bg, grid
- **Arc**: Arc gauge dashboard (AIDA64 style)
  - Parameters: expression, width, height, min, max, update, style (semi/quarter/full), ticks, minor, thickness, needle, arc, center, bg

## Display Configuration

- Driver: DPF (for AX206 displays)
- Port: usb0, usb1, etc.
- Font: 6x8, 8x10, 8x12, 10x14, 12x16
- Orientation: Landscape, Portrait, etc.
- Backlight: 0-7 levels
- Colors: Foreground/Background/Base

## More Info

- LCD4Linux Wiki: https://wiki.lcd4linux.tk/

## License

MIT License
