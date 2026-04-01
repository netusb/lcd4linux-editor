# LCD4Linux Visual Editor - 中文界面

UI_TEXT = {
    # 主窗口标题
    "app_title": "LCD4Linux 可视化编辑器 - 多驱动支持版",
    
    # 菜单
    "menu_file": "文件",
    "menu_new": "新建项目",
    "menu_open": "打开...",
    "menu_save": "保存",
    "menu_save_as": "另存为...",
    "menu_export": "导出配置...",
    "menu_exit": "退出",
    
    "menu_edit": "编辑",
    "menu_undo": "撤销",
    "menu_redo": "重做",
    "menu_delete": "删除组件",
    
    "menu_view": "视图",
    "menu_zoom_in": "放大",
    "menu_zoom_out": "缩小",
    "menu_reset_zoom": "重置缩放",
    
    "menu_help": "帮助",
    "menu_docs": "文档",
    "menu_about": "关于",
    
    # 标签页
    "tab_display": "显示器",
    "tab_widgets": "组件",
    "tab_layout": "布局",
    "tab_variables": "变量",
    
    # 显示器配置
    "display_settings": "显示器设置",
    "label_name": "名称:",
    "label_driver": "驱动:",
    "label_port": "端口/设备:",
    "label_font": "字体文件:",
    "label_font_size": "字号:",
    "label_width": "宽度:",
    "label_height": "高度:",
    "label_orientation": "方向:",
    "label_backlight": "背光:",
    "label_colors": "颜色",
    "label_foreground": "前景色:",
    "label_background": "背景色:",
    "label_basecolor": "基色:",
    "label_bpp": "颜色深度:",
    "label_model": "型号:",
    "label_speed": "波特率:",
    "label_contrast": "对比度:",
    "label_brightness": "亮度:",
    "label_vnc_port": "VNC端口:",
    "label_x11_display": "X11显示:",
    "label_driver_category": "驱动分类:",
    
    # 方向选项
    "orientation_landscape": "横向",
    "orientation_portrait": "纵向",
    "orientation_rev_landscape": "反向横向",
    "orientation_rev_portrait": "反向纵向",
    
    # 组件
    "btn_add_text": "+ 文本",
    "btn_add_bar": "+ 进度条",
    "btn_add_image": "+ 图片",
    "btn_add_timer": "+ 计时器",
    "btn_add_icon": "+ 图标",
    "btn_add_graph": "+ 折线图",
    "btn_add_arc": "+ 弧形仪表",
    
    "column_name": "名称",
    "column_type": "类型",
    "column_expression": "表达式",
    "column_update": "更新(ms)",
    
    # 组件编辑
    "edit_widget": "编辑组件",
    "tab_general": "常规",
    "tab_style": "样式",
    
    "label_widget_name": "名称:",
    "label_update_ms": "更新周期:",
    "label_expression": "表达式:",
    "label_prefix": "前缀:",
    "label_postfix": "后缀:",
    "label_width_chars": "宽度:",
    "label_precision": "精度:",
    "label_align": "对齐:",
    "label_file": "文件:",
    "label_visible": "可见:",
    "label_length": "长度:",
    "label_min": "最小值:",
    "label_max": "最大值:",
    "label_direction": "方向:",
    "label_bar_color_0": "进度条颜色0:",
    "label_bar_color_1": "进度条颜色1:",
    
    # 折线图参数
    "label_graph_width": "宽度:",
    "label_graph_height": "高度:",
    "label_graph_points": "数据点数:",
    "label_graph_style": "样式:",
    "label_graph_color": "线条颜色:",
    "label_graph_fill": "填充颜色:",
    "label_graph_grid": "网格颜色:",
    "graph_style_line": "线条",
    "graph_style_fill": "填充",
    
    # 弧形仪表参数
    "label_arc_style": "样式:",
    "label_arc_ticks": "主刻度数:",
    "label_arc_minor": "细分刻度:",
    "label_arc_thickness": "表盘厚度:",
    "label_arc_arc": "弧形颜色:",
    "label_arc_needle": "指针颜色:",
    "label_arc_center": "中心颜色:",
    "arc_style_semi": "半圆",
    "arc_style_quarter": "四分之一圆",
    "arc_style_full": "完整圆",
    
    # 对齐选项
    "align_left": "左对齐",
    "align_center": "居中",
    "align_right": "右对齐",
    "align_marquee": "滚动",
    "align_auto": "自动滚动",
    "align_pingpong_l": "左右弹跳",
    "align_pingpong_c": "居中弹跳",
    "align_pingpong_r": "右左弹跳",
    
    # 方向选项
    "direction_east": "东(左→右)",
    "direction_west": "西(右→左)",
    "direction_north": "北(下→上)",
    "direction_south": "南(上→下)",
    
    # 布局
    "layout_info": "布局信息",
    "label_layout": "布局:",
    "btn_add_layout": "+ 添加布局",
    "btn_delete_layout": "删除",
    
    # 变量
    "global_variables": "全局变量",
    "label_tick_ms": "Tick (毫秒):",
    "btn_add_variable": "+ 添加变量",
    
    # 状态栏
    "status_ready": "就绪",
    "status_added": "已添加 {type} 组件: {name}",
    "status_updated": "已更新组件: {name}",
    "status_deleted": "已删除组件: {name}",
    "status_saved": "已保存: {path}",
    "status_opened": "已打开: {path}",
    "status_exported": "已导出配置: {path}",
    "status_new_project": "已创建新项目",
    
    # 对话框
    "confirm_exit": "退出",
    "confirm_exit_msg": "确定要退出吗？",
    "warn_cannot_delete": "警告",
    "warn_cannot_delete_layout": "无法删除最后一个布局",
    "error_title": "错误",
    "error_open_failed": "无法打开项目: {error}",
    "error_save_failed": "无法保存项目: {error}",
    "error_export_failed": "无法导出配置: {error}",
    "export_complete": "导出完成",
    "export_complete_msg": "配置已导出到:\n{path}",
    
    # 画布
    "btn_grid": "网格",
    "label_zoom": "%",
    
    # 帮助
    "help_title": "帮助",
    "help_content": """LCD4Linux 可视化编辑器 - 帮助

本工具用于创建 lcd4linux 配置文件，支持多种显示器驱动。

主要功能:
- 可视化布局编辑器，支持拖放
- 多种组件类型 (文本、进度条、图片、计时器、图标、折线图、弧形仪表)
- 支持多种显示器驱动 (DPF, VNC, SamsungSPF, X11, 等)
- 支持中文显示 (需要配置 TrueType 字体)
- 实时预览
- 导出 lcd4linux.conf 格式配置

快速入门:
1. 选择显示器驱动类型
2. 配置显示器参数
3. 使用按钮添加组件
4. 拖动组件调整位置
5. 导出配置文件

支持的驱动:
- DPF: 数码相框 (AX206等)
- VNC: VNC服务器
- SamsungSPF: 三星电子相框
- X11: X11显示
- T6963: T6963 LCD控制器
- G15: Logitech G15键盘
- Framebuffer: Linux帧缓冲
- 以及更多...

更多信息请访问:
https://wiki.lcd4linux.tk/
https://github.com/netusb/lcd4linux-display-chinese
""",
    
    "about_title": "关于",
    "about_content": """LCD4Linux 可视化编辑器
版本 2.0

一款支持多种显示器驱动的 lcd4linux 可视化配置工具。

支持驱动:
- DPF (AX206数码相框)
- VNC
- SamsungSPF
- T6963
- G15
- X11
- Framebuffer
- HD44780
- 等50+种驱动

支持组件:
- Text (文本)
- Bar (进度条)
- Image (图片)
- Timer (计时器)
- Icon (图标)
- Graph (折线图)
- Arc (弧形仪表)

类似 AIDA64 LCD Manager。
""",
    
    # 组件类型
    "widget_type_text": "文本",
    "widget_type_bar": "进度条",
    "widget_type_image": "图片",
    "widget_type_timer": "计时器",
    "widget_type_icon": "图标",
    "widget_type_graph": "折线图",
    "widget_type_arc": "弧形仪表",
    
    # 右键菜单
    "context_edit": "编辑",
    "context_delete": "删除",
    
    # 文件对话框
    "file_lcd4_project": "LCD4Linux 项目",
    "file_lcd4_config": "lcd4linux 配置",
    "file_all": "所有文件",
    "file_save_title": "另存为",
    "file_open_title": "打开项目",
    "file_export_title": "导出 lcd4linux.conf",
    
    # 驱动分类
    "driver_category_graphic": "图形显示",
    "driver_category_character": "字符显示",
    "driver_category_usb": "USB设备",
    "driver_category_vfd": "VFD显示",
    "driver_category_lcd": "LCD控制器",
    "driver_category_network": "网络设备",
    "driver_category_other": "其他设备",
}

