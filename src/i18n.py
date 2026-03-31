# LCD4Linux Visual Editor - 中文界面

UI_TEXT = {
    # 主窗口标题
    "app_title": "LCD4Linux 可视化编辑器 - AX206 配置工具",
    
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
    "label_port": "端口:",
    "label_font": "字体:",
    "label_width": "宽度:",
    "label_height": "高度:",
    "label_orientation": "方向:",
    "label_backlight": "背光:",
    "label_colors": "颜色",
    "label_foreground": "前景色:",
    "label_background": "背景色:",
    
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

本工具用于创建 lcd4linux 配置文件，专为 AX206 DPF 显示器设计。

主要功能:
- 可视化布局编辑器，支持拖放
- 多种组件类型 (文本、进度条、图片、计时器、图标)
- 实时预览
- 导出 lcd4linux.conf 格式配置

快速入门:
1. 配置显示器设置
2. 使用按钮添加组件
3. 拖动组件调整位置
4. 导出配置文件

更多信息请访问:
https://wiki.lcd4linux.tk/
""",
    
    "about_title": "关于",
    "about_content": """LCD4Linux 可视化编辑器
版本 1.0

一款专为 AX206 DPF 显示器设计的 lcd4linux 可视化配置工具。

类似于 AIDA64 LCD Manager。
""",
    
    # 组件类型
    "widget_type_text": "文本",
    "widget_type_bar": "进度条",
    "widget_type_image": "图片",
    "widget_type_timer": "计时器",
    "widget_type_icon": "图标",
    
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
}

def get_text(key, **kwargs):
    """获取翻译文本"""
    text = UI_TEXT.get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text

def set_language(lang):
    """设置语言（预留）"""
    pass
