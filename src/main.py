#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LCD4Linux 可视化编辑器
用于配置 lcd4linux，专为 AX206 DPF 显示器设计
类似于 AIDA64 LCD Manager
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import json
import os
import sys
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field
from enum import Enum

try:
    from .models import (
        WidgetType, Alignment, BarDirection, BarStyle,
        DisplayConfig, LayoutPosition, WidgetPlacement,
        LayoutConfig, VariablesConfig, ProjectConfig
    )
    from .widgets.text_widget import TextWidgetConfig
    from .widgets.bar_widget import BarWidgetConfig
    from .widgets.image_widget import ImageWidgetConfig
    from .widgets.timer_widget import TimerWidgetConfig
    from .widgets.icon_widget import IconWidgetConfig
    from .utils.config_generator import ConfigGenerator
    from .i18n import get_text, UI_TEXT
except ImportError:
    from src.models import (
        WidgetType, Alignment, BarDirection, BarStyle,
        DisplayConfig, LayoutPosition, WidgetPlacement,
        LayoutConfig, VariablesConfig, ProjectConfig
    )
    from src.widgets.text_widget import TextWidgetConfig
    from src.widgets.bar_widget import BarWidgetConfig
    from src.widgets.image_widget import ImageWidgetConfig
    from src.widgets.timer_widget import TimerWidgetConfig
    from src.widgets.icon_widget import IconWidgetConfig
    from src.utils.config_generator import ConfigGenerator
    from src.i18n import get_text, UI_TEXT
from .widgets.icon_widget import IconWidgetConfig
from .utils.config_generator import ConfigGenerator
from .i18n import get_text, UI_TEXT


