# -*- coding: utf-8 -*-
"""
LCD4Linux Visual Editor - Entry Point
鍏ュ彛鏂囦欢 - 涓嶄娇鐢ㄧ浉瀵瑰鍏?"""

import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

if getattr(sys, 'frozen', False):
    if hasattr(sys, '_MEIPASS'):
        app_dir = os.path.join(sys._MEIPASS, 'src')
    else:
        exe_dir = os.path.dirname(sys.executable)
        app_dir = os.path.join(exe_dir, '_internal', 'src')
else:
    app_dir = script_dir

sys.path.insert(0, app_dir)

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import json
from dataclasses import dataclass, asdict, field
from enum import Enum
from typing import Dict, List, Optional, Any

from models import (
    WidgetType, Alignment, BarDirection, BarStyle,
    DisplayConfig, LayoutPosition, WidgetPlacement,
    LayoutConfig, VariablesConfig, ProjectConfig, DRIVER_CATEGORIES
)
from widgets.text_widget import TextWidgetConfig
from widgets.bar_widget import BarWidgetConfig
from widgets.image_widget import ImageWidgetConfig
from widgets.timer_widget import TimerWidgetConfig
from widgets.icon_widget import IconWidgetConfig
from widgets.graph_widget import GraphWidgetConfig
from widgets.arc_widget import ArcWidgetConfig
from utils.config_generator import ConfigGenerator
from i18n import get_text, UI_TEXT, get_driver_name


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

        ttk.Button(toolbar, text=UI_TEXT["menu_new"].replace("鏂板缓椤圭洰", "鏂板缓"), style="ToolButton.TButton", command=self.new_project).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text=UI_TEXT["menu_open"].replace("鎵撳紑...", "鎵撳紑"), style="ToolButton.TButton", command=self.open_project).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text=UI_TEXT["menu_save"].replace("淇濆瓨", "淇濆瓨"), style="ToolButton.TButton", command=self.save_project).pack(side=tk.LEFT, padx=2)

        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self._create_display_config(notebook)
        self._create_widgets_panel(notebook)
        self._create_layout_panel(notebook)
        self._create_variables_panel(notebook)

    def _create_display_config(self, notebook):
        display_tab = ttk.Frame(notebook)
        notebook.add(display_tab, text=UI_TEXT["tab_display"])

        canvas = tk.Canvas(display_tab)
        scrollbar = ttk.Scrollbar(display_tab, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        frame = ttk.LabelFrame(scroll_frame, text=UI_TEXT["display_settings"], style="Config.TLabelframe", padding=10)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        row = 0
        ttk.Label(frame, text=UI_TEXT["label_name"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.display_name = ttk.Entry(frame, width=25)
        self.display_name.insert(0, self.project.display.name)
        self.display_name.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1

        ttk.Label(frame, text=UI_TEXT["label_driver"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        all_drivers = []
        for cat, drivers in DRIVER_CATEGORIES.items():
            all_drivers.extend(drivers)
        self.display_driver = ttk.Combobox(frame, values=all_drivers, width=22)
        self.display_driver.set(self.project.display.driver)
        self.display_driver.grid(row=row, column=1, sticky=tk.W, pady=5)
        self.display_driver.bind("<<ComboboxSelected>>", self._on_driver_changed)
        row += 1

        ttk.Label(frame, text=UI_TEXT["label_port"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.display_port = ttk.Entry(frame, width=25)
        self.display_port.insert(0, self.project.display.port)
        self.display_port.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1

        ttk.Label(frame, text=UI_TEXT["label_font"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.display_font = ttk.Entry(frame, width=25)
        self.display_font.insert(0, self.project.display.font)
        self.display_font.grid(row=row, column=1, sticky=tk.W, pady=5)
        ttk.Button(frame, text="...", width=3, command=self.browse_font).grid(row=row, column=2, sticky=tk.W, padx=2)
        row += 1

        ttk.Label(frame, text=UI_TEXT["label_font_size"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.display_font_size = ttk.Spinbox(frame, from_=8, to=64, width=22)
        self.display_font_size.set(self.project.display.font_size)
        self.display_font_size.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1

        ttk.Label(frame, text=UI_TEXT["label_width"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.display_width = ttk.Spinbox(frame, from_=16, to=1920, width=22)
        self.display_width.set(self.project.display.width)
        self.display_width.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1

        ttk.Label(frame, text=UI_TEXT["label_height"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.display_height = ttk.Spinbox(frame, from_=16, to=1080, width=22)
        self.display_height.set(self.project.display.height)
        self.display_height.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1

        ttk.Label(frame, text=UI_TEXT["label_bpp"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.display_bpp = ttk.Combobox(frame, values=["1", "2", "4", "8", "16", "24", "32"], width=22)
        self.display_bpp.set(str(self.project.display.bpp))
        self.display_bpp.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1

        ttk.Label(frame, text=UI_TEXT["label_orientation"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.display_orientation = ttk.Combobox(frame, values=[
            UI_TEXT["orientation_landscape"],
            UI_TEXT["orientation_portrait"],
            UI_TEXT["orientation_rev_landscape"],
            UI_TEXT["orientation_rev_portrait"]
        ], width=22)
        self.display_orientation.current(self.project.display.orientation)
        self.display_orientation.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1

        ttk.Label(frame, text=UI_TEXT["label_backlight"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.display_backlight = ttk.Scale(frame, from_=0, to=7, orient=tk.HORIZONTAL, length=150)
        self.display_backlight.set(self.project.display.backlight)
        self.display_backlight.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1

        self.vnc_frame = ttk.LabelFrame(frame, text="VNC璁剧疆", padding=5)
        self.vnc_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=10)
        
        ttk.Label(self.vnc_frame, text=UI_TEXT["label_vnc_port"]).grid(row=0, column=0, sticky=tk.W, pady=2)
        self.vnc_port = ttk.Spinbox(self.vnc_frame, from_=1024, to=65535, width=20)
        self.vnc_port.set(self.project.display.vnc_port)
        self.vnc_port.grid(row=0, column=1, sticky=tk.W, pady=2)
        self.vnc_frame.grid_remove()
        row += 1

        self.x11_frame = ttk.LabelFrame(frame, text="X11璁剧疆", padding=5)
        self.x11_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=10)
        
        ttk.Label(self.x11_frame, text=UI_TEXT["label_x11_display"]).grid(row=0, column=0, sticky=tk.W, pady=2)
        self.x11_display = ttk.Entry(self.x11_frame, width=20)
        self.x11_display.insert(0, self.project.display.x11_display)
        self.x11_display.grid(row=0, column=1, sticky=tk.W, pady=2)
        self.x11_frame.grid_remove()
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

        self._on_driver_changed()
        self.display_port.bind("<FocusOut>", lambda e: self.update_display_config())
        self.display_width.bind("<FocusOut>", lambda e: self.update_display_config())
        self.display_height.bind("<FocusOut>", lambda e: self.update_display_config())
        self.display_driver.bind("<<ComboboxSelected>>", lambda e: self.update_display_config())
        self.display_font.bind("<FocusOut>", lambda e: self.update_display_config())
        self.display_font_size.bind("<FocusOut>", lambda e: self.update_display_config())
        self.display_orientation.bind("<<ComboboxSelected>>", lambda e: self.update_display_config())
        self.display_backlight.bind("<ButtonRelease-1>", lambda e: self.update_display_config())
        self.display_bpp.bind("<<ComboboxSelected>>", lambda e: self.update_display_config())

    def _on_driver_changed(self):
        driver = self.display_driver.get()
        if driver == "VNC":
            self.vnc_frame.grid()
            self.x11_frame.grid_remove()
        elif driver == "X11":
            self.vnc_frame.grid_remove()
            self.x11_frame.grid()
        else:
            self.vnc_frame.grid_remove()
            self.x11_frame.grid_remove()

    def browse_font(self):
        filename = filedialog.askopenfilename(title="閫夋嫨瀛椾綋鏂囦欢", filetypes=[("TTF瀛椾綋", "*.ttf *.TTC"), ("鎵€鏈夋枃浠?, "*.*")])
        if filename:
            self.display_font.delete(0, tk.END)
            self.display_font.insert(0, filename)
            self.update_display_config()

    def _create_widgets_panel(self, notebook):
        widgets_tab = ttk.Frame(notebook)
        notebook.add(widgets_tab, text=UI_TEXT["tab_widgets"])

        toolbar = ttk.Frame(widgets_tab)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        ttk.Button(toolbar, text=UI_TEXT["btn_add_text"], command=lambda: self.add_widget(WidgetType.TEXT)).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text=UI_TEXT["btn_add_bar"], command=lambda: self.add_widget(WidgetType.BAR)).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text=UI_TEXT["btn_add_image"], command=lambda: self.add_widget(WidgetType.IMAGE)).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text=UI_TEXT["btn_add_timer"], command=lambda: self.add_widget(WidgetType.TIMER)).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text=UI_TEXT["btn_add_icon"], command=lambda: self.add_widget(WidgetType.ICON)).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text=UI_TEXT["btn_add_graph"], command=lambda: self.add_widget(WidgetType.GRAPH)).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text=UI_TEXT["btn_add_arc"], command=lambda: self.add_widget(WidgetType.ARC)).pack(side=tk.LEFT, padx=2)

        tree_frame = ttk.Frame(widgets_tab)
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

    def _create_layout_panel(self, notebook):
        layout_tab = ttk.Frame(notebook)
        notebook.add(layout_tab, text=UI_TEXT["tab_layout"])

        toolbar = ttk.Frame(layout_tab)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        ttk.Label(toolbar, text=UI_TEXT["label_layout"]).pack(side=tk.LEFT, padx=5)
        self.layout_combo = ttk.Combobox(toolbar, values=["Default"], width=15, state="readonly")
        self.layout_combo.pack(side=tk.LEFT, padx=5)
        self.layout_combo.bind("<<ComboboxSelected>>", self.select_layout)

        ttk.Button(toolbar, text=UI_TEXT["btn_add_layout"], command=self.add_layout).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text=UI_TEXT["btn_delete_layout"], command=self.delete_layout).pack(side=tk.LEFT, padx=5)

        info_frame = ttk.LabelFrame(layout_tab, text=UI_TEXT["layout_info"], padding=10)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.layout_info = tk.Text(info_frame, height=8, bg="#2b2b2b", fg="#ffffff",
                                    relief=tk.FLAT, wrap=tk.WORD)
        self.layout_info.pack(fill=tk.BOTH, expand=True)
        self.update_layout_info()

    def _create_variables_panel(self, notebook):
        variables_tab = ttk.Frame(notebook)
        notebook.add(variables_tab, text=UI_TEXT["tab_variables"])

        frame = ttk.LabelFrame(variables_tab, text=UI_TEXT["global_variables"], padding=10)
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

        self.canvas = tk.Canvas(canvas_frame, bg="#1a1a1a",
                               xscrollcommand=self.canvas_scroll_x.set,
                               yscrollcommand=self.canvas_scroll_y.set,
                               highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas_scroll_x.config(command=self.canvas.xview)
        self.canvas_scroll_y.config(command=self.canvas.yview)

        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<B1-Motion>", self.canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.canvas_release)
        self.canvas.bind("<MouseWheel>", self.canvas_zoom)

        self._draw_canvas()

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
                self.canvas.create_line(10 + x, 10, 10 + x, 10 + scaled_height, fill="#333333", tags="grid")
            for y in range(0, scaled_height + 1, grid_size):
                self.canvas.create_line(10, 10 + y, 10 + scaled_width, 10 + y, fill="#333333", tags="grid")

        self.canvas.create_text(10 + scaled_width // 2, 10 + scaled_height + 20,
                                text=f"{width}x{height}", fill="#888888", tags="size_label")

        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self._draw_widgets_on_canvas()

    def _draw_widgets_on_canvas(self):
        for placement in self.project.layouts[0].placements:
            widget = self.widgets.get(placement.widget_name)
            if widget:
                self._draw_widget(placement, widget)

    def _draw_widget(self, placement, widget):
        x = int(10 + placement.position.x * self.canvas_scale)
        y = int(10 + placement.position.y * self.canvas_scale)

        colors = {WidgetType.TEXT: "#4a9eff", WidgetType.BAR: "#ff6b4a",
                  WidgetType.IMAGE: "#4aff6b", WidgetType.TIMER: "#ffaa4a", WidgetType.ICON: "#aa4aff",
                  WidgetType.GRAPH: "#00ffaa", WidgetType.ARC: "#ffaa00"}
        wtype_names = {WidgetType.TEXT: UI_TEXT["widget_type_text"], WidgetType.BAR: UI_TEXT["widget_type_bar"],
                       WidgetType.IMAGE: UI_TEXT["widget_type_image"], WidgetType.TIMER: UI_TEXT["widget_type_timer"],
                       WidgetType.ICON: UI_TEXT["widget_type_icon"], WidgetType.GRAPH: UI_TEXT["widget_type_graph"],
                       WidgetType.ARC: UI_TEXT["widget_type_arc"]}

        width = 80 * self.canvas_scale
        height = 30 * self.canvas_scale
        if placement.widget_type == WidgetType.IMAGE:
            width, height = 60 * self.canvas_scale, 60 * self.canvas_scale
        elif placement.widget_type == WidgetType.BAR:
            width, height = 100 * self.canvas_scale, 20 * self.canvas_scale
        elif placement.widget_type == WidgetType.GRAPH:
            width, height = 100 * self.canvas_scale, 40 * self.canvas_scale
        elif placement.widget_type == WidgetType.ARC:
            width, height = 80 * self.canvas_scale, 50 * self.canvas_scale

        rect = self.canvas.create_rectangle(x, y, x + width, y + height,
                                            fill=colors.get(placement.widget_type, "#888888"),
                                            outline="#ffffff", width=2, tags=f"widget_{placement.widget_name}")
        self.canvas.tag_bind(rect, "<Button-1>", lambda e, w=placement.widget_name: self.select_widget_on_canvas(w))
        self.canvas.tag_bind(rect, "<B1-Motion>", lambda e, w=placement.widget_name: self.drag_widget(w, e))
        self.canvas.tag_bind(rect, "<Button-3>", lambda e, w=placement.widget_name: self.show_widget_context_menu(e, w))

        self.canvas.create_text(x + width/2, y + height/2, text=wtype_names.get(placement.widget_type, "WIDGET"),
                                fill="#ffffff", tags=f"text_{placement.widget_name}")
        self.canvas.create_text(x + 3, y + 3, text=placement.widget_name,
                                fill="#ffffff", anchor=tk.NW, font=("Arial", 8), tags=f"label_{placement.widget_name}")

    def select_widget_on_canvas(self, widget_name):
        self.canvas.delete("selection")
        placement = next((p for p in self.project.layouts[0].placements if p.widget_name == widget_name), None)
        if placement:
            x, y = int(10 + placement.position.x * self.canvas_scale), int(10 + placement.position.y * self.canvas_scale)
            self.canvas.create_rectangle(x - 2, y - 2, x + 82, y + 32, outline="#00ff00", width=2, tags="selection")
        self.widgets_tree.selection_set(widget_name)

    def drag_widget(self, widget_name, event):
        if self.drag_start is None:
            self.drag_start = (event.x, event.y)
            placement = next((p for p in self.project.layouts[0].placements if p.widget_name == widget_name), None)
            if placement:
                self.drag_original = (placement.position.x, placement.position.y)
            return

        dx, dy = (event.x - self.drag_start[0]) / self.canvas_scale, (event.y - self.drag_start[1]) / self.canvas_scale
        if self.drag_original:
            placement = next((p for p in self.project.layouts[0].placements if p.widget_name == widget_name), None)
            if placement:
                placement.position.x = max(0, int(self.drag_original[0] + dx))
                placement.position.y = max(0, int(self.drag_original[1] + dy))
                self._draw_canvas()

    def canvas_release(self, event):
        self.drag_start = None
        self.drag_original = None

    def canvas_click(self, event): pass
    def canvas_drag(self, event): pass

    def canvas_zoom(self, event):
        self.zoom_canvas(1.1 if event.delta > 0 else 0.9)

    def zoom_canvas(self, factor):
        self.canvas_scale = max(0.25, min(4.0, self.canvas_scale * factor))
        self.zoom_label.config(text=f"{int(self.canvas_scale * 100)}%")
        self._draw_canvas()

    def reset_zoom(self):
        self.canvas_scale = 1.0
        self.zoom_label.config(text="100%")
        self._draw_canvas()

    def add_widget(self, widget_type):
        name = f"{widget_type.value.lower()}_{len(self.widgets) + 1}"
        config_classes = {WidgetType.TEXT: TextWidgetConfig, WidgetType.BAR: BarWidgetConfig,
                         WidgetType.IMAGE: ImageWidgetConfig, WidgetType.TIMER: TimerWidgetConfig,
                         WidgetType.ICON: IconWidgetConfig, WidgetType.GRAPH: GraphWidgetConfig,
                         WidgetType.ARC: ArcWidgetConfig}
        config = config_classes.get(widget_type, TextWidgetConfig)()
        config.name = name
        self.widgets[name] = config
        self.project.layouts[0].placements.append(WidgetPlacement(widget_name=name, widget_type=widget_type,
                                                                     position=LayoutPosition(x=10, y=10)))
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
        if widget:
            self.current_widget = widget
            self._open_widget_editor(widget)

    def _open_widget_editor(self, widget):
        editor = WidgetEditorWindow(self, widget, self._on_widget_updated)
        editor.grab_set()

    def _on_widget_updated(self, widget_name, widget_config):
        self.widgets[widget_name] = widget_config
        self._draw_canvas()
        widget_type = widget_config.__class__.__name__.replace("WidgetConfig", "")
        try:
            wtype = WidgetType[widget_type.upper()]
        except:
            wtype = WidgetType.TEXT
        for item in self.widgets_tree.get_children():
            if self.widgets_tree.item(item, "iid") == widget_name:
                self.widgets_tree.item(item, values=(wtype.value, getattr(widget_config, "expression", getattr(widget_config, "file", ""))[:30], getattr(widget_config, "update", 1000)))
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
        self.project.layouts[0].placements = [p for p in self.project.layouts[0].placements if p.widget_name != widget_name]
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
        self.project.display.name = self.display_name.get()
        self.project.display.driver = self.display_driver.get()
        self.project.display.port = self.display_port.get()
        self.project.display.font = self.display_font.get()
        self.project.display.font_size = int(self.display_font_size.get())
        self.project.display.width = int(self.display_width.get())
        self.project.display.height = int(self.display_height.get())
        self.project.display.bpp = int(self.display_bpp.get())
        self.project.display.orientation = self.display_orientation.current()
        self.project.display.backlight = int(self.display_backlight.get())
        self.project.display.vnc_port = int(self.vnc_port.get())
        self.project.display.x11_display = self.x11_display.get()
        self._on_driver_changed()
        self._draw_canvas()

    def update_variables(self):
        self.project.variables.tick = int(self.tick_var.get())

    def add_layout(self):
        name = f"Layout_{len(self.project.layouts) + 1}"
        self.project.layouts.append(LayoutConfig(name=name))
        self.layout_combo["values"] = [l.name for l in self.project.layouts]
        self.layout_combo.set(name)
        self.update_layout_info()

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
        self.project.active_layout = self.layout_combo.get()
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

        ttk.Button(dialog, text="娣诲姞", command=save).grid(row=2, column=0, columnspan=2, pady=10)

    def update_layout_info(self):
        layout = self.project.layouts[0] if self.project.layouts else None
        if not layout:
            return
        info = f"甯冨眬: {layout.name}\n缁勪欢鏁? {len(layout.placements)}\n\n缁勪欢浣嶇疆:\n"
        for p in layout.placements:
            widget = self.widgets.get(p.widget_name)
            if widget:
                info += f"  - {p.widget_name} ({widget.__class__.__name__.replace('WidgetConfig', '')})\n"
                info += f"    浣嶇疆: ({p.position.x}, {p.position.y})\n    鍥惧眰: {p.layer}\n"
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
        filename = filedialog.askopenfilename(title=UI_TEXT["file_open_title"],
                                             filetypes=[(UI_TEXT["file_lcd4_project"], "*.lcd4"), (UI_TEXT["file_all"], "*.*")])
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
            self.display_font.delete(0, tk.END)
            self.display_font.insert(0, self.project.display.font)
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
                self.widgets_tree.insert("", "end", iid=name, values=(wt.value, getattr(widget, "expression", getattr(widget, "file", ""))[:30], getattr(widget, "update", 1000)))
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
        variables = VariablesConfig(tick=variables_data.get("tick", 500), custom_vars=variables_data.get("custom_vars", {}))
        return ProjectConfig(display=display, layouts=layouts, active_layout=data.get("active_layout", "Default"), variables=variables, file_path=data.get("file_path"))

    def _create_widget_from_config(self, placement):
        widget_classes = {WidgetType.TEXT: TextWidgetConfig, WidgetType.BAR: BarWidgetConfig,
                          WidgetType.IMAGE: ImageWidgetConfig, WidgetType.TIMER: TimerWidgetConfig,
                          WidgetType.ICON: IconWidgetConfig, WidgetType.GRAPH: GraphWidgetConfig,
                          WidgetType.ARC: ArcWidgetConfig}
        return widget_classes.get(placement.widget_type, TextWidgetConfig)(name=placement.widget_name)

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
        filename = filedialog.asksaveasfilename(title=UI_TEXT["file_save_title"], defaultextension=".lcd4",
                                                filetypes=[(UI_TEXT["file_lcd4_project"], "*.lcd4"), (UI_TEXT["file_all"], "*.*")])
        if filename:
            self.project.file_path = filename
            self.save_project()

    def _serialize_project(self):
        data = {"display": asdict(self.project.display), "layouts": [], "active_layout": self.project.active_layout,
                "variables": {"tick": self.project.variables.tick, "custom_vars": self.project.variables.custom_vars},
                "file_path": self.project.file_path}
        for layout in self.project.layouts:
            layout_data = {"name": layout.name, "placements": []}
            for p in layout.placements:
                layout_data["placements"].append({"widget_name": p.widget_name, "widget_type": p.widget_type.name,
                                                  "position": {"x": p.position.x, "y": p.position.y}, "layer": p.layer})
            data["layouts"].append(layout_data)
        return data

    def export_config(self):
        filename = filedialog.asksaveasfilename(title=UI_TEXT["file_export_title"], defaultextension=".conf",
                                                filetypes=[(UI_TEXT["file_lcd4_config"], "*.conf"), (UI_TEXT["file_all"], "*.*")])
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
        
        widget_class = self.widget_config.__class__.__name__
        if widget_class == "GraphWidgetConfig":
            graph_tab = ttk.Frame(notebook, padding=10)
            notebook.add(graph_tab, text="鍥捐〃璁剧疆")
            self._create_graph_tab(graph_tab)
        elif widget_class == "ArcWidgetConfig":
            arc_tab = ttk.Frame(notebook, padding=10)
            notebook.add(arc_tab, text="浠〃璁剧疆")
            self._create_arc_tab(arc_tab)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        ttk.Button(button_frame, text="纭畾", command=self.save_and_close).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="鍙栨秷", command=self.destroy).pack(side=tk.RIGHT)

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
            for label, var, default in [(UI_TEXT["label_expression"], "expression", ""), (UI_TEXT["label_prefix"], "prefix", ""),
                                       (UI_TEXT["label_postfix"], "postfix", ""), (UI_TEXT["label_width_chars"], "width", 10),
                                       (UI_TEXT["label_precision"], "precision", 0), (UI_TEXT["label_align"], "align", "L")]:
                ttk.Label(parent, text=label).grid(row=row, column=0, sticky=tk.W, pady=5)
                value = getattr(self.widget_config, var, default)
                if var == "width" or var == "precision":
                    ttk.Entry(parent, textvariable=tk.StringVar(value=str(value)), width=30).grid(row=row, column=1, sticky=tk.W, pady=5)
                elif var == "align":
                    ttk.Combobox(parent, textvariable=tk.StringVar(value=value), values=["L", "C", "R", "M", "A", "PL", "PC", "PR"], width=28).grid(row=row, column=1, sticky=tk.W, pady=5)
                else:
                    ttk.Entry(parent, textvariable=tk.StringVar(value=str(value)), width=30).grid(row=row, column=1, sticky=tk.W, pady=5)
                row += 1
        if hasattr(self.widget_config, "file"):
            ttk.Label(parent, text=UI_TEXT["label_file"]).grid(row=row, column=0, sticky=tk.W, pady=5)
            self.file_var = tk.StringVar(value=getattr(self.widget_config, "file", ""))
            ttk.Entry(parent, textvariable=self.file_var, width=25).grid(row=row, column=1, sticky=tk.W, pady=5)
            ttk.Button(parent, text="...", width=3, command=self.browse_file).grid(row=row, column=2, sticky=tk.W, padx=5)
            row += 1

    def _create_style_tab(self, parent):
        row = 0
        for label, attr, default in [(UI_TEXT["label_foreground"], "foreground", "000000"),
                                      (UI_TEXT["label_background"], "background", "ffffff")]:
            ttk.Label(parent, text=label).grid(row=row, column=0, sticky=tk.W, pady=5)
            color = getattr(self.widget_config, attr, default)
            btn = tk.Button(parent, bg=f"#{color}", width=5, command=lambda a=attr, c=color: self._choose_color(a, c))
            btn.grid(row=row, column=1, sticky=tk.W, pady=5)
            entry = ttk.Entry(parent, textvariable=tk.StringVar(value=color), width=20)
            entry.grid(row=row, column=2, sticky=tk.W, pady=5)
            row += 1

    def _create_graph_tab(self, parent):
        row = 0
        ttk.Label(parent, text=UI_TEXT["label_expression"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.graph_expr_var = tk.StringVar(value=getattr(self.widget_config, "expression", ""))
        ttk.Entry(parent, textvariable=self.graph_expr_var, width=30).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(parent, text=UI_TEXT["label_graph_width"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.graph_width_var = tk.StringVar(value=str(getattr(self.widget_config, "width", 100)))
        ttk.Entry(parent, textvariable=self.graph_width_var, width=30).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(parent, text=UI_TEXT["label_graph_height"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.graph_height_var = tk.StringVar(value=str(getattr(self.widget_config, "height", 40)))
        ttk.Entry(parent, textvariable=self.graph_height_var, width=30).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(parent, text=UI_TEXT["label_min"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.graph_min_var = tk.StringVar(value=str(getattr(self.widget_config, "min_val", 0)))
        ttk.Entry(parent, textvariable=self.graph_min_var, width=30).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(parent, text=UI_TEXT["label_max"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.graph_max_var = tk.StringVar(value=str(getattr(self.widget_config, "max_val", 100)))
        ttk.Entry(parent, textvariable=self.graph_max_var, width=30).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(parent, text=UI_TEXT["label_graph_points"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.graph_points_var = tk.StringVar(value=str(getattr(self.widget_config, "points", 50)))
        ttk.Entry(parent, textvariable=self.graph_points_var, width=30).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(parent, text=UI_TEXT["label_graph_style"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.graph_style_var = tk.StringVar(value=str(getattr(self.widget_config, "style", 0)))
        ttk.Combobox(parent, textvariable=self.graph_style_var, values=["0-绾挎潯", "1-濉厖"], width=28).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(parent, text=UI_TEXT["label_graph_color"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.graph_color_var = tk.StringVar(value=getattr(self.widget_config, "color", "00FF00"))
        ttk.Entry(parent, textvariable=self.graph_color_var, width=20).grid(row=row, column=1, sticky=tk.W, pady=5)
        ttk.Button(parent, text="...", width=3, command=lambda: self._choose_color("color", self.graph_color_var.get())).grid(row=row, column=2, sticky=tk.W, padx=5)
        row += 1
        
        ttk.Label(parent, text=UI_TEXT["label_graph_fill"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.graph_fill_var = tk.StringVar(value=getattr(self.widget_config, "fill", "003300"))
        ttk.Entry(parent, textvariable=self.graph_fill_var, width=20).grid(row=row, column=1, sticky=tk.W, pady=5)
        ttk.Button(parent, text="...", width=3, command=lambda: self._choose_color("fill", self.graph_fill_var.get())).grid(row=row, column=2, sticky=tk.W, padx=5)
        row += 1
        
        ttk.Label(parent, text=UI_TEXT["label_graph_grid"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.graph_grid_var = tk.StringVar(value=getattr(self.widget_config, "grid", "404040"))
        ttk.Entry(parent, textvariable=self.graph_grid_var, width=20).grid(row=row, column=1, sticky=tk.W, pady=5)
        ttk.Button(parent, text="...", width=3, command=lambda: self._choose_color("grid", self.graph_grid_var.get())).grid(row=row, column=2, sticky=tk.W, padx=5)
        row += 1
        
        ttk.Label(parent, text=UI_TEXT["label_background"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.graph_bg_var = tk.StringVar(value=getattr(self.widget_config, "bg", "000000"))
        ttk.Entry(parent, textvariable=self.graph_bg_var, width=20).grid(row=row, column=1, sticky=tk.W, pady=5)
        ttk.Button(parent, text="...", width=3, command=lambda: self._choose_color("bg", self.graph_bg_var.get())).grid(row=row, column=2, sticky=tk.W, padx=5)

    def _create_arc_tab(self, parent):
        row = 0
        ttk.Label(parent, text=UI_TEXT["label_expression"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.arc_expr_var = tk.StringVar(value=getattr(self.widget_config, "expression", ""))
        ttk.Entry(parent, textvariable=self.arc_expr_var, width=30).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(parent, text=UI_TEXT["label_graph_width"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.arc_width_var = tk.StringVar(value=str(getattr(self.widget_config, "width", 80)))
        ttk.Entry(parent, textvariable=self.arc_width_var, width=30).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(parent, text=UI_TEXT["label_graph_height"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.arc_height_var = tk.StringVar(value=str(getattr(self.widget_config, "height", 50)))
        ttk.Entry(parent, textvariable=self.arc_height_var, width=30).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(parent, text=UI_TEXT["label_min"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.arc_min_var = tk.StringVar(value=str(getattr(self.widget_config, "min_val", 0)))
        ttk.Entry(parent, textvariable=self.arc_min_var, width=30).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(parent, text=UI_TEXT["label_max"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.arc_max_var = tk.StringVar(value=str(getattr(self.widget_config, "max_val", 100)))
        ttk.Entry(parent, textvariable=self.arc_max_var, width=30).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(parent, text=UI_TEXT["label_arc_style"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.arc_style_var = tk.StringVar(value=getattr(self.widget_config, "style", "semi"))
        ttk.Combobox(parent, textvariable=self.arc_style_var, values=["semi", "quarter", "full"], width=28).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(parent, text=UI_TEXT["label_arc_ticks"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.arc_ticks_var = tk.StringVar(value=str(getattr(self.widget_config, "ticks", 5)))
        ttk.Entry(parent, textvariable=self.arc_ticks_var, width=30).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(parent, text=UI_TEXT["label_arc_minor"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.arc_minor_var = tk.StringVar(value=str(getattr(self.widget_config, "minor", 5)))
        ttk.Entry(parent, textvariable=self.arc_minor_var, width=30).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(parent, text=UI_TEXT["label_arc_thickness"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.arc_thickness_var = tk.StringVar(value=str(getattr(self.widget_config, "thickness", 8)))
        ttk.Entry(parent, textvariable=self.arc_thickness_var, width=30).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(parent, text=UI_TEXT["label_arc_arc"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.arc_arc_var = tk.StringVar(value=getattr(self.widget_config, "arc", "404040"))
        ttk.Entry(parent, textvariable=self.arc_arc_var, width=20).grid(row=row, column=1, sticky=tk.W, pady=5)
        ttk.Button(parent, text="...", width=3, command=lambda: self._choose_color("arc", self.arc_arc_var.get())).grid(row=row, column=2, sticky=tk.W, padx=5)
        row += 1
        
        ttk.Label(parent, text=UI_TEXT["label_arc_needle"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.arc_needle_var = tk.StringVar(value=getattr(self.widget_config, "needle", "FF0000"))
        ttk.Entry(parent, textvariable=self.arc_needle_var, width=20).grid(row=row, column=1, sticky=tk.W, pady=5)
        ttk.Button(parent, text="...", width=3, command=lambda: self._choose_color("needle", self.arc_needle_var.get())).grid(row=row, column=2, sticky=tk.W, padx=5)
        row += 1
        
        ttk.Label(parent, text=UI_TEXT["label_arc_center"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.arc_center_var = tk.StringVar(value=getattr(self.widget_config, "center", "808080"))
        ttk.Entry(parent, textvariable=self.arc_center_var, width=20).grid(row=row, column=1, sticky=tk.W, pady=5)
        ttk.Button(parent, text="...", width=3, command=lambda: self._choose_color("center", self.arc_center_var.get())).grid(row=row, column=2, sticky=tk.W, padx=5)
        row += 1
        
        ttk.Label(parent, text=UI_TEXT["label_background"]).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.arc_bg_var = tk.StringVar(value=getattr(self.widget_config, "bg", "000000"))
        ttk.Entry(parent, textvariable=self.arc_bg_var, width=20).grid(row=row, column=1, sticky=tk.W, pady=5)
        ttk.Button(parent, text="...", width=3, command=lambda: self._choose_color("bg", self.arc_bg_var.get())).grid(row=row, column=2, sticky=tk.W, padx=5)

    def _choose_color(self, attr, current_color):
        color = colorchooser.askcolor(color=current_color, parent=self)
        if color[1]:
            setattr(self.widget_config, attr, color[1].lstrip("#"))

    def browse_file(self):
        filename = filedialog.askopenfilename(title="閫夋嫨鍥剧墖", filetypes=[("PNG 鍥剧墖", "*.png"), ("鎵€鏈夋枃浠?, "*.*")])
        if filename:
            self.file_var.set(filename)

    def _populate_fields(self): pass

    def save_and_close(self):
        self.widget_config.name = self.name_var.get()
        if hasattr(self.widget_config, "update"):
            self.widget_config.update = int(self.update_var.get())
        if hasattr(self.widget_config, "expression"):
            self.widget_config.expression = getattr(self.widget_config, "expression", "")
        
        widget_class = self.widget_config.__class__.__name__
        if widget_class == "GraphWidgetConfig":
            self.widget_config.expression = self.graph_expr_var.get()
            self.widget_config.width = int(self.graph_width_var.get())
            self.widget_config.height = int(self.graph_height_var.get())
            self.widget_config.min_val = float(self.graph_min_var.get())
            self.widget_config.max_val = float(self.graph_max_var.get())
            self.widget_config.points = int(self.graph_points_var.get())
            self.widget_config.style = int(self.graph_style_var.get().split("-")[0])
            self.widget_config.color = self.graph_color_var.get()
            self.widget_config.fill = self.graph_fill_var.get()
            self.widget_config.bg = self.graph_bg_var.get()
            self.widget_config.grid = self.graph_grid_var.get()
        elif widget_class == "ArcWidgetConfig":
            self.widget_config.expression = self.arc_expr_var.get()
            self.widget_config.width = int(self.arc_width_var.get())
            self.widget_config.height = int(self.arc_height_var.get())
            self.widget_config.min_val = float(self.arc_min_var.get())
            self.widget_config.max_val = float(self.arc_max_var.get())
            self.widget_config.style = self.arc_style_var.get()
            self.widget_config.ticks = int(self.arc_ticks_var.get())
            self.widget_config.minor = int(self.arc_minor_var.get())
            self.widget_config.thickness = int(self.arc_thickness_var.get())
            self.widget_config.arc = self.arc_arc_var.get()
            self.widget_config.needle = self.arc_needle_var.get()
            self.widget_config.center = self.arc_center_var.get()
            self.widget_config.bg = self.arc_bg_var.get()
        
        self.callback(self.widget_config.name, self.widget_config)
        self.destroy()


def main():
    app = LCD4LinuxEditor()
    app.mainloop()


if __name__ == "__main__":
    main()