# 驱动中文名称映射
DRIVER_NAMES = {
    "DPF": "数码相框 (AX206)",
    "VNC": "VNC服务器",
    "SamsungSPF": "三星电子相框",
    "T6963": "T6963 LCD控制器",
    "G15": "Logitech G15键盘",
    "X11": "X11显示",
    "Framebuffer": "Linux帧缓冲",
    "HD44780": "HD44780字符LCD",
    "Curses": "Curses终端",
    "Image": "图片输出",
    "NULL": "空输出",
    "Sample": "示例输出",
    "AW4220": "AW4220 LCD",
    "BWCT": "BWCT显示器",
    "BeckmannEgle": "BeckmannEgle",
    "Crystalfontz": "Crystalfontz LCD",
    "Cwlinux": "Cwlinux LCD",
    "D4D": "D4D显示器",
    "EA232graphic": "EA232图形显示",
    "EFN": "EFN显示器",
    "FW8888": "FW8888显示器",
    "FutabaVFD": "Futaba VFD",
    "GLCD2USB": "GLCD2USB",
    "IRLCD": "IRLCD",
    "LCD2USB": "LCD2USB",
    "LCDLinux": "LCDLinux",
    "LCDTerm": "LCD终端",
    "LEDMatrix": "LED矩阵",
    "LPH7508": "LPH7508 LCD",
    "LUIse": "LUIse",
    "LW_ABP": "LW_ABP",
    "M50530": "M50530 LCD",
    "MatrixOrbital": "MatrixOrbital",
    "MatrixOrbitalGX": "MatrixOrbitalGX",
    "MilfordInstruments": "MilfordInstruments",
    "Newhaven": "Newhaven LCD",
    "Noritake": "Noritake VFD",
    "PHAnderson": "PHAnderson",
    "PICGraphic": "PIC图形",
    "Pertelian": "Pertelian",
    "RouterBoard": "RouterBoard",
    "ShuttleVFD": "Shuttle VFD",
    "SimpleLCD": "SimpleLCD",
    "TeakLCM": "TeakLCM",
    "Trefon": "Trefon",
    "USBHUB": "USBHUB",
    "USBLCD": "USBLCD",
    "WincorNixdorf": "WincorNixdorf",
    "mdm166a": "mdm166a",
    "picoLCD": "picoLCD",
    "picoLCDGraphic": "picoLCD Graphic",
    "serdisplib": "serdisplib",
    "st2205": "ST2205 LCD",
    "ula200": "ula200",
}

# 驱动参数提示
DRIVER_HELP = {
    "DPF": "数码相框驱动，需要AX206芯片的设备",
    "VNC": "VNC服务器，需要设置端口号",
    "SamsungSPF": "三星电子相框驱动",
    "X11": "X11显示驱动，需要设置DISPLAY",
    "Framebuffer": "Linux帧缓冲设备",
    "HD44780": "HD44780字符LCD控制器",
    "T6963": "T6963图形LCD控制器",
    "G15": "Logitech G15键盘LCD",
}

def get_text(key, **kwargs):
    """获取翻译文本"""
    text = UI_TEXT.get(key, key)
    if kwargs:
        try:
            text = text.format(**kwargs)
        except:
            pass
    return text

def get_driver_name(driver):
    """获取驱动的中文名称"""
    return DRIVER_NAMES.get(driver, driver)

def set_language(lang):
    """设置语言（预留）"""
    pass