class LCD4LinuxEditor(tk.Tk):
    WINDOW_TITLE = UI_TEXT.get("app_title", "LCD4Linux Visual Editor")
    WINDOW_SIZE = "1400x900"
    FONT_FAMILY = "Microsoft YaHei UI"
    FONT_SIZE = 10

    def __init__(self):
        super().__init__()
        self.title(self.WINDOW_TITLE)
        self.geometry(self.WINDOW_SIZE)
        self.configure(bg="#2b2b2b")

        try:
            self.tk.call('tk', 'scaling', 1.5)
        except:
            pass

        self.project = ProjectConfig()
        self.current_widget = None
        self.canvas_scale = 1.0
        self.drag_data = {"widget": None, "x": 0, "y": 0}
        self.drag_start = None
        self.drag_original = None

        self._setup_styles()
        self._create_menu()
        self._create_ui()
        self._create_statusbar()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except:
            pass

        style.configure("LeftPanel.TFrame", background="#3c3c3c")
        style.configure("RightPanel.TFrame", background="#3c3c3c")
        style.configure("Toolbar.TFrame", background="#2b2b2b")
        style.configure("ToolButton.TButton", padding=5, background="#4a4a4a")
        style.configure("Nav.TButton", padding=3)
        style.configure("Treeview", background="#2b2b2b", foreground="#ffffff",
                        fieldbackground="#2b2b2b", rowheight=25)
        style.configure("Treeview.Heading", background="#3c3c3c", foreground="#ffffff")
        style.configure("Config.TLabelframe", background="#3c3c3c", foreground="#ffffff")
        style.configure("Config.TLabelframe.Label", background="#3c3c3c", foreground="#ffffff")

    def _create_menu(self):
        menubar = tk.Menu(self, bg="#2b2b2b", fg="#ffffff")
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, bg="#3c3c3c", fg="#ffffff", tearoff=0)
        menubar.add_cascade(label=UI_TEXT["menu_file"], menu=file_menu)
        file_menu.add_command(label=UI_TEXT["menu_new"], command=self.new_project, accelerator="Ctrl+N")
        file_menu.add_command(label=UI_TEXT["menu_open"], command=self.open_project, accelerator="Ctrl+O")
        file_menu.add_command(label=UI_TEXT["menu_save"], command=self.save_project, accelerator="Ctrl+S")
        file_menu.add_command(label=UI_TEXT["menu_save_as"], command=self.save_project_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label=UI_TEXT["menu_export"], command=self.export_config, accelerator="Ctrl+E")
        file_menu.add_separator()
        file_menu.add_command(label=UI_TEXT["menu_exit"], command=self.on_closing)

        edit_menu = tk.Menu(menubar, bg="#3c3c3c", fg="#ffffff", tearoff=0)
        menubar.add_cascade(label=UI_TEXT["menu_edit"], menu=edit_menu)
        edit_menu.add_command(label=UI_TEXT["menu_undo"], accelerator="Ctrl+Z")
        edit_menu.add_command(label=UI_TEXT["menu_redo"], accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label=UI_TEXT["menu_delete"], command=self.delete_selected_widget)

        view_menu = tk.Menu(menubar, bg="#3c3c3c", fg="#ffffff", tearoff=0)
        menubar.add_cascade(label=UI_TEXT["menu_view"], menu=view_menu)
        view_menu.add_command(label=UI_TEXT["menu_zoom_in"], command=lambda: self.zoom_canvas(1.2))
        view_menu.add_command(label=UI_TEXT["menu_zoom_out"], command=lambda: self.zoom_canvas(0.8))
        view_menu.add_command(label=UI_TEXT["menu_reset_zoom"], command=self.reset_zoom)

        help_menu = tk.Menu(menubar, bg="#3c3c3c", fg="#ffffff", tearoff=0)
        menubar.add_cascade(label=UI_TEXT["menu_help"], menu=help_menu)
        help_menu.add_command(label=UI_TEXT["menu_docs"], command=self.show_help)
        help_menu.add_command(label=UI_TEXT["menu_about"], command=self.show_about)

        self.bind("<Control-n>", lambda e: self.new_project())
        self.bind("<Control-o>", lambda e: self.open_project())
        self.bind("<Control-s>", lambda e: self.save_project())
        self.bind("<Control-e>", lambda e: self.export_config())

    def _create_ui(self):
        main_paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        left_panel = ttk.Frame(main_paned, style="LeftPanel.TFrame")
        main_paned.add(left_panel, weight=1)

        right_panel = ttk.Frame(main_paned, style="RightPanel.TFrame")
        main_paned.add(right_panel, weight=3)

        self._create_left_panel(left_panel)
        self._create_right_panel(right_panel)

    def _create_left_panel(self, parent):
        toolbar = ttk.Frame(parent, style="Toolbar.TFrame")
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        ttk.Button(toolbar, text=UI_TEXT["menu_new"].replace("新建项目", "新建"), style="ToolButton.TButton", command=self.new_project).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text=UI_TEXT["menu_open"].replace("打开...", "打开"), style="ToolButton.TButton", command=self.open_project).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text=UI_TEXT["menu_save"].replace("保存", "保存"), style="ToolButton.TButton", command=self.save_project).pack(side=tk.LEFT, padx=2)

        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        notebook.add(ttk.Frame(notebook), text=UI_TEXT["tab_display"])
        notebook.add(ttk.Frame(notebook), text=UI_TEXT["tab_widgets"])
        notebook.add(ttk.Frame(notebook), text=UI_TEXT["tab_layout"])
        notebook.add(ttk.Frame(notebook), text=UI_TEXT["tab_variables"])

        self._create_display_config(notebook.children['!frame'])
        self._create_widgets_panel(notebook.children['!frame2'])
        self._create_layout_panel(notebook.children['!frame3'])
        self._create_variables_panel(notebook.children['!frame4'])

    def _create_display_config(self, parent):
        frame = ttk.LabelFrame(parent, text=UI_TEXT["display_settings"], style="Config.TLabelframe", padding=10)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        row = 0
        self._add_label_entry(frame, UI_TEXT["label_name"], row, self.project.display.name)
        row += 1

        ttk.Label(frame, text=UI_TEXT["label_driver"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.display_driver = ttk.Combobox(frame, values=["DPF", "HD44780", "Framebuffer"], width=18)
        self.display_driver.set(self.project.display.driver)
        self.display_driver.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1

        ttk.Label(frame, text=UI_TEXT["label_port"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.display_port = ttk.Entry(frame, width=20)
        self.display_port.insert(0, self.project.display.port)
        self.display_port.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1

        ttk.Label(frame, text=UI_TEXT["label_font"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.display_font = ttk.Combobox(frame, values=["6x8", "8x10", "8x12", "10x14", "12x16"], width=18)
        self.display_font.set(self.project.display.font)
        self.display_font.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1

        ttk.Label(frame, text=UI_TEXT["label_width"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.display_width = ttk.Spinbox(frame, from_=64, to=800, width=18)
        self.display_width.set(self.project.display.width)
        self.display_width.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1

        ttk.Label(frame, text=UI_TEXT["label_height"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.display_height = ttk.Spinbox(frame, from_=32, to=600, width=18)
        self.display_height.set(self.project.display.height)
        self.display_height.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1

        ttk.Label(frame, text=UI_TEXT["label_orientation"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.display_orientation = ttk.Combobox(frame, values=[
            UI_TEXT["orientation_landscape"],
            UI_TEXT["orientation_portrait"],
            UI_TEXT["orientation_rev_landscape"],
            UI_TEXT["orientation_rev_portrait"]
        ], width=18)
        self.display_orientation.current(self.project.display.orientation)
        self.display_orientation.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1

        ttk.Label(frame, text=UI_TEXT["label_backlight"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.display_backlight = ttk.Scale(frame, from_=0, to=7, orient=tk.HORIZONTAL, length=120)
        self.display_backlight.set(self.project.display.backlight)
        self.display_backlight.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1

        color_frame = ttk.LabelFrame(frame, text=UI_TEXT["label_colors"], padding=5)
        color_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=10)

        ttk.Label(color_frame, text=UI_TEXT["label_foreground"]).grid(row=0, column=0, sticky=tk.W)
        self.fg_color_btn = tk.Button(color_frame, bg=f"#{self.project.display.foreground}",
                                       width=3, command=self.choose_fg_color)
        self.fg_color_btn.grid(row=0, column=1, padx=5)

        ttk.Label(color_frame, text=UI_TEXT["label_background"]).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.bg_color_btn = tk.Button(color_frame, bg=f"#{self.project.display.background}",
                                       width=3, command=self.choose_bg_color)
        self.bg_color_btn.grid(row=1, column=1, padx=5, pady=5)

        for entry in [self.display_port]:
            entry.bind("<FocusOut>", lambda e: self.update_display_config())

        for spinbox in [self.display_width, self.display_height]:
            spinbox.bind("<FocusOut>", lambda e: self.update_display_config())

        self.display_driver.bind("<<ComboboxSelected>>", lambda e: self.update_display_config())
        self.display_font.bind("<<ComboboxSelected>>", lambda e: self.update_display_config())
        self.display_orientation.bind("<<ComboboxSelected>>", lambda e: self.update_display_config())
        self.display_backlight.bind("<ButtonRelease-1>", lambda e: self.update_display_config())

    def _add_label_entry(self, parent, label_text, row, default_value=""):
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky=tk.W, pady=5)
        entry = ttk.Entry(parent, width=20)
        entry.insert(0, default_value)
        entry.grid(row=row, column=1, sticky=tk.W, pady=5)
        entry.bind("<FocusOut>", lambda e: self.update_display_config())
        return entry

    def _create_widgets_panel(self, parent):
        toolbar = ttk.Frame(parent)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        ttk.Button(toolbar, text=UI_TEXT["btn_add_text"], command=lambda: self.add_widget(WidgetType.TEXT)).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text=UI_TEXT["btn_add_bar"], command=lambda: self.add_widget(WidgetType.BAR)).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text=UI_TEXT["btn_add_image"], command=lambda: self.add_widget(WidgetType.IMAGE)).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text=UI_TEXT["btn_add_timer"], command=lambda: self.add_widget(WidgetType.TIMER)).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text=UI_TEXT["btn_add_icon"], command=lambda: self.add_widget(WidgetType.ICON)).pack(side=tk.LEFT, padx=2)

        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        columns = ("Type", "Expression", "Update")
        self.widgets_tree = ttk.Treeview(tree_frame, columns=columns, show="tree headings", height=15)
        self.widgets_tree.heading("#0", text=UI_TEXT["column_name"])
        self.widgets_tree.heading("Type", text=UI_TEXT["column_type"])
        self.widgets_tree.heading("Expression", text=UI_TEXT["column_expression"])
        self.widgets_tree.heading("Update", text=UI_TEXT["column_update"])

        self.widgets_tree.column("#0", width=120)
        self.widgets_tree.column("Type", width=80)
        self.widgets_tree.column("Expression", width=150)
        self.widgets_tree.column("Update", width=80)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.widgets_tree.yview)
        self.widgets_tree.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.widgets_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.widgets_tree.bind("<Double-1>", self.edit_widget)
        self.widgets_tree.bind("<Button-3>", self.show_widget_menu)

        self.widgets = {}

    def _create_layout_panel(self, parent):
        toolbar = ttk.Frame(parent)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        ttk.Label(toolbar, text=UI_TEXT["label_layout"]).pack(side=tk.LEFT, padx=5)
        self.layout_combo = ttk.Combobox(toolbar, values=["Default"], width=15, state="readonly")
        self.layout_combo.pack(side=tk.LEFT, padx=5)
        self.layout_combo.bind("<<ComboboxSelected>>", self.select_layout)

        ttk.Button(toolbar, text=UI_TEXT["btn_add_layout"], command=self.add_layout).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text=UI_TEXT["btn_delete_layout"], command=self.delete_layout).pack(side=tk.LEFT, padx=5)

        info_frame = ttk.LabelFrame(parent, text=UI_TEXT["layout_info"], padding=10)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.layout_info = tk.Text(info_frame, height=8, bg="#2b2b2b", fg="#ffffff",
                                    relief=tk.FLAT, wrap=tk.WORD)
        self.layout_info.pack(fill=tk.BOTH, expand=True)
        self.update_layout_info()

    def _create_variables_panel(self, parent):
        frame = ttk.LabelFrame(parent, text=UI_TEXT["global_variables"], padding=10)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(frame, text=UI_TEXT["label_tick_ms"]).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.tick_var = ttk.Spinbox(frame, from_=100, to=10000, width=15)
        self.tick_var.set(self.project.variables.tick)
        self.tick_var.grid(row=0, column=1, sticky=tk.W, pady=5)
        self.tick_var.bind("<FocusOut>", lambda e: self.update_variables())

        ttk.Button(frame, text=UI_TEXT["btn_add_variable"], command=self.add_variable).grid(row=1, column=0, columnspan=2, pady=10)

        self.vars_tree = ttk.Treeview(frame, columns=("Value"), show="tree", height=10)
        self.vars_tree.heading("#0", text=UI_TEXT["column_name"])
        self.vars_tree.heading("Value", text="Value")
        self.vars_tree.column("#0", width=150)
        self.vars_tree.column("Value", width=150)
        self.vars_tree.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)

    def _create_statusbar(self):
        self.statusbar = tk.Label(self, text=UI_TEXT["status_ready"], bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    def _draw_canvas(self):
        self.canvas.delete("all")

        width = int(self.display_width.get()) if self.display_width.get() else self.project.display.width
        height = int(self.display_height.get()) if self.display_height.get() else self.project.display.height

        scaled_width = int(width * self.canvas_scale)
        scaled_height = int(height * self.canvas_scale)

        self.canvas.create_rectangle(10, 10, 10 + scaled_width, 10 + scaled_height,
                                      fill=f"#{self.project.display.background}",
                                      outline="#555555", width=2, tags="display")

        if self.show_grid.get():
            grid_size = int(20 * self.canvas_scale)
            for x in range(0, scaled_width + 1, grid_size):
                self.canvas.create_line(10 + x, 10, 10 + x, 10 + scaled_height,
                                         fill="#333333", tags="grid")
            for y in range(0, scaled_height + 1, grid_size):
                self.canvas.create_line(10, 10 + y, 10 + scaled_width, 10 + y,
                                         fill="#333333", tags="grid")

        self.canvas.create_text(10 + scaled_width // 2, 10 + scaled_height + 20,
                                 text=f"{width}x{height}", fill="#888888", tags="size_label")

        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        self._draw_widgets_on_canvas()

    def _draw_widgets_on_canvas(self):
        for placement in self.project.layouts[0].placements:
            widget = self.widgets.get(placement.widget_name)
            if widget:
                self._draw_widget(placement, widget)

    def _draw_widget(self, placement: WidgetPlacement, widget):
        x = int(10 + placement.position.x * self.canvas_scale)
        y = int(10 + placement.position.y * self.canvas_scale)

        colors = {
            WidgetType.TEXT: "#4a9eff",
            WidgetType.BAR: "#ff6b4a",
            WidgetType.IMAGE: "#4aff6b",
            WidgetType.TIMER: "#ffaa4a",
            WidgetType.ICON: "#aa4aff"
        }

        wtype_names = {
            WidgetType.TEXT: UI_TEXT["widget_type_text"],
            WidgetType.BAR: UI_TEXT["widget_type_bar"],
            WidgetType.IMAGE: UI_TEXT["widget_type_image"],
            WidgetType.TIMER: UI_TEXT["widget_type_timer"],
            WidgetType.ICON: UI_TEXT["widget_type_icon"]
        }

        width = 80 * self.canvas_scale
        height = 30 * self.canvas_scale

        if placement.widget_type == WidgetType.IMAGE:
            width = 60 * self.canvas_scale
            height = 60 * self.canvas_scale
        elif placement.widget_type == WidgetType.BAR:
            width = 100 * self.canvas_scale
            height = 20 * self.canvas_scale

        rect = self.canvas.create_rectangle(x, y, x + width, y + height,
                                             fill=colors.get(placement.widget_type, "#888888"),
                                             outline="#ffffff", width=2, tags=f"widget_{placement.widget_name}")
        self.canvas.tag_bind(rect, "<Button-1>",
                             lambda e, w=placement.widget_name: self.select_widget_on_canvas(w))
        self.canvas.tag_bind(rect, "<B1-Motion>",
                             lambda e, w=placement.widget_name: self.drag_widget(w, e))
        self.canvas.tag_bind(rect, "<Button-3>",
                             lambda e, w=placement.widget_name: self.show_widget_context_menu(e, w))

        type_text = wtype_names.get(placement.widget_type, "WIDGET")
        self.canvas.create_text(x + width/2, y + height/2,
                               text=type_text, fill="#ffffff", tags=f"text_{placement.widget_name}")

        self.canvas.tag_bind(self.canvas.create_text(x + width/2, y + height/2,
                              text=type_text, fill="#ffffff", tags=f"text_{placement.widget_name}"),
                              "<Button-1>",
                              lambda e, w=placement.widget_name: self.select_widget_on_canvas(w))
        self.canvas.tag_bind(self.canvas.create_text(x + width/2, y + height/2,
                              text=type_text, fill="#ffffff", tags=f"text_{placement.widget_name}"),
                              "<B1-Motion>",
                              lambda e, w=placement.widget_name: self.drag_widget(w, e))
        self.canvas.tag_bind(self.canvas.create_text(x + width/2, y + height/2,
                              text=type_text, fill="#ffffff", tags=f"text_{placement.widget_name}"),
                              "<Button-3>",
                              lambda e, w=placement.widget_name: self.show_widget_context_menu(e, w))

        self.canvas.create_text(x + 3, y + 3, text=placement.widget_name,
                                 fill="#ffffff", anchor=tk.NW, font=("Arial", 8), tags=f"label_{placement.widget_name}")

    def _create_right_panel(self, parent):
        self.show_grid = tk.BooleanVar(value=True)
        
        toolbar = ttk.Frame(parent, style="Toolbar.TFrame")
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.zoom_label = ttk.Label(toolbar, text="100%")
        self.zoom_label.pack(side=tk.RIGHT, padx=10)
        ttk.Button(toolbar, text="-", width=3, command=lambda: self.zoom_canvas(0.8)).pack(side=tk.RIGHT, padx=2)
        ttk.Button(toolbar, text="+", width=3, command=lambda: self.zoom_canvas(1.2)).pack(side=tk.RIGHT, padx=2)
        self.grid_check = ttk.Checkbutton(toolbar, text=UI_TEXT["btn_grid"], variable=self.show_grid)
        self.grid_check.pack(side=tk.RIGHT, padx=10)

        canvas_frame = ttk.Frame(parent)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.canvas_scroll_x = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
        self.canvas_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas_scroll_y = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL)
        self.canvas_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(
            canvas_frame,
            bg="#1a1a1a",
            xscrollcommand=self.canvas_scroll_x.set,
            yscrollcommand=self.canvas_scroll_y.set,
            highlightthickness=0
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas_scroll_x.config(command=self.canvas.xview)
        self.canvas_scroll_y.config(command=self.canvas.yview)

        self.show_grid = tk.BooleanVar(value=True)

        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<B1-Motion>", self.canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.canvas_release)
        self.canvas.bind("<MouseWheel>", self.canvas_zoom)

        self._draw_canvas()

    def select_widget_on_canvas(self, widget_name):
        self.canvas.delete("selection")
        placement = next((p for p in self.project.layouts[0].placements if p.widget_name == widget_name), None)
        if placement:
            x = int(10 + placement.position.x * self.canvas_scale)
            y = int(10 + placement.position.y * self.canvas_scale)
            width = 80 * self.canvas_scale
            height = 30 * self.canvas_scale

            self.canvas.create_rectangle(x - 2, y - 2, x + width + 2, y + height + 2,
                                          outline="#00ff00", width=2, tags="selection")

        self.widgets_tree.selection_set(widget_name)
        self.widgets_tree.see(widget_name)

    def drag_widget(self, widget_name, event):
        if self.drag_start is None:
            self.drag_start = (event.x, event.y)
            placement = next((p for p in self.project.layouts[0].placements if p.widget_name == widget_name), None)
            if placement:
                self.drag_original = (placement.position.x, placement.position.y)
            return

        dx = (event.x - self.drag_start[0]) / self.canvas_scale
        dy = (event.y - self.drag_start[1]) / self.canvas_scale

        if self.drag_original:
            new_x = max(0, int(self.drag_original[0] + dx))
            new_y = max(0, int(self.drag_original[1] + dy))

            placement = next((p for p in self.project.layouts[0].placements if p.widget_name == widget_name), None)
            if placement:
                placement.position.x = new_x
                placement.position.y = new_y
                self._draw_canvas()

    def canvas_release(self, event):
        self.drag_start = None
        self.drag_original = None

    def canvas_click(self, event):
        pass

    def canvas_drag(self, event):
        pass

    def canvas_zoom(self, event):
        if event.delta > 0:
            self.zoom_canvas(1.1)
        else:
            self.zoom_canvas(0.9)

    def zoom_canvas(self, factor):
        self.canvas_scale *= factor
        self.canvas_scale = max(0.25, min(4.0, self.canvas_scale))
        self.zoom_label.config(text=f"{int(self.canvas_scale * 100)}%")
        self._draw_canvas()

    def reset_zoom(self):
        self.canvas_scale = 1.0
        self.zoom_label.config(text="100%")
        self._draw_canvas()

    def add_widget(self, widget_type: WidgetType):
        name = f"{widget_type.value.lower()}_{len(self.widgets) + 1}"

        if widget_type == WidgetType.TEXT:
            config = TextWidgetConfig()
        elif widget_type == WidgetType.BAR:
            config = BarWidgetConfig()
        elif widget_type == WidgetType.IMAGE:
            config = ImageWidgetConfig()
        elif widget_type == WidgetType.TIMER:
            config = TimerWidgetConfig()
        elif widget_type == WidgetType.ICON:
            config = IconWidgetConfig()
        else:
            return

        config.name = name
        self.widgets[name] = config

        placement = WidgetPlacement(
            widget_name=name,
            widget_type=widget_type,
            position=LayoutPosition(x=10, y=10)
        )
        self.project.layouts[0].placements.append(placement)

        self.widgets_tree.insert("", "end", iid=name, values=(widget_type.value, "", "1000"))
        self._draw_canvas()
        self.update_layout_info()
        self.statusbar.config(text=get_text("status_added", type=widget_type.value, name=name))

    def edit_widget(self, event):
        selection = self.widgets_tree.selection()
        if not selection:
            return

        widget_name = selection[0]
        widget = self.widgets.get(widget_name)
        if not widget:
            return

        self.current_widget = widget
        self._open_widget_editor(widget)

    def _open_widget_editor(self, widget):
        editor = WidgetEditorWindow(self, widget, self._on_widget_updated)
        editor.grab_set()

    def _on_widget_updated(self, widget_name: str, widget_config):
        self.widgets[widget_name] = widget_config
        self._draw_canvas()

        widget_type = widget_config.__class__.__name__.replace("WidgetConfig", "")
        try:
            wtype = WidgetType[widget_type.upper()]
        except:
            wtype = WidgetType.TEXT

        for item in self.widgets_tree.get_children():
            if self.widgets_tree.item(item, "iid") == widget_name:
                self.widgets_tree.item(item, values=(
                    wtype.value,
                    getattr(widget_config, "expression", getattr(widget_config, "file", ""))[:30],
                    getattr(widget_config, "update", 1000)
                ))
                break

        self.update_layout_info()
        self.statusbar.config(text=get_text("status_updated", name=widget_name))

    def delete_selected_widget(self):
        selection = self.widgets_tree.selection()
        if not selection:
            return

        widget_name = selection[0]
        if widget_name in self.widgets:
            del self.widgets[widget_name]

        self.project.layouts[0].placements = [
            p for p in self.project.layouts[0].placements if p.widget_name != widget_name
        ]

        self.widgets_tree.delete(widget_name)
        self._draw_canvas()
        self.update_layout_info()
        self.statusbar.config(text=get_text("status_deleted", name=widget_name))

    def show_widget_menu(self, event):
        menu = tk.Menu(self, bg="#3c3c3c", fg="#ffffff", tearoff=0)
        menu.add_command(label=UI_TEXT["context_edit"], command=lambda: self.edit_widget(None))
        menu.add_command(label=UI_TEXT["context_delete"], command=lambda: self.delete_selected_widget())
        menu.tk_popup(event.x_root, event.y_root)

    def show_widget_context_menu(self, event, widget_name):
        menu = tk.Menu(self, bg="#3c3c3c", fg="#ffffff", tearoff=0)
        menu.add_command(label=UI_TEXT["context_edit"], command=lambda: self._edit_widget_by_name(widget_name))
        menu.add_command(label=UI_TEXT["context_delete"], command=lambda: self._delete_widget_by_name(widget_name))
        menu.tk_popup(event.x_root, event.y_root)

    def _edit_widget_by_name(self, widget_name):
        self.widgets_tree.selection_set(widget_name)
        self.edit_widget(None)

    def _delete_widget_by_name(self, widget_name):
        self.widgets_tree.selection_set(widget_name)
        self.delete_selected_widget()

    def choose_fg_color(self):
        color = colorchooser.askcolor(color=self.project.display.foreground, parent=self)
        if color[1]:
            self.project.display.foreground = color[1].lstrip("#")
            self.fg_color_btn.config(bg=f"#{self.project.display.foreground}")
            self._draw_canvas()

    def choose_bg_color(self):
        color = colorchooser.askcolor(color=self.project.display.background, parent=self)
        if color[1]:
            self.project.display.background = color[1].lstrip("#")
            self.bg_color_btn.config(bg=f"#{self.project.display.background}")
            self._draw_canvas()

    def update_display_config(self):
        self.project.display.name = getattr(self, 'display_port', tk.Entry()).get() if hasattr(self, 'display_port') else "dpf"
        self.project.display.driver = self.display_driver.get()
        self.project.display.port = self.display_port.get()
        self.project.display.font = self.display_font.get()
        self.project.display.width = int(self.display_width.get())
        self.project.display.height = int(self.display_height.get())
        self.project.display.orientation = self.display_orientation.current()
        self.project.display.backlight = int(self.display_backlight.get())
        self._draw_canvas()

    def update_variables(self):
        self.project.variables.tick = int(self.tick_var.get())

    def add_layout(self):
        name = f"Layout_{len(self.project.layouts) + 1}"
        new_layout = LayoutConfig(name=name)
        self.project.layouts.append(new_layout)
        self.layout_combo["values"] = [l.name for l in self.project.layouts]
        self.layout_combo.set(name)
        self.update_layout_info()
        self.statusbar.config(text=f"已添加布局: {name}")

    def delete_layout(self):
        if len(self.project.layouts) <= 1:
            messagebox.showwarning(UI_TEXT["warn_cannot_delete"], UI_TEXT["warn_cannot_delete_layout"])
            return

        current = self.layout_combo.get()
        self.project.layouts = [l for l in self.project.layouts if l.name != current]
        self.layout_combo["values"] = [l.name for l in self.project.layouts]
        self.layout_combo.set(self.project.layouts[0].name)
        self.update_layout_info()

    def select_layout(self, event):
        current = self.layout_combo.get()
        self.project.active_layout = current
        self._draw_canvas()

    def add_variable(self):
        dialog = tk.Toplevel(self)
        dialog.title(UI_TEXT["btn_add_variable"])
        dialog.geometry("300x100")
        dialog.transient(self)

        ttk.Label(dialog, text=UI_TEXT["column_name"]).grid(row=0, column=0, padx=10, pady=10)
        name_entry = ttk.Entry(dialog, width=20)
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(dialog, text="Value:").grid(row=1, column=0, padx=10, pady=10)
        value_entry = ttk.Entry(dialog, width=20)
        value_entry.grid(row=1, column=1, padx=10, pady=10)

        def save():
            name = name_entry.get()
            value = value_entry.get()
            if name:
                self.project.variables.custom_vars[name] = value
                self.vars_tree.insert("", "end", iid=name, values=(value,))
            dialog.destroy()

        ttk.Button(dialog, text="添加", command=save).grid(row=2, column=0, columnspan=2, pady=10)

    def update_layout_info(self):
        layout = self.project.layouts[0] if self.project.layouts else None
        if not layout:
            return

        info = f"布局: {layout.name}\n"
        info += f"组件数: {len(layout.placements)}\n\n"
        info += "组件位置:\n"

        for p in layout.placements:
            widget = self.widgets.get(p.widget_name)
            if widget:
                widget_type = widget.__class__.__name__.replace("WidgetConfig", "")
                info += f"  - {p.widget_name} ({widget_type})\n"
                info += f"    位置: ({p.position.x}, {p.position.y})\n"
                info += f"    图层: {p.layer}\n"

        self.layout_info.config(state=tk.NORMAL)
        self.layout_info.delete(1.0, tk.END)
        self.layout_info.insert(1.0, info)
        self.layout_info.config(state=tk.DISABLED)

    def new_project(self):
        self.project = ProjectConfig()
        self.widgets = {}
        self.widgets_tree.delete(*self.widgets_tree.get_children())
        self._draw_canvas()
        self.statusbar.config(text=UI_TEXT["status_new_project"])

    def open_project(self):
        filename = filedialog.askopenfilename(
            title=UI_TEXT["file_open_title"],
            filetypes=[(UI_TEXT["file_lcd4_project"], "*.lcd4"), (UI_TEXT["file_all"], "*.*")]
        )
        if not filename:
            return

        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.project = self._deserialize_project(data)
            self.widgets = {}

            for layout in self.project.layouts:
                for placement in layout.placements:
                    widget = self._create_widget_from_config(placement)
                    if widget:
                        self.widgets[placement.widget_name] = widget

            self.display_driver.set(self.project.display.driver)
            self.display_port.delete(0, tk.END)
            self.display_port.insert(0, self.project.display.port)
            self.display_font.set(self.project.display.font)
            self.display_width.set(self.project.display.width)
            self.display_height.set(self.project.display.height)
            self.display_orientation.current(self.project.display.orientation)
            self.display_backlight.set(self.project.display.backlight)
            self.fg_color_btn.config(bg=f"#{self.project.display.foreground}")
            self.bg_color_btn.config(bg=f"#{self.project.display.background}")

            self.widgets_tree.delete(*self.widgets_tree.get_children())
            for name, widget in self.widgets.items():
                wtype = widget.__class__.__name__.replace("WidgetConfig", "")
                try:
                    wt = WidgetType[wtype.upper()]
                except:
                    wt = WidgetType.TEXT
                self.widgets_tree.insert("", "end", iid=name, values=(
                    wt.value,
                    getattr(widget, "expression", getattr(widget, "file", ""))[:30],
                    getattr(widget, "update", 1000)
                ))

            self.layout_combo["values"] = [l.name for l in self.project.layouts]
            self.layout_combo.set(self.project.active_layout)

            self._draw_canvas()
            self.statusbar.config(text=get_text("status_opened", path=filename))

        except Exception as e:
            messagebox.showerror(UI_TEXT["error_title"], get_text("error_open_failed", error=str(e)))

    def _deserialize_project(self, data):
        display = DisplayConfig(**data.get("display", {}))
        layouts = [LayoutConfig(**l) for l in data.get("layouts", [])]
        for layout in layouts:
            for p in layout.placements:
                wt_str = str(p.widget_type).replace("WidgetType.", "")
                p.widget_type = WidgetType[wt_str]
                p.position = LayoutPosition(**p.position)
        variables_data = data.get("variables", {})
        variables = VariablesConfig(
            tick=variables_data.get("tick", 500),
            custom_vars=variables_data.get("custom_vars", {})
        )

        project = ProjectConfig(
            display=display,
            layouts=layouts,
            active_layout=data.get("active_layout", "Default"),
            variables=variables,
            file_path=data.get("file_path")
        )
        return project

    def _create_widget_from_config(self, placement: WidgetPlacement):
        widget_name = placement.widget_name
        widget_type = placement.widget_type

        if widget_type == WidgetType.TEXT:
            return TextWidgetConfig(name=widget_name)
        elif widget_type == WidgetType.BAR:
            return BarWidgetConfig(name=widget_name)
        elif widget_type == WidgetType.IMAGE:
            return ImageWidgetConfig(name=widget_name)
        elif widget_type == WidgetType.TIMER:
            return TimerWidgetConfig(name=widget_name)
        elif widget_type == WidgetType.ICON:
            return IconWidgetConfig(name=widget_name)
        return None

    def save_project(self):
        if not self.project.file_path:
            self.save_project_as()
            return

        try:
            data = self._serialize_project()
            with open(self.project.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.statusbar.config(text=get_text("status_saved", path=self.project.file_path))
        except Exception as e:
            messagebox.showerror(UI_TEXT["error_title"], get_text("error_save_failed", error=str(e)))

    def save_project_as(self):
        filename = filedialog.asksaveasfilename(
            title=UI_TEXT["file_save_title"],
            defaultextension=".lcd4",
            filetypes=[(UI_TEXT["file_lcd4_project"], "*.lcd4"), (UI_TEXT["file_all"], "*.*")]
        )
        if not filename:
            return

        self.project.file_path = filename
        self.save_project()

    def _serialize_project(self):
        data = {
            "display": asdict(self.project.display),
            "layouts": [],
            "active_layout": self.project.active_layout,
            "variables": {
                "tick": self.project.variables.tick,
                "custom_vars": self.project.variables.custom_vars
            },
            "file_path": self.project.file_path
        }

        for layout in self.project.layouts:
            layout_data = {
                "name": layout.name,
                "placements": []
            }
            for p in layout.placements:
                placement_data = {
                    "widget_name": p.widget_name,
                    "widget_type": p.widget_type.name,
                    "position": {"x": p.position.x, "y": p.position.y},
                    "layer": p.layer
                }
                layout_data["placements"].append(placement_data)
            data["layouts"].append(layout_data)

        return data

    def export_config(self):
        filename = filedialog.asksaveasfilename(
            title=UI_TEXT["file_export_title"],
            defaultextension=".conf",
            filetypes=[(UI_TEXT["file_lcd4_config"], "*.conf"), (UI_TEXT["file_all"], "*.*")]
        )
        if not filename:
            return

        try:
            generator = ConfigGenerator()
            config_text = generator.generate(self.project, self.widgets)

            with open(filename, "w", encoding="utf-8") as f:
                f.write(config_text)

            self.statusbar.config(text=get_text("status_exported", path=filename))
            messagebox.showinfo(UI_TEXT["export_complete"], get_text("export_complete_msg", path=filename))

        except Exception as e:
            messagebox.showerror(UI_TEXT["error_title"], get_text("error_export_failed", error=str(e)))

    def show_help(self):
        messagebox.showinfo(UI_TEXT["help_title"], UI_TEXT["help_content"])

    def show_about(self):
        messagebox.showinfo(UI_TEXT["about_title"], UI_TEXT["about_content"])

    def on_closing(self):
        if messagebox.askokcancel(UI_TEXT["confirm_exit"], UI_TEXT["confirm_exit_msg"]):
            self.destroy()


class WidgetEditorWindow(tk.Toplevel):
    def __init__(self, parent, widget_config, callback):
        super().__init__(parent)
        self.widget_config = widget_config
        self.callback = callback
        self.title(f"{UI_TEXT['edit_widget']}: {widget_config.name}")

        self._create_ui()
        self._populate_fields()

    def _create_ui(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        general_tab = ttk.Frame(notebook, padding=10)
        notebook.add(general_tab, text=UI_TEXT["tab_general"])
        self._create_general_tab(general_tab)

        style_tab = ttk.Frame(notebook, padding=10)
        notebook.add(style_tab, text=UI_TEXT["tab_style"])
        self._create_style_tab(style_tab)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(button_frame, text="确定", command=self.save_and_close).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="取消", command=self.destroy).pack(side=tk.RIGHT)

    def _create_general_tab(self, parent):
        row = 0

        ttk.Label(parent, text=UI_TEXT["label_widget_name"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar(value=self.widget_config.name)
        ttk.Entry(parent, textvariable=self.name_var, width=30).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1

        ttk.Label(parent, text=UI_TEXT["label_update_ms"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.update_var = tk.StringVar(value=str(getattr(self.widget_config, "update", 1000)))
        ttk.Entry(parent, textvariable=self.update_var, width=30).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1

        if hasattr(self.widget_config, "expression"):
            ttk.Label(parent, text=UI_TEXT["label_expression"]).grid(row=row, column=0, sticky=tk.W, pady=5)
            self.expression_var = tk.StringVar(value=getattr(self.widget_config, "expression", ""))
            ttk.Entry(parent, textvariable=self.expression_var, width=30).grid(row=row, column=1, sticky=tk.W, pady=5)
            row += 1

            ttk.Label(parent, text=UI_TEXT["label_prefix"]).grid(row=row, column=0, sticky=tk.W, pady=5)
            self.prefix_var = tk.StringVar(value=getattr(self.widget_config, "prefix", ""))
            ttk.Entry(parent, textvariable=self.prefix_var, width=30).grid(row=row, column=1, sticky=tk.W, pady=5)
            row += 1

            ttk.Label(parent, text=UI_TEXT["label_postfix"]).grid(row=row, column=0, sticky=tk.W, pady=5)
            self.postfix_var = tk.StringVar(value=getattr(self.widget_config, "postfix", ""))
            ttk.Entry(parent, textvariable=self.postfix_var, width=30).grid(row=row, column=1, sticky=tk.W, pady=5)
            row += 1

            ttk.Label(parent, text=UI_TEXT["label_width_chars"]).grid(row=row, column=0, sticky=tk.W, pady=5)
            self.width_var = tk.StringVar(value=str(getattr(self.widget_config, "width", 10)))
            ttk.Entry(parent, textvariable=self.width_var, width=30).grid(row=row, column=1, sticky=tk.W, pady=5)
            row += 1

            ttk.Label(parent, text=UI_TEXT["label_precision"]).grid(row=row, column=0, sticky=tk.W, pady=5)
            self.precision_var = tk.StringVar(value=str(getattr(self.widget_config, "precision", 0)))
            ttk.Spinbox(parent, from_=0, to=10, textvariable=self.precision_var, width=28).grid(row=row, column=1, sticky=tk.W, pady=5)
            row += 1

            ttk.Label(parent, text=UI_TEXT["label_align"]).grid(row=row, column=0, sticky=tk.W, pady=5)
            self.align_var = tk.StringVar(value=getattr(self.widget_config, "align", "L"))
            align_combo = ttk.Combobox(parent, textvariable=self.align_var,
                                       values=["L", "C", "R", "M", "A", "PL", "PC", "PR"], width=28)
            align_combo.grid(row=row, column=1, sticky=tk.W, pady=5)
            row += 1

        if hasattr(self.widget_config, "file"):
            ttk.Label(parent, text=UI_TEXT["label_file"]).grid(row=row, column=0, sticky=tk.W, pady=5)
            self.file_var = tk.StringVar(value=getattr(self.widget_config, "file", ""))
            ttk.Entry(parent, textvariable=self.file_var, width=25).grid(row=row, column=1, sticky=tk.W, pady=5)
            ttk.Button(parent, text="...", width=3, command=self.browse_file).grid(row=row, column=2, sticky=tk.W, padx=5)
            row += 1

            ttk.Label(parent, text=UI_TEXT["label_visible"]).grid(row=row, column=0, sticky=tk.W, pady=5)
            self.visible_var = tk.StringVar(value=str(getattr(self.widget_config, "visible", 1)))
            ttk.Entry(parent, textvariable=self.visible_var, width=30).grid(row=row, column=1, sticky=tk.W, pady=5)
            row += 1

        if hasattr(self.widget_config, "length"):
            ttk.Label(parent, text=UI_TEXT["label_length"]).grid(row=row, column=0, sticky=tk.W, pady=5)
            self.length_var = tk.StringVar(value=str(getattr(self.widget_config, "length", 10)))
            ttk.Entry(parent, textvariable=self.length_var, width=30).grid(row=row, column=1, sticky=tk.W, pady=5)
            row += 1

            ttk.Label(parent, text=UI_TEXT["label_min"]).grid(row=row, column=0, sticky=tk.W, pady=5)
            self.min_var = tk.StringVar(value=str(getattr(self.widget_config, "min_val", 0)))
            ttk.Entry(parent, textvariable=self.min_var, width=30).grid(row=row, column=1, sticky=tk.W, pady=5)
            row += 1

            ttk.Label(parent, text=UI_TEXT["label_max"]).grid(row=row, column=0, sticky=tk.W, pady=5)
            self.max_var = tk.StringVar(value=str(getattr(self.widget_config, "max_val", 100)))
            ttk.Entry(parent, textvariable=self.max_var, width=30).grid(row=row, column=1, sticky=tk.W, pady=5)
            row += 1

            ttk.Label(parent, text=UI_TEXT["label_direction"]).grid(row=row, column=0, sticky=tk.W, pady=5)
            self.direction_var = tk.StringVar(value=getattr(self.widget_config, "direction", "E"))
            dir_combo = ttk.Combobox(parent, textvariable=self.direction_var,
                                     values=["E", "W", "N", "S"], width=28)
            dir_combo.grid(row=row, column=1, sticky=tk.W, pady=5)
            row += 1

    def _create_style_tab(self, parent):
        row = 0

        ttk.Label(parent, text=UI_TEXT["label_foreground"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        fg_color = getattr(self.widget_config, "foreground", "000000")
        self.fg_color_btn = tk.Button(parent, bg=f"#{fg_color}", width=5, command=self.choose_fg_color)
        self.fg_color_btn.grid(row=row, column=1, sticky=tk.W, pady=5)
        self.fg_color_var = tk.StringVar(value=fg_color)
        ttk.Entry(parent, textvariable=self.fg_color_var, width=20).grid(row=row, column=2, sticky=tk.W, pady=5)
        row += 1

        ttk.Label(parent, text=UI_TEXT["label_background"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        bg_color = getattr(self.widget_config, "background", "ffffff")
        self.bg_color_btn = tk.Button(parent, bg=f"#{bg_color}", width=5, command=self.choose_bg_color)
        self.bg_color_btn.grid(row=row, column=1, sticky=tk.W, pady=5)
        self.bg_color_var = tk.StringVar(value=bg_color)
        ttk.Entry(parent, textvariable=self.bg_color_var, width=20).grid(row=row, column=2, sticky=tk.W, pady=5)
        row += 1

        if hasattr(self.widget_config, "barcolor0"):
            ttk.Label(parent, text=UI_TEXT["label_bar_color_0"]).grid(row=row, column=0, sticky=tk.W, pady=5)
            bar0_color = getattr(self.widget_config, "barcolor0", "ff0000")
            self.bar0_color_btn = tk.Button(parent, bg=f"#{bar0_color}", width=5, command=self.choose_bar0_color)
            self.bar0_color_btn.grid(row=row, column=1, sticky=tk.W, pady=5)
            self.bar0_color_var = tk.StringVar(value=bar0_color)
            ttk.Entry(parent, textvariable=self.bar0_color_var, width=20).grid(row=row, column=2, sticky=tk.W, pady=5)
            row += 1

            ttk.Label(parent, text=UI_TEXT["label_bar_color_1"]).grid(row=row, column=0, sticky=tk.W, pady=5)
            bar1_color = getattr(self.widget_config, "barcolor1", "00ff00")
            self.bar1_color_btn = tk.Button(parent, bg=f"#{bar1_color}", width=5, command=self.choose_bar1_color)
            self.bar1_color_btn.grid(row=row, column=1, sticky=tk.W, pady=5)
            self.bar1_color_var = tk.StringVar(value=bar1_color)
            ttk.Entry(parent, textvariable=self.bar1_color_var, width=20).grid(row=row, column=2, sticky=tk.W, pady=5)
            row += 1

    def _populate_fields(self):
        pass

    def choose_fg_color(self):
        color = colorchooser.askcolor(color=self.fg_color_var.get(), parent=self)
        if color[1]:
            hex_color = color[1].lstrip("#")
            self.fg_color_var.set(hex_color)
            self.fg_color_btn.config(bg=f"#{hex_color}")

    def choose_bg_color(self):
        color = colorchooser.askcolor(color=self.bg_color_var.get(), parent=self)
        if color[1]:
            hex_color = color[1].lstrip("#")
            self.bg_color_var.set(hex_color)
            self.bg_color_btn.config(bg=f"#{hex_color}")

    def choose_bar0_color(self):
        color = colorchooser.askcolor(color=self.bar0_color_var.get(), parent=self)
        if color[1]:
            hex_color = color[1].lstrip("#")
            self.bar0_color_var.set(hex_color)
            self.bar0_color_btn.config(bg=f"#{hex_color}")

    def choose_bar1_color(self):
        color = colorchooser.askcolor(color=self.bar1_color_var.get(), parent=self)
        if color[1]:
            hex_color = color[1].lstrip("#")
            self.bar1_color_var.set(hex_color)
            self.bar1_color_btn.config(bg=f"#{hex_color}")

    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="选择图片",
            filetypes=[("PNG 图片", "*.png"), (UI_TEXT["file_all"], "*.*")]
        )
        if filename:
            self.file_var.set(filename)

    def save_and_close(self):
        old_name = self.widget_config.name
        new_name = self.name_var.get()

        self.widget_config.name = new_name

        if hasattr(self.widget_config, "update"):
            self.widget_config.update = int(self.update_var.get())
        if hasattr(self.widget_config, "expression"):
            self.widget_config.expression = self.expression_var.get()
            self.widget_config.prefix = self.prefix_var.get()
            self.widget_config.postfix = self.postfix_var.get()
            self.widget_config.width = int(self.width_var.get())
            self.widget_config.precision = int(self.precision_var.get())
            self.widget_config.align = self.align_var.get()
        if hasattr(self.widget_config, "file"):
            self.widget_config.file = self.file_var.get()
            self.widget_config.visible = int(self.visible_var.get())
        if hasattr(self.widget_config, "length"):
            self.widget_config.length = int(self.length_var.get())
            self.widget_config.min_val = float(self.min_var.get())
            self.widget_config.max_val = float(self.max_var.get())
            self.widget_config.direction = self.direction_var.get()
        if hasattr(self.widget_config, "foreground"):
            self.widget_config.foreground = self.fg_color_var.get()
        if hasattr(self.widget_config, "background"):
            self.widget_config.background = self.bg_color_var.get()
        if hasattr(self.widget_config, "barcolor0"):
            self.widget_config.barcolor0 = self.bar0_color_var.get()
        if hasattr(self.widget_config, "barcolor1"):
            self.widget_config.barcolor1 = self.bar1_color_var.get()

        self.callback(old_name, self.widget_config)
        self.destroy()


def main():
    app = LCD4LinuxEditor()
    app.mainloop()


if __name__ == "__main__":
    main()
