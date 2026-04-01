# LCD4Linux 可视化编辑器

用于 lcd4linux 配置的可视化编辑器，支持 50+ 种显示驱动。

## 功能特性

- 可视化布局编辑器，支持拖放功能
- 多种组件类型：文本、进度条、图片、计时器、图标、折线图、弧形仪表
- **支持 50+ 种显示驱动**（DPF、VNC、SamsungSPF、X11 等）
- 实时预览显示布局
- 导出 lcd4linux 配置文件
- 项目保存/加载功能（.lcd4 格式）
- **中文界面**
- 支持 TrueType 字体显示中文字符

## 安装

```bash
pip install pyinstaller
```

## 编译可执行文件

```bash
pyinstaller lcd4linux_editor.spec
```

可执行文件位置：`dist/LCD4Linux_Editor/LCD4Linux_Editor.exe`

## 支持的显示驱动

### 图形显示
- **DPF** - 数码相框（AX206 等）
- **VNC** - VNC 服务器
- **SamsungSPF** - 三星电子相框
- **X11** - X11 显示
- **T6963** - T6963 LCD 控制器
- **G15** - Logitech G15 键盘
- **Framebuffer** - Linux 帧缓冲

### 字符显示
- **HD44780** - HD44780 字符 LCD
- **Curses** - 终端界面
- **MatrixOrbital** - MatrixOrbital LCD
- **Noritake** - Noritake VFD
- 以及更多...

### USB 设备
- **LCD2USB** - LCD2USB
- **USBLCD** - USBLCD
- **picoLCD** - picoLCD

### 网络设备
- **VNC** - VNC 服务器
- **LCDTerm** - LCD 终端
- **RouterBoard** - RouterBoard

完整支持的 50+ 种驱动列表请参考源代码。

## 使用方法

1. 从下拉菜单中选择显示驱动
2. 配置显示设置（分辨率、字体、端口等）
3. 使用按钮添加组件（文本、进度条、图片、折线图、弧形仪表等）
4. 拖动组件在画布上定位
5. 导出配置到 lcd4linux.conf 文件

## 支持的组件

- **文本**：支持表达式的动态/静态文本
- **进度条**：带最小/最大值的进度条
- **图片**：PNG 图片显示
- **计时器**：倒计时/已用时间
- **图标**：基于表达式的图标显示
- **折线图**：历史数据折线图/面积图（AIDA64 风格）
  - 参数：表达式、宽度、高度、最小值、最大值、更新周期、数据点数、样式（0=线条，1=填充）、颜色、填充色、背景色、网格色
- **弧形仪表**：弧形仪表盘（AIDA64 风格）
  - 参数：表达式、宽度、高度、最小值、最大值、更新周期、样式（半圆/四分之一圆/完整圆）、主刻度数、细分刻度、表盘厚度、指针颜色、弧形颜色、中心颜色、背景色

## 显示配置

### 通用参数
- 驱动：从 50+ 种支持的驱动中选择
- 端口：设备/端口标识符
- 宽度/高度：显示分辨率
- 颜色深度：1-32 位
- 方向：横向、纵向等
- 前景色/背景色：颜色设置

### 字体设置（图形显示）
- 字体：TrueType 字体文件路径
- 字号：字体大小（8-64）

### VNC 设置
- 端口：VNC 端口（默认：5900）

### X11 设置
- 显示：X11 显示标识符（默认：:0）

## 更多信息

- LCD4Linux Wiki：https://wiki.lcd4linux.tk/
- 中文显示项目：https://github.com/netusb/lcd4linux-display-chinese

## 许可证

MIT 许可证