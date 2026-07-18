"""
Smart Rainwater Harvesting and Energy Estimation System
PyQt5 User Interface — Theme-Switchable Edition

Changes from previous version:
  - Analyze button has white text (clearly visible on cyan gradient)
  - Water quality status labels shown as plain colored text (no pill backgrounds)
  - Theme toggle button (🌙 / ☀️) in the header switches Dark ↔ Light instantly
"""

import sys
import pandas as pd
import joblib
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QComboBox, QTextEdit, QGroupBox,
    QRadioButton, QButtonGroup, QMessageBox, QFrame, QScrollArea,
    QGridLayout, QSlider, QSplitter
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextCursor


# ═══════════════════════════════════════════════════════════════════════════════
#  THEME DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════════════

DARK = {
    "name":        "dark",
    "BG":          "#0d1117",
    "SURFACE":     "#161b22",
    "CARD":        "#1c2333",
    "BORDER":      "#30363d",
    "ACCENT":      "#00d4ff",
    "ACCENT2":     "#00ff9d",
    "TEXT":        "#e6edf3",
    "MUTED":       "#8b949e",
    "SUCCESS":     "#3fb950",
    "WARNING":     "#d29922",
    "DANGER":      "#f85149",
    "ENERGY":      "#f0883e",
    "INPUT_BG":    "#161b22",
    "INPUT_FOCUS": "#1c2333",
    "SCROLL_BG":   "#161b22",
    "SCROLL_HDL":  "#30363d",
    "GROUP_BG":    "#161b22",
    "HEADER_G1":   "#0d1f2d",
    "HEADER_G2":   "#0a2640",
    "HEADER_G3":   "#061a2e",
    "HEADER_BDR":  "#1e3a52",
    "TITLE_COLOR": "#00d4ff",
    "SUB_COLOR":   "#8b949e",
    "TOGGLE_ICON": "☀️",
    "TOGGLE_TIP":  "Switch to Light Mode",
}

LIGHT = {
    "name":        "light",
    "BG":          "#f0f4f8",
    "SURFACE":     "#ffffff",
    "CARD":        "#f8fafc",
    "BORDER":      "#d0d7de",
    "ACCENT":      "#0969da",
    "ACCENT2":     "#1a7f37",
    "TEXT":        "#1f2328",
    "MUTED":       "#57606a",
    "SUCCESS":     "#1a7f37",
    "WARNING":     "#9a6700",
    "DANGER":      "#cf222e",
    "ENERGY":      "#bc4c00",
    "INPUT_BG":    "#ffffff",
    "INPUT_FOCUS": "#f6f8fa",
    "SCROLL_BG":   "#f6f8fa",
    "SCROLL_HDL":  "#d0d7de",
    "GROUP_BG":    "#ffffff",
    "HEADER_G1":   "#0969da",
    "HEADER_G2":   "#0550ae",
    "HEADER_G3":   "#033d8b",
    "HEADER_BDR":  "#0550ae",
    "TITLE_COLOR": "#ffffff",
    "SUB_COLOR":   "#cce5ff",
    "TOGGLE_ICON": "🌙",
    "TOGGLE_TIP":  "Switch to Dark Mode",
}


