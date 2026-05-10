"""
summary_frame.py
Monthly summary: totals cards + bar chart + Excel export.
"""
from __future__ import annotations

import tkinter as tk
from datetime import date as dt_date
from pathlib import Path
import customtkinter as ctk
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from services import get_monthly_summary, export_to_excel, PAYMENT_LABELS
from utils import format_clp
from ui import styles as s


class SummaryFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=s.COLOR_BG, **kwargs)
        self._canvas_widget = None
        self._fig = None
        self._build_ui()

    # ── Build ─────────────────────────────────────────────────────────────────

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # ── Title + filter bar ────────────────────────────────────────────────
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", padx=s.PAD_LG, pady=(s.PAD_LG, 0))
        top.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(top, text="Resumen Mensual", font=s.FONT_XL, text_color=s.COLOR_TEXT) \
            .grid(row=0, column=0, sticky="w")

        filter_row = ctk.CTkFrame(self, fg_color=s.COLOR_CARD, corner_radius=s.CORNER_RADIUS)
        filter_row.grid(row=1, column=0, sticky="ew", padx=s.PAD_LG, pady=s.PAD_SM)
        filter_row.grid_columnconfigure((0, 1, 2), weight=1)

        self._month_var = tk.StringVar(value=dt_date.today().strftime("%Y-%m"))
        ctk.CTkLabel(filter_row, text="Mes (AAAA-MM)", font=s.FONT_SM, text_color=s.COLOR_TEXT_MUTED, anchor="w") \
            .grid(row=0, column=0, sticky="w", padx=s.PAD_MD, pady=(s.PAD_SM, 2))
        ctk.CTkEntry(filter_row, textvariable=self._month_var, font=s.FONT_MD, height=32) \
            .grid(row=1, column=0, sticky="ew", padx=s.PAD_MD, pady=(0, s.PAD_SM))

        ctk.CTkButton(
            filter_row, text="Actualizar", width=100, height=32, font=s.FONT_SM,
            fg_color=s.COLOR_ACCENT, hover_color=s.COLOR_ACCENT_HOVER,
            command=self.refresh,
        ).grid(row=1, column=1, sticky="w", padx=s.PAD_SM, pady=(0, s.PAD_SM))

        ctk.CTkButton(
            filter_row, text="⬇ Exportar a Excel", width=160, height=32, font=s.FONT_SM,
            fg_color=s.COLOR_SUCCESS, hover_color="#2E9960",
            command=self._export,
        ).grid(row=1, column=2, sticky="e", padx=s.PAD_MD, pady=(0, s.PAD_SM))

        # ── Content area ──────────────────────────────────────────────────────
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.grid(row=2, column=0, sticky="nsew", padx=s.PAD_LG, pady=(0, s.PAD_MD))
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=2)
        content.grid_rowconfigure(0, weight=1)

        # Left: totals panel
        self._totals_panel = ctk.CTkFrame(content, fg_color=s.COLOR_CARD, corner_radius=s.CORNER_RADIUS)
        self._totals_panel.grid(row=0, column=0, sticky="nsew", padx=(0, s.PAD_SM))

        # Right: chart panel
        self._chart_panel = ctk.CTkFrame(content, fg_color=s.COLOR_CARD, corner_radius=s.CORNER_RADIUS)
        self._chart_panel.grid(row=0, column=1, sticky="nsew", padx=(s.PAD_SM, 0))
        self._chart_panel.grid_columnconfigure(0, weight=1)
        self._chart_panel.grid_rowconfigure(0, weight=1)

        # Export feedback
        self._export_label = ctk.CTkLabel(self, text="", font=s.FONT_SM, text_color=s.COLOR_SUCCESS)
        self._export_label.grid(row=3, column=0, sticky="e", padx=s.PAD_LG, pady=(0, s.PAD_SM))

        self.refresh()

    # ── Public API ────────────────────────────────────────────────────────────

    def refresh(self):
        month = self._month_var.get().strip() or None
        summary = get_monthly_summary(month=month)
        self._render_totals(summary)
        self._render_chart(summary)

    # ── Totals ────────────────────────────────────────────────────────────────

    def _render_totals(self, summary: dict):
        for w in self._totals_panel.winfo_children():
            w.destroy()

        self._totals_panel.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self._totals_panel, text="Totales", font=s.FONT_LG, text_color=s.COLOR_TEXT
        ).grid(row=0, column=0, sticky="w", padx=s.PAD_MD, pady=(s.PAD_MD, s.PAD_SM))

        # Tarjeta total general
        self._stat_card(
            self._totals_panel, row=1,
            label="Total General",
            value=format_clp(summary['total']),
            value_color=s.COLOR_SUCCESS,
        )

        ctk.CTkLabel(
            self._totals_panel, text="Por Método de Pago",
            font=(s.FONT_FAMILY, 11, "bold"), text_color=s.COLOR_TEXT_MUTED,
        ).grid(row=2, column=0, sticky="w", padx=s.PAD_MD, pady=(s.PAD_MD, 0))

        for row_offset, (pm, amount) in enumerate(summary["by_payment"].items(), start=3):
            color = s.PAYMENT_COLORS.get(pm, s.COLOR_ACCENT)
            self._stat_card(
                self._totals_panel, row=row_offset,
                label=PAYMENT_LABELS.get(pm, pm),
                value=format_clp(amount),
                value_color=color,
                small=True,
            )

        ctk.CTkLabel(
            self._totals_panel, text="Por Categoría",
            font=(s.FONT_FAMILY, 11, "bold"), text_color=s.COLOR_TEXT_MUTED,
        ).grid(row=6, column=0, sticky="w", padx=s.PAD_MD, pady=(s.PAD_MD, 0))

        cat_scroll = ctk.CTkScrollableFrame(self._totals_panel, fg_color="transparent", label_text="")
        cat_scroll.grid(row=7, column=0, sticky="nsew", padx=s.PAD_SM, pady=(0, s.PAD_SM))
        cat_scroll.grid_columnconfigure(0, weight=1)
        self._totals_panel.grid_rowconfigure(7, weight=1)

        if not summary["by_category"]:
            ctk.CTkLabel(cat_scroll, text="Sin datos", font=s.FONT_SM, text_color=s.COLOR_TEXT_MUTED) \
                .grid(row=0, column=0, pady=s.PAD_SM)
        else:
            for cat_row, (cat, amount) in enumerate(summary["by_category"].items()):
                self._stat_card(cat_scroll, row=cat_row, label=cat, value=format_clp(amount), small=True)

        count = summary.get("count", 0)
        ctk.CTkLabel(
            self._totals_panel, text=f"{count} gasto(s) en este período",
            font=s.FONT_SM, text_color=s.COLOR_TEXT_MUTED,
        ).grid(row=8, column=0, sticky="e", padx=s.PAD_MD, pady=(0, s.PAD_MD))

    def _stat_card(self, parent, row, label, value, value_color=None, small=False):
        card = ctk.CTkFrame(parent, fg_color=s.COLOR_BG, corner_radius=8)
        card.grid(row=row, column=0, sticky="ew", padx=s.PAD_SM, pady=3)
        card.grid_columnconfigure(0, weight=1)

        font_label = s.FONT_SM if small else s.FONT_MD
        font_value = s.FONT_MD if small else s.FONT_LG

        ctk.CTkLabel(card, text=label, font=font_label, text_color=s.COLOR_TEXT_MUTED, anchor="w") \
            .grid(row=0, column=0, sticky="w", padx=s.PAD_SM, pady=(4, 0))
        ctk.CTkLabel(card, text=value, font=font_value,
                     text_color=value_color or s.COLOR_TEXT, anchor="e") \
            .grid(row=0, column=1, sticky="e", padx=s.PAD_SM, pady=4)

    # ── Chart ─────────────────────────────────────────────────────────────────

    def _render_chart(self, summary: dict):
        # Remove old canvas
        if self._canvas_widget:
            self._canvas_widget.get_tk_widget().destroy()
            plt.close(self._fig)

        by_cat = summary.get("by_category", {})

        self._fig, ax = plt.subplots(figsize=(6, 4))
        self._fig.patch.set_facecolor(s.COLOR_CARD)
        ax.set_facecolor(s.COLOR_CARD)

        if by_cat:
            categories = list(by_cat.keys())
            amounts = list(by_cat.values())

            bar_colors = [
                "#5B8DEF", "#3DBC78", "#B06EF5", "#F0A050",
                "#E05252", "#00C8C8", "#F5C518", "#8888FF",
            ]
            colors = [bar_colors[i % len(bar_colors)] for i in range(len(categories))]

            bars = ax.barh(categories[::-1], amounts[::-1], color=colors[::-1], height=0.55)
            ax.bar_label(bars, fmt="$%.2f", label_type="edge", color=s.COLOR_TEXT, fontsize=9, padding=4)
            ax.set_xlabel("Amount ($)", color=s.COLOR_TEXT_MUTED, fontsize=9)
            ax.tick_params(colors=s.COLOR_TEXT, labelsize=9)
            ax.spines[:].set_color(s.COLOR_BORDER)
            for spine in ax.spines.values():
                spine.set_alpha(0.3)
            ax.xaxis.label.set_color(s.COLOR_TEXT_MUTED)
        else:
            ax.text(
                0.5, 0.5, "Sin datos para este período",
                ha="center", va="center", color=s.COLOR_TEXT_MUTED,
                transform=ax.transAxes, fontsize=12,
            )
            ax.set_xticks([])
            ax.set_yticks([])

        ax.set_title("Gastos por Categoría", color=s.COLOR_TEXT, fontsize=11, pad=10)
        self._fig.tight_layout()

        self._canvas_widget = FigureCanvasTkAgg(self._fig, master=self._chart_panel)
        self._canvas_widget.draw()
        self._canvas_widget.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=s.PAD_SM, pady=s.PAD_SM)

    # ── Export ────────────────────────────────────────────────────────────────

    def _export(self):
        month = self._month_var.get().strip() or None
        filename = f"expenses_{month or 'all'}.xlsx"
        output_path = Path.home() / "Downloads" / filename
        try:
            saved = export_to_excel(output_path, month=month)
            self._export_label.configure(
                text=f"✓ Guardado en {saved}", text_color=s.COLOR_SUCCESS
            )
        except Exception as exc:
            self._export_label.configure(
                text=f"Error al exportar: {exc}", text_color=s.COLOR_DANGER
            )
