# LCD4Linux Visual Editor

Visual editor for lcd4linux configuration with support for 50+ display drivers.

## Features

- Visual layout editor with drag-and-drop support
- Multiple widget types: Text, Bar, Image, Timer, Icon, Graph, Arc
- **50+ Display Drivers Support** (DPF, VNC, SamsungSPF, X11, and more)
- Real-time preview of the display layout
- Configuration export for lcd4linux
- Project save/load functionality (.lcd4 format)
- **Chinese UI (涓枃鐣岄潰)**
- TrueType font support for Chinese characters

## Installation

```bash
pip install pyinstaller
```

## Build Executable

```bash
pyinstaller lcd4linux_editor.spec
```

Executable location: `dist/LCD4Linux_Editor/LCD4Linux_Editor.exe`

## Supported Display Drivers

### Graphic Displays (鍥惧舰鏄剧ず)
- **DPF** - Digital Photo Frame (AX206, etc.)
- **VNC** - VNC Server
- **SamsungSPF** - Samsung SPF displays
- **X11** - X11 Display
- **T6963** - T6963 LCD Controller
- **G15** - Logitech G15 Keyboard
- **Framebuffer** - Linux Framebuffer

### Character Displays (瀛楃鏄剧ず)
- **HD44780** - HD44780 Character LCD
- **Curses** - Curses Terminal
- **MatrixOrbital** - MatrixOrbital LCD
- **Noritake** - Noritake VFD
- And more...

### USB Devices (USB璁惧)
- **LCD2USB** - LCD2USB
- **USBLCD** - USBLCD
- **picoLCD** - picoLCD

### Network Devices (缃戠粶璁惧)
- **VNC** - VNC Server
- **LCDTerm** - LCD Terminal
- **RouterBoard** - RouterBoard

For full list of 50+ supported drivers, see the source code.

## Usage

1. Select Display Driver from the dropdown
2. Configure Display settings (resolution, font, port, etc.)
3. Add widgets using the buttons (Text, Bar, Image, Graph, Arc, etc.)
4. Drag widgets to position them on the canvas
5. Export configuration to lcd4linux.conf

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

### Common Parameters
- Driver: Select from 50+ supported drivers
- Port: Device/port identifier
- Width/Height: Display resolution
- Bpp: Color depth (1-32)
- Orientation: Landscape, Portrait, etc.
- Foreground/Background: Colors

### Font Settings (鍥惧舰鏄剧ず)
- Font: TrueType font file path
- FontSize: Font size (8-64)

### VNC Settings
- Port: VNC port (default: 5900)

### X11 Settings
- Display: X11 display identifier (default: :0)

## More Info

- LCD4Linux Wiki: https://wiki.lcd4linux.tk/
- Chinese Display Project: https://github.com/netusb/lcd4linux-display-chinese

## License

MIT License