def build_stylesheet(t: dict) -> str:
    return f"""
    QMainWindow, QWidget {{
        background-color: {t['BG']};
        color: {t['TEXT']};
    }}
    QLabel {{
        color: {t['TEXT']};
        font-family: 'Segoe UI', 'Ubuntu', sans-serif;
    }}

    /* ── Base button (fallback for zoom/misc buttons) ──────────────── */
    QPushButton {{
        background: transparent;
        color: {t['TEXT']};
        border: 1px solid {t['BORDER']};
        padding: 10px 24px;
        border-radius: 6px;
        font-size: 14px;
        font-weight: bold;
        font-family: 'Segoe UI', 'Ubuntu', sans-serif;
        letter-spacing: 0.5px;
    }}
    QPushButton:hover {{
        background: {t['SURFACE']};
        color: {t['TEXT']};
        border: 1px solid {t['MUTED']};
    }}
    QPushButton:pressed {{
        background: {t['BORDER']};
    }}
    QPushButton:disabled {{
        background: transparent;
        color: {t['MUTED']};
        border: 1px solid {t['BORDER']};
    }}

    QLineEdit {{
        padding: 9px 12px;
        border: 1px solid {t['BORDER']};
        border-radius: 6px;
        background-color: {t['INPUT_BG']};
        color: {t['TEXT']};
        font-size: 13px;
        font-family: 'Segoe UI', 'Ubuntu', sans-serif;
        selection-background-color: {t['ACCENT']};
        selection-color: #ffffff;
    }}
    QLineEdit:focus {{
        border: 1px solid {t['ACCENT']};
        background-color: {t['INPUT_FOCUS']};
    }}

    QComboBox {{
        padding: 9px 12px;
        border: 1px solid {t['BORDER']};
        border-radius: 6px;
        background-color: {t['INPUT_BG']};
        color: {t['TEXT']};
        font-size: 13px;
        font-family: 'Segoe UI', 'Ubuntu', sans-serif;
        min-width: 140px;
    }}
    QComboBox:focus {{ border: 1px solid {t['ACCENT']}; }}
    QComboBox::drop-down {{ border: none; width: 24px; }}
    QComboBox::down-arrow {{
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 6px solid {t['MUTED']};
        margin-right: 6px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {t['SURFACE']};
        border: 1px solid {t['BORDER']};
        color: {t['TEXT']};
        selection-background-color: {t['ACCENT']}30;
        selection-color: {t['ACCENT']};
        padding: 4px;
    }}

    QGroupBox {{
        font-weight: bold;
        font-size: 13px;
        font-family: 'Segoe UI', 'Ubuntu', sans-serif;
        border: 1px solid {t['BORDER']};
        border-radius: 10px;
        margin-top: 14px;
        padding-top: 14px;
        background-color: {t['GROUP_BG']};
        color: {t['TEXT']};
    }}
    QGroupBox::title {{
        color: {t['ACCENT']};
        subcontrol-origin: margin;
        left: 14px;
        padding: 0 8px;
        letter-spacing: 0.5px;
    }}

    QRadioButton {{
        font-size: 13px;
        color: {t['TEXT']};
        font-family: 'Segoe UI', 'Ubuntu', sans-serif;
        spacing: 8px;
    }}
    QRadioButton::indicator {{
        width: 16px; height: 16px;
        border-radius: 8px;
        border: 2px solid {t['BORDER']};
        background-color: {t['INPUT_BG']};
    }}
    QRadioButton::indicator:checked {{
        border: 2px solid {t['ACCENT']};
        background-color: {t['ACCENT']};
    }}
    QRadioButton::indicator:hover {{ border: 2px solid {t['ACCENT']}; }}

    QTextEdit {{
        border: 1px solid {t['BORDER']};
        border-radius: 8px;
        background-color: {t['BG']};
        color: {t['TEXT']};
        font-size: 13px;
        font-family: 'Consolas', 'Cascadia Code', 'Monaco', monospace;
        padding: 4px;
        selection-background-color: {t['ACCENT']}40;
        selection-color: {t['TEXT']};
    }}

    QScrollArea {{ border: none; background-color: transparent; }}
    QScrollBar:vertical {{
        border: none; background: {t['SCROLL_BG']};
        width: 10px; margin: 0px; border-radius: 5px;
    }}
    QScrollBar::handle:vertical {{
        background: {t['SCROLL_HDL']}; min-height: 30px; border-radius: 5px;
    }}
    QScrollBar::handle:vertical:hover {{ background: {t['ACCENT']}; }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
    QScrollBar:horizontal {{
        border: none; background: {t['SCROLL_BG']};
        height: 10px; margin: 0px; border-radius: 5px;
    }}
    QScrollBar::handle:horizontal {{
        background: {t['SCROLL_HDL']}; min-width: 30px; border-radius: 5px;
    }}
    QScrollBar::handle:horizontal:hover {{ background: {t['ACCENT']}; }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0px; }}

    QSlider::groove:horizontal {{
        border: none; height: 6px;
        background: {t['BORDER']}; border-radius: 3px;
    }}
    QSlider::sub-page:horizontal {{
        background: {t['ACCENT']}; border-radius: 3px;
    }}
    QSlider::handle:horizontal {{
        background: {t['ACCENT']};
        border: 2px solid {t['BG']};
        width: 16px; height: 16px;
        margin: -5px 0; border-radius: 8px;
    }}
    QSlider::handle:horizontal:hover {{ background: {t['ACCENT']}cc; }}

    QSplitter::handle {{ background-color: {t['BORDER']}; height: 2px; }}
    QSplitter::handle:hover {{ background-color: {t['ACCENT']}; }}

    QMessageBox {{ background-color: {t['SURFACE']}; color: {t['TEXT']}; }}
    QMessageBox QLabel {{ color: {t['TEXT']}; }}
    QMessageBox QPushButton {{ min-width: 80px; min-height: 32px; }}
    """


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN WINDOW
# ═══════════════════════════════════════════════════════════════════════════════

class RainwaterHarvestingUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dataset      = None
        self.models       = {}
        self.encoders     = None
        self.current_zoom = 100
        self.theme        = DARK          # start in dark mode
        self._last_data   = None          # cache for re-render on theme switch
        self._last_mode   = None

        self.init_ui()
        self.apply_theme()
        self.load_dataset()
        self.load_models()

    # ─────────────────────────────────────────────────────────────────────
    #  THEME
    # ─────────────────────────────────────────────────────────────────────

    def apply_theme(self):
        t = self.theme
        self.setStyleSheet(build_stylesheet(t))

        # Header gradient
        self.header_widget.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {t['HEADER_G1']},
                    stop:0.5 {t['HEADER_G2']},
                    stop:1 {t['HEADER_G3']});
                border-radius: 10px;
                border: 1px solid {t['HEADER_BDR']};
            }}
        """)
        self.header_title.setStyleSheet(f"""
            color: {t['TITLE_COLOR']}; font-size: 22px; font-weight: bold;
            font-family: 'Segoe UI', 'Ubuntu', sans-serif;
            letter-spacing: 0.5px; background: transparent; border: none;
        """)
        self.header_sub.setStyleSheet(f"""
            color: {t['SUB_COLOR']}; font-size: 12px;
            font-family: 'Segoe UI', 'Ubuntu', sans-serif;
            letter-spacing: 1px; background: transparent; border: none;
        """)

        # Toggle button
        self.toggle_btn.setText(f"  {t['TOGGLE_ICON']}  ")
        self.toggle_btn.setToolTip(t['TOGGLE_TIP'])
        self.toggle_btn.setStyleSheet(f"""
            QPushButton {{
                background: {'rgba(255,255,255,0.15)' if t['name']=='dark' else 'rgba(255,255,255,0.3)'};
                color: #ffffff;
                border: 1px solid {'rgba(255,255,255,0.25)' if t['name']=='dark' else 'rgba(255,255,255,0.5)'};
                border-radius: 18px;
                font-size: 18px;
                padding: 4px 10px;
                font-weight: normal;
                letter-spacing: 0px;
            }}
            QPushButton:hover {{
                background: {'rgba(255,255,255,0.25)' if t['name']=='dark' else 'rgba(255,255,255,0.45)'};
            }}
            QPushButton:pressed {{
                background: rgba(255,255,255,0.1);
            }}
        """)

        # Both action buttons — identical ghost/outline style
        action_btn_style = f"""
            QPushButton {{
                background: transparent;
                color: {t['TEXT']};
                border: 1px solid {t['BORDER']};
                padding: 10px 24px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 0.5px;
            }}
            QPushButton:hover {{
                background: {t['SURFACE']};
                color: {t['TEXT']};
                border: 1px solid {t['MUTED']};
            }}
            QPushButton:pressed {{
                background: {t['BORDER']};
            }}
        """
        self.analyze_btn.setStyleSheet(action_btn_style)
        self.clear_btn.setStyleSheet(action_btn_style)

        # Zoom controls bar
        self.zoom_bar.setStyleSheet(f"""
            QWidget {{
                background-color: {t['SURFACE']};
                border-radius: 8px;
                border: 1px solid {t['BORDER']};
            }}
        """)
        self.zoom_lbl.setStyleSheet(f"""
            font-weight: bold; color: {t['MUTED']}; font-size: 12px;
            letter-spacing: 0.5px; background: transparent; border: none;
        """)
        self.zoom_percent_label.setStyleSheet(f"""
            font-weight: bold; color: {t['ACCENT']}; min-width: 46px;
            font-size: 12px; background: transparent; border: none;
        """)
        for btn in [self.zoom_out_btn, self.zoom_in_btn]:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {t['BORDER']};
                    color: {t['TEXT']};
                    font-size: 16px; font-weight: bold;
                    border: none; border-radius: 4px; padding: 0px;
                }}
                QPushButton:hover {{ background: {t['MUTED']}; color: #ffffff; }}
                QPushButton:pressed {{ background: {t['ACCENT']}; color: #ffffff; }}
            """)
        self.zoom_reset_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent; color: {t['MUTED']};
                border: 1px solid {t['BORDER']}; border-radius: 4px;
                font-size: 11px; padding: 0 10px;
            }}
            QPushButton:hover {{ background: {t['SURFACE']}; color: {t['TEXT']}; }}
        """)

        # Top scroll area backgrounds
        self.top_inner.setStyleSheet(f"background-color: {t['BG']};")
        self.bottom_inner.setStyleSheet(f"background-color: {t['BG']};")

        # Label styles inside input groups
        for lbl in self.findChildren(QLabel):
            if lbl.objectName() == "field_label":
                lbl.setStyleSheet(f"""
                    font-weight: bold; color: {t['MUTED']};
                    font-size: 12px; letter-spacing: 0.3px;
                """)

        # Re-render results with new theme colors if data exists
        if self._last_data is not None:
            self.display_results(self._last_data, self._last_mode)

    def toggle_theme(self):
        self.theme = LIGHT if self.theme["name"] == "dark" else DARK
        self.apply_theme()

    # ─────────────────────────────────────────────────────────────────────
    #  UI INIT
    # ─────────────────────────────────────────────────────────────────────

    def init_ui(self):
        self.setWindowTitle("Smart Rainwater Harvesting & Energy Estimation System")
        self.setGeometry(100, 100, 1400, 900)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(16, 16, 16, 16)

        main_layout.addWidget(self._build_header())

        splitter = QSplitter(Qt.Vertical)
        splitter.setHandleWidth(2)

        # Top
        self.top_inner = QWidget()
        top_layout = QVBoxLayout(self.top_inner)
        top_layout.setSpacing(12)
        top_layout.setContentsMargins(4, 4, 4, 4)
        top_layout.addWidget(self._build_input_method_selection())

        self.location_widget = self._build_location_input()
        top_layout.addWidget(self.location_widget)

        self.parameter_scroll = QScrollArea()
        self.parameter_scroll.setWidgetResizable(True)
        self.parameter_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.parameter_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.parameter_widget = self._build_parameter_input()
        self.parameter_scroll.setWidget(self.parameter_widget)
        self.parameter_scroll.hide()
        top_layout.addWidget(self.parameter_scroll)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        self.analyze_btn = QPushButton("⚡  Analyze Data")
        self.analyze_btn.setMinimumHeight(44)
        self.analyze_btn.setCursor(Qt.PointingHandCursor)
        self.analyze_btn.clicked.connect(self.analyze_data)

        self.clear_btn = QPushButton("↺  Clear All")
        self.clear_btn.setMinimumHeight(44)
        self.clear_btn.setCursor(Qt.PointingHandCursor)
        self.clear_btn.clicked.connect(self.clear_all)

        btn_layout.addWidget(self.analyze_btn)
        btn_layout.addWidget(self.clear_btn)
        top_layout.addLayout(btn_layout)
        top_layout.addStretch()

        top_scroll = QScrollArea()
        top_scroll.setWidgetResizable(True)
        top_scroll.setWidget(self.top_inner)
        top_scroll.setMinimumHeight(300)

        # Bottom
        self.bottom_inner = QWidget()
        bottom_layout = QVBoxLayout(self.bottom_inner)
        bottom_layout.setSpacing(10)
        bottom_layout.setContentsMargins(4, 4, 4, 4)
        bottom_layout.addWidget(self._build_zoom_controls())
        bottom_layout.addWidget(self._build_results_section())

        splitter.addWidget(top_scroll)
        splitter.addWidget(self.bottom_inner)
        splitter.setSizes([400, 500])
        main_layout.addWidget(splitter)

    # ─────────────────────────────────────────────────────────────────────
    #  WIDGET BUILDERS
    # ─────────────────────────────────────────────────────────────────────

    def _build_header(self):
        self.header_widget = QWidget()
        self.header_widget.setFixedHeight(90)
        lay = QHBoxLayout(self.header_widget)
        lay.setContentsMargins(24, 10, 16, 10)

        text_lay = QVBoxLayout()
        text_lay.setSpacing(4)
        self.header_title = QLabel("💧  Smart Rainwater Harvesting & Energy Estimation System")
        self.header_title.setAlignment(Qt.AlignCenter)
        self.header_sub = QLabel("Advanced ML-Powered Analysis for Sustainable Water Management")
        self.header_sub.setAlignment(Qt.AlignCenter)
        text_lay.addWidget(self.header_title)
        text_lay.addWidget(self.header_sub)

        self.toggle_btn = QPushButton("  🌙  ")
        self.toggle_btn.setFixedSize(44, 44)
        self.toggle_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_btn.clicked.connect(self.toggle_theme)

        lay.addLayout(text_lay, 1)
        lay.addWidget(self.toggle_btn, 0, Qt.AlignVCenter)
        return self.header_widget

    def _build_zoom_controls(self):
        self.zoom_bar = QWidget()
        lay = QHBoxLayout(self.zoom_bar)
        lay.setContentsMargins(14, 8, 14, 8)
        lay.setSpacing(10)

        self.zoom_lbl = QLabel("🔍  Zoom")
        lay.addWidget(self.zoom_lbl)

        self.zoom_out_btn = QPushButton("−")
        self.zoom_out_btn.setFixedSize(28, 28)
        self.zoom_out_btn.setCursor(Qt.PointingHandCursor)
        self.zoom_out_btn.clicked.connect(self.zoom_out)
        lay.addWidget(self.zoom_out_btn)

        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setMinimum(50)
        self.zoom_slider.setMaximum(200)
        self.zoom_slider.setValue(100)
        self.zoom_slider.setTickPosition(QSlider.TicksBelow)
        self.zoom_slider.setTickInterval(25)
        self.zoom_slider.valueChanged.connect(self.update_zoom)
        self.zoom_slider.setMaximumWidth(260)
        lay.addWidget(self.zoom_slider)

        self.zoom_in_btn = QPushButton("+")
        self.zoom_in_btn.setFixedSize(28, 28)
        self.zoom_in_btn.setCursor(Qt.PointingHandCursor)
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        lay.addWidget(self.zoom_in_btn)

        self.zoom_percent_label = QLabel("100%")
        self.zoom_percent_label.setAlignment(Qt.AlignCenter)
        lay.addWidget(self.zoom_percent_label)

        self.zoom_reset_btn = QPushButton("Reset")
        self.zoom_reset_btn.setFixedHeight(28)
        self.zoom_reset_btn.setCursor(Qt.PointingHandCursor)
        self.zoom_reset_btn.clicked.connect(self.reset_zoom)
        lay.addWidget(self.zoom_reset_btn)
        lay.addStretch()
        return self.zoom_bar

    def _build_input_method_selection(self):
        group = QGroupBox("📋  Select Input Method")
        lay   = QHBoxLayout()
        lay.setSpacing(30)
        lay.setContentsMargins(16, 10, 16, 10)

        self.input_method_group = QButtonGroup()
        self.location_radio  = QRadioButton("🌍  Location-Based Input")
        self.location_radio.setChecked(True)
        self.location_radio.setCursor(Qt.PointingHandCursor)
        self.location_radio.toggled.connect(self.toggle_input_method)
        self.parameter_radio = QRadioButton("⚙️  Direct Parameters Input")
        self.parameter_radio.setCursor(Qt.PointingHandCursor)
        self.input_method_group.addButton(self.location_radio)
        self.input_method_group.addButton(self.parameter_radio)

        lay.addWidget(self.location_radio)
        lay.addWidget(self.parameter_radio)
        lay.addStretch()
        group.setLayout(lay)
        return group

    def _field_label(self, text):
        lbl = QLabel(text)
        lbl.setObjectName("field_label")
        lbl.setStyleSheet(
            f"font-weight: bold; color: {self.theme['MUTED']};"
            "font-size: 12px; letter-spacing: 0.3px;"
        )
        return lbl

    def _build_location_input(self):
        group = QGroupBox("🗺️  Location Information")
        lay   = QGridLayout()
        lay.setSpacing(12)
        lay.setContentsMargins(16, 10, 16, 10)

        for row, (text, attr, ph) in enumerate([
            ("City:",     "city_input",     "e.g., Vijayawada"),
            ("District:", "district_input", "e.g., Krishna"),
            ("State:",    "state_input",    "e.g., Andhra Pradesh"),
        ]):
            lay.addWidget(self._field_label(text), row, 0)
            fld = QLineEdit()
            fld.setPlaceholderText(ph)
            setattr(self, attr, fld)
            lay.addWidget(fld, row, 1)

        group.setLayout(lay)
        return group

    def _build_parameter_input(self):
        group = QGroupBox("⚙️  Direct Parameters")
        lay   = QGridLayout()
        lay.setSpacing(12)
        lay.setContentsMargins(16, 10, 16, 10)

        self.rainfall_intensity_input = self._make_input("Rainfall Intensity (mm/hr):", "e.g., 25.5", lay, 0)
        self.raindrop_size_input      = self._make_input("Raindrop Size (mm):",         "e.g., 3.2",  lay, 1)

        lay.addWidget(self._field_label("Rainfall Type:"), 2, 0)
        self.rainfall_type_combo = QComboBox()
        self.rainfall_type_combo.addItems(["Moderate", "Heavy", "Storm"])
        lay.addWidget(self.rainfall_type_combo, 2, 1)

        self.roof_area_input = self._make_input("Roof Area (m²):", "e.g., 150", lay, 3)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        lay.addWidget(sep, 4, 0, 1, 2)

        hdr = QLabel("💧  Water Quality Parameters")
        hdr.setStyleSheet(
            f"font-weight: bold; color: {self.theme['ACCENT']};"
            "font-size: 13px; letter-spacing: 0.5px; margin-top: 6px;"
        )
        lay.addWidget(hdr, 5, 0, 1, 2)

        self.ph_input        = self._make_input("pH Level:",        "e.g., 7.0  (Acceptable: 6.0 – 9.0)", lay, 6)
        self.tds_input       = self._make_input("TDS (ppm):",       "e.g., 250  (Acceptable: 0 – 900)",   lay, 7)
        self.turbidity_input = self._make_input("Turbidity (NTU):", "e.g., 3.5  (Acceptable: 0 – 10)",   lay, 8)

        legend = QLabel("ℹ️  Thresholds:  pH 6.0–9.0  |  TDS ≤ 900 ppm  |  Turbidity ≤ 10 NTU")
        legend.setStyleSheet(f"color: {self.theme['MUTED']}; font-size: 11px; font-style: italic; margin-top: 6px;")
        lay.addWidget(legend, 9, 0, 1, 2)

        info = QLabel("ℹ️  All fields are required for accurate prediction")
        info.setStyleSheet(f"color: {self.theme['MUTED']}; font-size: 11px; font-style: italic;")
        lay.addWidget(info, 10, 0, 1, 2)

        group.setLayout(lay)
        return group

    def _make_input(self, label_text, placeholder, layout, row):
        layout.addWidget(self._field_label(label_text), row, 0)
        fld = QLineEdit()
        fld.setPlaceholderText(placeholder)
        layout.addWidget(fld, row, 1)
        return fld

    def _build_results_section(self):
        group = QGroupBox("📊  Analysis Results")
        lay   = QVBoxLayout()
        lay.setContentsMargins(12, 8, 12, 12)

        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMinimumHeight(380)
        self.results_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.results_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.results_text.setPlaceholderText("Results will appear here after analysis...")

        lay.addWidget(self.results_text)
        group.setLayout(lay)
        return group

    def toggle_input_method(self):
        if self.location_radio.isChecked():
            self.location_widget.show()
            self.parameter_scroll.hide()
        else:
            self.location_widget.hide()
            self.parameter_scroll.show()

    # ─────────────────────────────────────────────────────────────────────
    #  DATA / MODEL LOADING
    # ─────────────────────────────────────────────────────────────────────

    def load_dataset(self):
        try:
            self.dataset = pd.read_csv(
                r"E:\Documents\SEM-8\SDP\dataset\final_augmented_rainwater_dataset.csv"
            )
            print(f"Dataset loaded! Shape: {self.dataset.shape}")
        except Exception as e:
            QMessageBox.warning(self, "Dataset Error",
                f"Could not load dataset: {str(e)}\n\n"
                "Please ensure the dataset file is in the correct location.")

    def load_models(self):
        try:
            MODEL_DIR = r"E:\Documents\SEM-8\SDP\Models"
            self.models['ph']          = joblib.load(f"{MODEL_DIR}/ph_model.pkl")
            self.models['tds']         = joblib.load(f"{MODEL_DIR}/tds_model.pkl")
            self.models['turbidity']   = joblib.load(f"{MODEL_DIR}/turbidity_model.pkl")
            self.models['harvestable'] = joblib.load(f"{MODEL_DIR}/harvestable_model.pkl")
            self.models['quantity']    = joblib.load(f"{MODEL_DIR}/harvest_quantity_model.pkl")
            self.encoders              = joblib.load(f"{MODEL_DIR}/label_encoders.pkl")
            print("Models loaded!")
        except Exception as e:
            QMessageBox.warning(self, "Model Error",
                f"Could not load models: {str(e)}\n\n"
                "Please ensure model files are in the correct directory.")

    # ─────────────────────────────────────────────────────────────────────
    #  HARVESTABILITY LOGIC
    # ─────────────────────────────────────────────────────────────────────

    def check_harvestable_by_quality(self, ph, tds, turbidity):
        reasons = []
        if not (6.0 <= ph <= 9.0):
            reasons.append(f"pH {ph:.2f} is outside the acceptable range (6.0 – 9.0).")
        if tds > 900:
            reasons.append(f"TDS {tds:.2f} ppm exceeds the acceptable limit (≤ 900 ppm).")
        if turbidity > 10:
            reasons.append(f"Turbidity {turbidity:.2f} NTU exceeds the acceptable limit (≤ 10 NTU).")
        return (len(reasons) == 0), reasons

    def parse_model_harvestable(self, value):
        try:
            v = value.item() if hasattr(value, 'item') else value
            if isinstance(v, bool):          return v
            if isinstance(v, (int, float)):  return int(v) == 1
            if isinstance(v, str):           return v.strip().lower() in ("1", "yes", "true", "harvestable")
            return bool(v)
        except Exception:
            return bool(value)

    # ─────────────────────────────────────────────────────────────────────
    #  ANALYSIS
    # ─────────────────────────────────────────────────────────────────────

    def analyze_data(self):
        if self.location_radio.isChecked():
            self.analyze_by_location()
        else:
            self.analyze_by_parameters()

    def analyze_by_location(self):
        if self.dataset is None:
            QMessageBox.warning(self, "Error", "Dataset not loaded!")
            return
        city     = self.city_input.text().strip()
        district = self.district_input.text().strip()
        state    = self.state_input.text().strip()
        if not all([city, district, state]):
            QMessageBox.warning(self, "Input Error", "Please enter City, District, and State!")
            return
        mask = (
            (self.dataset['city'].str.lower()     == city.lower()) &
            (self.dataset['district'].str.lower() == district.lower()) &
            (self.dataset['state'].str.lower()    == state.lower())
        )
        result = self.dataset[mask]
        if result.empty:
            QMessageBox.warning(self, "Not Found",
                f"No data found for:\n{city}, {district}, {state}\n\nPlease check the spelling.")
            return
        self.display_results(result.iloc[0], mode='location')

    def analyze_by_parameters(self):
        if not self.models:
            QMessageBox.warning(self, "Error", "Models not loaded!")
            return
        try:
            ri_text  = self.rainfall_intensity_input.text().strip()
            rds_text = self.raindrop_size_input.text().strip()
            ra_text  = self.roof_area_input.text().strip()
            ph_text  = self.ph_input.text().strip()
            tds_text = self.tds_input.text().strip()
            tb_text  = self.turbidity_input.text().strip()

            if not all([ri_text, rds_text, ra_text, ph_text, tds_text, tb_text]):
                QMessageBox.warning(self, "Input Error",
                    "Please fill in all required fields:\n"
                    "• Rainfall Intensity\n• Raindrop Size\n• Rainfall Type\n"
                    "• Roof Area\n• pH Level\n• TDS\n• Turbidity")
                return

            try:
                rainfall_intensity = float(ri_text)
                raindrop_size      = float(rds_text)
                roof_area          = float(ra_text)
                ph                 = float(ph_text)
                tds                = float(tds_text)
                turbidity          = float(tb_text)
            except ValueError as ve:
                QMessageBox.warning(self, "Input Error",
                    f"Invalid numeric value.\nUse decimal point (.) not comma (,)\n\nError: {ve}")
                return

            checks = [
                (0 < rainfall_intensity <= 100,  "Rainfall Intensity should be between 0 and 100 mm/hr"),
                (0 < raindrop_size <= 10,         "Raindrop Size should be between 0 and 10 mm"),
                (0 < roof_area <= 1000,           "Roof Area should be between 0 and 1000 m²"),
                (0 <= ph <= 14,                   "pH should be between 0 and 14"),
                (0 <= tds <= 5000,                "TDS should be between 0 and 5000 ppm"),
                (0 <= turbidity <= 100,           "Turbidity should be between 0 and 100 NTU"),
            ]
            for ok, msg in checks:
                if not ok:
                    QMessageBox.warning(self, "Input Error", msg)
                    return

            rainfall_type = self.rainfall_type_combo.currentText()
            try:
                rainfall_type_encoded = self.encoders['rainfall_type'].transform([rainfall_type])[0]
            except Exception as e:
                QMessageBox.critical(self, "Encoding Error",
                    f"Error encoding '{rainfall_type}':\n{e}")
                return

            features = np.array([[
                rainfall_intensity, raindrop_size, rainfall_type_encoded,
                roof_area, ph, tds, turbidity
            ]])
            try:
                quantity = self.models['quantity'].predict(features)[0]
            except Exception as e:
                QMessageBox.critical(self, "Prediction Error", f"Model prediction failed:\n{e}")
                return

            harvestable, fail_reasons = self.check_harvestable_by_quality(ph, tds, turbidity)
            energy = rainfall_intensity * roof_area * 9.8 * 0.001

            result_data = {
                'rainfall_intensity_mm_hr': rainfall_intensity,
                'raindrop_size_mm':         raindrop_size,
                'rainfall_type':            rainfall_type,
                'roof_area_m2':             roof_area,
                'ph':                       ph,
                'tds':                      tds,
                'turbidity':                turbidity,
                'harvestable':              harvestable,
                'harvest_quantity_liters':  quantity,
                'rain_energy_joules':       energy,
                '_fail_reasons':            fail_reasons,
            }
            self.display_results(pd.Series(result_data), mode='parameter')

        except Exception as e:
            QMessageBox.critical(self, "Unexpected Error", f"An unexpected error occurred:\n{e}")
            import traceback; traceback.print_exc()

    # ─────────────────────────────────────────────────────────────────────
    #  ZOOM
    # ─────────────────────────────────────────────────────────────────────

    def zoom_in(self):   self.zoom_slider.setValue(min(200, self.zoom_slider.value() + 10))
    def zoom_out(self):  self.zoom_slider.setValue(max(50,  self.zoom_slider.value() - 10))
    def reset_zoom(self): self.zoom_slider.setValue(100)

    def update_zoom(self, value):
        self.current_zoom = value
        self.zoom_percent_label.setText(f"{value}%")
        t = self.theme
        new_size = int(13 * value / 100)
        self.results_text.setStyleSheet(f"""
            QTextEdit {{
                font-family: 'Consolas', 'Cascadia Code', 'Monaco', monospace;
                font-size: {new_size}px; line-height: 1.5; padding: 10px;
                border: 1px solid {t['BORDER']}; border-radius: 8px;
                background-color: {t['BG']}; color: {t['TEXT']};
            }}
        """)

    # ─────────────────────────────────────────────────────────────────────
    #  DISPLAY RESULTS
    # ─────────────────────────────────────────────────────────────────────

    def display_results(self, data, mode='location'):
        # Cache for theme re-render
        self._last_data = data
        self._last_mode = mode

        t = self.theme

        if mode == 'location':
            harvestable  = self.parse_model_harvestable(data['harvestable'])
            fail_reasons = []
        else:
            harvestable  = bool(data['harvestable'])
            fail_reasons = data.get('_fail_reasons', [])

        tds_v  = data['tds']
        turb_v = data['turbidity']

        BG      = t['BG']
        SURFACE = t['SURFACE']
        CARD    = t['CARD']
        BORDER  = t['BORDER']
        ACCENT  = t['ACCENT']
        ACCENT2 = t['ACCENT2']
        TEXT    = t['TEXT']
        MUTED   = t['MUTED']
        SUCCESS = t['SUCCESS']
        WARNING = t['WARNING']
        DANGER  = t['DANGER']
        ENERGY  = t['ENERGY']

        is_predicted = (mode == 'parameter')

        def row(alt=False):
            bg = CARD if alt else SURFACE
            return f"background-color:{bg}; padding:10px 14px;"

        html = f"""
        <div style='font-family:"Segoe UI",Arial,sans-serif;
                    line-height:1.8; padding:14px;
                    background-color:{BG}; color:{TEXT};'>

        <div style='border-bottom:2px solid {ACCENT};
                    padding-bottom:12px; margin-bottom:18px;'>
            <span style='color:{ACCENT}; font-size:20px; font-weight:bold;
                         letter-spacing:0.5px;'>
                ⚡ &nbsp;Analysis Results
            </span>
            <span style='color:{MUTED}; font-size:11px; margin-left:12px;
                         letter-spacing:1px; text-transform:uppercase;'>
                {'Predicted by ML Model' if is_predicted else 'From Dataset'}
            </span>
        </div>

        <div style='color:{ACCENT2}; font-size:12px; font-weight:bold;
                    letter-spacing:1px; margin-bottom:8px;
                    text-transform:uppercase;'>
            📥 &nbsp;Input Parameters
        </div>
        <table style='width:100%; border-collapse:collapse; border:1px solid {BORDER};'>
        """

        if mode == 'location':
            html += f"""
            <tr>
                <td style='{row(True)} color:{MUTED}; font-weight:bold;
                            width:200px; font-size:12px;'>Location</td>
                <td style='{row(True)} color:{TEXT};'>
                    {data.get('city','N/A')}, {data.get('district','N/A')}, {data.get('state','N/A')}
                </td>
            </tr>"""

        for label, key, unit, alt in [
            ("Rainfall Intensity", "rainfall_intensity_mm_hr", "mm/hr", False),
            ("Raindrop Size",      "raindrop_size_mm",         "mm",    True),
            ("Rainfall Type",      "rainfall_type",            "",      False),
            ("Roof Area",          "roof_area_m2",             "m²",    True),
        ]:
            val     = data[key]
            display = f"{val:.2f} {unit}".strip() if isinstance(val, float) else f"{val} {unit}".strip()
            html += f"""
            <tr>
                <td style='{row(alt)} color:{MUTED}; font-weight:bold; font-size:12px;'>
                    {label}</td>
                <td style='{row(alt)} color:{TEXT};'>{display}</td>
            </tr>"""

        html += "</table>"

        # ── Water Quality ─────────────────────────────────────────────────
        html += f"""
        <div style='color:{ACCENT2}; font-size:12px; font-weight:bold;
                    letter-spacing:1px; margin-bottom:8px; margin-top:20px;
                    text-transform:uppercase;'>
            💧 &nbsp;Water Quality Parameters
        </div>
        <table style='width:100%; border-collapse:collapse; border:1px solid {BORDER};'>
        """

        # pH row — plain colored text, no pill background
        if pd.notna(data['ph']):
            pv       = data['ph']
            st_color, st_icon, st_label = self._status_parts_ph(pv)
            html += f"""
            <tr>
                <td style='{row(True)} color:{MUTED}; font-weight:bold;
                            width:200px; font-size:12px;'>pH Level</td>
                <td style='{row(True)} color:{TEXT};'>
                    <b>{pv:.2f}</b>
                    &nbsp;<span style='color:{st_color}; font-weight:bold;'>{st_icon} {st_label}</span>
                </td>
            </tr>
            <tr><td colspan='2' style='padding:3px 14px 8px; font-size:10px;
                                       color:{MUTED}; background-color:{SURFACE};'>
                Ideal: 6.5–8.5 &nbsp;|&nbsp; Harvestable range: 6.0–9.0
            </td></tr>"""
        else:
            html += f"""
            <tr>
                <td style='{row(True)} color:{MUTED}; font-weight:bold; font-size:12px;'>
                    pH Level</td>
                <td style='{row(True)} color:{MUTED};'>Not Available</td>
            </tr>"""

        # TDS row
        st_color, st_icon, st_label = self._status_parts_tds(tds_v)
        html += f"""
        <tr>
            <td style='{row(False)} color:{MUTED}; font-weight:bold; font-size:12px;'>
                TDS</td>
            <td style='{row(False)} color:{TEXT};'>
                <b>{tds_v:.2f}</b> ppm
                &nbsp;<span style='color:{st_color}; font-weight:bold;'>{st_icon} {st_label}</span>
            </td>
        </tr>
        <tr><td colspan='2' style='padding:3px 14px 8px; font-size:10px;
                                   color:{MUTED}; background-color:{CARD};'>
            Excellent: &lt;300 ppm &nbsp;|&nbsp; Good: 300–600 &nbsp;|&nbsp;
            Fair: 600–900 &nbsp;|&nbsp; Poor: &gt;900 ppm
        </td></tr>"""

        # Turbidity row
        st_color, st_icon, st_label = self._status_parts_turb(turb_v)
        html += f"""
        <tr>
            <td style='{row(True)} color:{MUTED}; font-weight:bold; font-size:12px;'>
                Turbidity</td>
            <td style='{row(True)} color:{TEXT};'>
                <b>{turb_v:.2f}</b> NTU
                &nbsp;<span style='color:{st_color}; font-weight:bold;'>{st_icon} {st_label}</span>
            </td>
        </tr>
        <tr><td colspan='2' style='padding:3px 14px 8px; font-size:10px;
                                   color:{MUTED}; background-color:{SURFACE};'>
            Excellent: &lt;1 NTU &nbsp;|&nbsp; Good: 1–5 &nbsp;|&nbsp;
            Fair: 5–10 &nbsp;|&nbsp; Poor: &gt;10 NTU
        </td></tr>
        </table>"""

        # ── Harvesting ────────────────────────────────────────────────────
        harvest_color = SUCCESS if harvestable else DANGER
        harvest_label = "YES — Suitable for Harvesting" if harvestable else "NO — Not Suitable"
        harvest_icon  = "✅" if harvestable else "❌"
        quantity      = data['harvest_quantity_liters'] if harvestable else 0

        html += f"""
        <div style='color:{ACCENT2}; font-size:12px; font-weight:bold;
                    letter-spacing:1px; margin-bottom:8px; margin-top:20px;
                    text-transform:uppercase;'>
            🌊 &nbsp;Harvesting Information
        </div>
        <table style='width:100%; border-collapse:collapse; border:1px solid {BORDER};'>
        <tr>
            <td style='{row(True)} color:{MUTED}; font-weight:bold;
                        font-size:12px; width:200px;'>Harvestable</td>
            <td style='{row(True)};'>
                <span style='color:{harvest_color}; font-weight:bold; font-size:14px;'>
                    {harvest_icon} &nbsp;{harvest_label}
                </span>
            </td>
        </tr>
        <tr>
            <td style='{row(False)} color:{MUTED}; font-weight:bold; font-size:12px;'>
                Harvest Quantity</td>
            <td style='{row(False)};'>
                <span style='color:{ACCENT}; font-size:18px; font-weight:bold;'>
                    {quantity:.2f}
                </span>
                <span style='color:{MUTED}; font-size:12px;'> Liters</span>
            </td>
        </tr>
        </table>"""

        # ── Energy ────────────────────────────────────────────────────────
        energy = data['rain_energy_joules']
        html += f"""
        <div style='color:{ACCENT2}; font-size:12px; font-weight:bold;
                    letter-spacing:1px; margin-bottom:8px; margin-top:20px;
                    text-transform:uppercase;'>
            ⚡ &nbsp;Energy Generation
        </div>
        <table style='width:100%; border-collapse:collapse; border:1px solid {BORDER};'>
        <tr>
            <td style='{row(True)} color:{MUTED}; font-weight:bold;
                        font-size:12px; width:200px;'>Rain Energy</td>
            <td style='{row(True)};'>
                <span style='color:{ENERGY}; font-size:18px; font-weight:bold;'>
                    {energy:.2f}
                </span>
                <span style='color:{MUTED}; font-size:12px;'> Joules</span>
            </td>
        </tr>
        <tr><td colspan='2' style='padding:3px 14px 8px; font-size:10px;
                                   color:{MUTED}; background-color:{SURFACE};'>
            Equivalent to: {energy / 3600:.4f} Watt-hours (Wh)
        </td></tr>
        </table>"""

        # ── Recommendations ───────────────────────────────────────────────
        rec_border = SUCCESS if harvestable else DANGER
        html += f"""
        <div style='color:{ACCENT2}; font-size:12px; font-weight:bold;
                    letter-spacing:1px; margin-bottom:8px; margin-top:20px;
                    text-transform:uppercase;'>
            💡 &nbsp;Recommendations
        </div>
        <div style='padding:16px 18px; background-color:{SURFACE};
                    border-left:3px solid {rec_border};
                    border-radius:0 6px 6px 0; margin-bottom:20px;
                    border-top:1px solid {BORDER}; border-right:1px solid {BORDER};
                    border-bottom:1px solid {BORDER};'>
        """

        if harvestable:
            html += f"<p style='margin:5px 0; color:{SUCCESS};'>✓ &nbsp;Water quality is suitable for harvesting.</p>"
            if pd.notna(data['ph']):
                pv = data['ph']
                if pv < 6.5 or pv > 8.5:
                    html += f"<p style='margin:8px 0; color:{WARNING};'>⚠ &nbsp;pH is outside the ideal range (6.5–8.5). Consider mild treatment before use.</p>"
            if tds_v > 600:
                html += f"<p style='margin:8px 0; color:{WARNING};'>⚠ &nbsp;TDS is elevated. Consider filtration to improve water quality.</p>"
            if turb_v > 5:
                html += f"<p style='margin:8px 0; color:{WARNING};'>⚠ &nbsp;Turbidity is moderate. Filtration recommended before use.</p>"
        else:
            html += f"<p style='margin:5px 0; color:{DANGER};'>✗ &nbsp;Water quality does not meet minimum harvesting standards.</p>"
            for reason in fail_reasons:
                html += f"<p style='margin:8px 0 0 12px; color:{WARNING};'>• &nbsp;{reason}</p>"
            html += f"<p style='margin:8px 0; color:{MUTED};'>• &nbsp;Advanced filtration and treatment are required before use.</p>"

        html += "</div></div>"

        self.results_text.setHtml(html)
        self.results_text.moveCursor(QTextCursor.Start)
        self.results_text.ensureCursorVisible()

    # ─────────────────────────────────────────────────────────────────────
    #  STATUS HELPERS — return (color, icon, label) tuples, no pill HTML
    # ─────────────────────────────────────────────────────────────────────

    def _status_parts_ph(self, ph):
        t = self.theme
        if 6.5 <= ph <= 8.5:                   return t['SUCCESS'], "✓", "Normal"
        if 6.0 <= ph < 6.5 or 8.5 < ph <= 9.0: return t['WARNING'], "⚠", "Borderline"
        return t['DANGER'], "✗", "Abnormal"

    def _status_parts_tds(self, tds):
        t = self.theme
        if tds < 300: return t['SUCCESS'], "✓", "Excellent"
        if tds < 600: return t['SUCCESS'], "✓", "Good"
        if tds < 900: return t['WARNING'], "⚠", "Fair"
        return t['DANGER'], "✗", "Poor"

    def _status_parts_turb(self, turb):
        t = self.theme
        if turb < 1:  return t['SUCCESS'], "✓", "Excellent"
        if turb < 5:  return t['SUCCESS'], "✓", "Good"
        if turb < 10: return t['WARNING'], "⚠", "Fair"
        return t['DANGER'], "✗", "Poor"

    # kept for backward-compat if anything calls them
    def get_ph_status(self, ph):
        c, i, l = self._status_parts_ph(ph);   return f"{i} {l}"
    def get_tds_status(self, tds):
        c, i, l = self._status_parts_tds(tds); return f"{i} {l}"
    def get_turbidity_status(self, turb):
        c, i, l = self._status_parts_turb(turb); return f"{i} {l}"

    # ─────────────────────────────────────────────────────────────────────
    #  CLEAR
    # ─────────────────────────────────────────────────────────────────────

    def clear_all(self):
        for fld in [
            self.city_input, self.district_input, self.state_input,
            self.rainfall_intensity_input, self.raindrop_size_input,
            self.roof_area_input, self.ph_input, self.tds_input, self.turbidity_input,
        ]:
            fld.clear()
        self.rainfall_type_combo.setCurrentIndex(0)
        self.results_text.clear()
        self.results_text.setPlaceholderText("Results will appear here after analysis...")
        self._last_data = None
        self._last_mode = None


# ═══════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = RainwaterHarvestingUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()