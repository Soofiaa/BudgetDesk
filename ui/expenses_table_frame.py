"""
expenses_table_frame.py
Table view with filters and Edit/Delete actions.
"""
from __future__ import annotations

import tkinter as tk
from datetime import date as dt_date
import customtkinter as ctk

from database import fetch_filtered_expenses, delete_expense, fetch_category_names
from models.expense import Expense
from services import PAYMENT_METHODS, PAYMENT_LABELS, PAYMENT_DISPLAY_NAMES, PAYMENT_DISPLAY_TO_METHOD
from utils import format_clp, date_to_display
from ui import styles as s


class ExpensesTableFrame(ctk.CTkFrame):
    _COLUMNS = ["Fecha", "Descripción", "Categoría", "Método de Pago", "Monto", "Notas", "Acciones"]
    _COL_WEIGHTS = [10, 25, 13, 14, 9, 18, 11]  # relative widths

    def __init__(self, master, on_edit_callback=None, **kwargs):
        super().__init__(master, fg_color=s.COLOR_BG, **kwargs)
        self._on_edit = on_edit_callback
        self._expenses: list[Expense] = []
        self._build_ui()
        self.refresh()

    # ── Build ─────────────────────────────────────────────────────────────────

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Title row
        title_row = ctk.CTkFrame(self, fg_color="transparent")
        title_row.grid(row=0, column=0, sticky="ew", padx=s.PAD_LG, pady=(s.PAD_LG, 0))
        title_row.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(title_row, text="Gastos", font=s.FONT_XL, text_color=s.COLOR_TEXT) \
            .grid(row=0, column=0, sticky="w")

        # Filter bar
        filter_card = ctk.CTkFrame(self, fg_color=s.COLOR_CARD, corner_radius=s.CORNER_RADIUS)
        filter_card.grid(row=1, column=0, sticky="ew", padx=s.PAD_LG, pady=s.PAD_SM)
        filter_card.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Month filter
        self._month_var = tk.StringVar()
        self._add_filter(filter_card, col=0, label="Mes (AAAA-MM)", var=self._month_var, placeholder="ej. 2025-01")

        # Category filter
        self._cat_var = tk.StringVar()
        ctk.CTkLabel(filter_card, text="Categoría", font=s.FONT_SM, text_color=s.COLOR_TEXT_MUTED, anchor="w") \
            .grid(row=0, column=1, sticky="w", padx=s.PAD_MD, pady=(s.PAD_SM, 2))
        self._cat_combo = ctk.CTkComboBox(
            filter_card, variable=self._cat_var,
            values=["(todos)"] + self._load_categories(),
            font=s.FONT_MD, height=32,
        )
        self._cat_combo.set("(todos)")
        self._cat_combo.grid(row=1, column=1, sticky="ew", padx=s.PAD_MD, pady=(0, s.PAD_SM))

        # Payment method filter
        self._pm_var = tk.StringVar()
        ctk.CTkLabel(filter_card, text="Método de Pago", font=s.FONT_SM, text_color=s.COLOR_TEXT_MUTED, anchor="w") \
            .grid(row=0, column=2, sticky="w", padx=s.PAD_MD, pady=(s.PAD_SM, 2))
        self._pm_combo = ctk.CTkComboBox(
            filter_card, variable=self._pm_var,
            values=["(todos)"] + PAYMENT_DISPLAY_NAMES,
            font=s.FONT_MD, height=32,
        )
        self._pm_combo.set("(todos)")
        self._pm_combo.grid(row=1, column=2, sticky="ew", padx=s.PAD_MD, pady=(0, s.PAD_SM))

        # Buttons
        btn_col = ctk.CTkFrame(filter_card, fg_color="transparent")
        btn_col.grid(row=0, column=3, rowspan=2, sticky="se", padx=s.PAD_MD, pady=s.PAD_SM)

        ctk.CTkButton(btn_col, text="Aplicar", width=90, height=32, font=s.FONT_SM,
                      fg_color=s.COLOR_ACCENT, hover_color=s.COLOR_ACCENT_HOVER,
                      command=self.refresh).grid(row=0, column=0, padx=(0, s.PAD_SM))
        ctk.CTkButton(btn_col, text="Limpiar", width=80, height=32, font=s.FONT_SM,
                      fg_color=s.COLOR_BORDER, hover_color=s.COLOR_CARD_HOVER,
                      command=self._clear_filters).grid(row=0, column=1)

        # Table
        table_card = ctk.CTkFrame(self, fg_color=s.COLOR_CARD, corner_radius=s.CORNER_RADIUS)
        table_card.grid(row=2, column=0, sticky="nsew", padx=s.PAD_LG, pady=(0, s.PAD_MD))
        table_card.grid_columnconfigure(0, weight=1)
        table_card.grid_rowconfigure(1, weight=1)

        # Header
        header = ctk.CTkFrame(table_card, fg_color="#1E2235", corner_radius=0, height=36)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        self._configure_cols(header)
        for col_idx, col_name in enumerate(self._COLUMNS):
            ctk.CTkLabel(
                header, text=col_name, font=(s.FONT_FAMILY, 11, "bold"),
                text_color=s.COLOR_TEXT_MUTED, anchor="w",
            ).grid(row=0, column=col_idx, sticky="ew", padx=(s.PAD_SM, 0))

        # Scrollable rows
        self._rows_frame = ctk.CTkScrollableFrame(
            table_card, fg_color="transparent", label_text=""
        )
        self._rows_frame.grid(row=1, column=0, sticky="nsew")
        self._configure_cols(self._rows_frame)

        # Count label
        self._count_label = ctk.CTkLabel(
            self, text="", font=s.FONT_SM, text_color=s.COLOR_TEXT_MUTED
        )
        self._count_label.grid(row=3, column=0, sticky="e", padx=s.PAD_LG, pady=(0, s.PAD_SM))

    def _configure_cols(self, frame):
        for i, w in enumerate(self._COL_WEIGHTS):
            frame.grid_columnconfigure(i, weight=w)

    def _add_filter(self, parent, col, label, var, placeholder=""):
        ctk.CTkLabel(parent, text=label, font=s.FONT_SM, text_color=s.COLOR_TEXT_MUTED, anchor="w") \
            .grid(row=0, column=col, sticky="w", padx=s.PAD_MD, pady=(s.PAD_SM, 2))
        ctk.CTkEntry(parent, textvariable=var, placeholder_text=placeholder, font=s.FONT_MD, height=32) \
            .grid(row=1, column=col, sticky="ew", padx=s.PAD_MD, pady=(0, s.PAD_SM))

    # ── Public API ────────────────────────────────────────────────────────────

    def refresh(self):
        """Reload and render expenses from the DB with current filters."""
        month = self._month_var.get().strip() or None
        cat = self._cat_var.get()
        category = None if cat in ("", "(todos)") else cat
        pm = self._pm_var.get()
        payment_method = None if pm in ("", "(todos)") else PAYMENT_DISPLAY_TO_METHOD.get(pm, pm)

        self._expenses = fetch_filtered_expenses(
            month=month, category=category, payment_method=payment_method
        )
        self._render_rows()
        self._count_label.configure(text=f"{len(self._expenses)} gasto(s) encontrado(s)")

    def refresh_categories(self):
        """Recarga el dropdown de categorías cuando cambia la lista."""
        names = ["(todos)"] + self._load_categories()
        self._cat_combo.configure(values=names)

    # ── Rendering ─────────────────────────────────────────────────────────────

    def _render_rows(self):
        for w in self._rows_frame.winfo_children():
            w.destroy()

        if not self._expenses:
            ctk.CTkLabel(
                self._rows_frame, text="No se encontraron gastos.",
                font=s.FONT_MD, text_color=s.COLOR_TEXT_MUTED,
            ).grid(row=0, column=0, columnspan=len(self._COLUMNS), pady=s.PAD_LG)
            return

        for idx, expense in enumerate(self._expenses):
            self._build_row(idx, expense)

    def _build_row(self, idx: int, expense: Expense):
        bg = s.COLOR_CARD if idx % 2 == 0 else s.COLOR_BG
        row = ctk.CTkFrame(self._rows_frame, fg_color=bg, corner_radius=0, height=s.TABLE_ROW_HEIGHT)
        row.grid(row=idx, column=0, columnspan=len(self._COLUMNS), sticky="ew")
        row.grid_propagate(False)
        self._configure_cols(row)

        pm_color = s.PAYMENT_COLORS.get(expense.payment_method, s.COLOR_ACCENT)
        pm_label = PAYMENT_LABELS.get(expense.payment_method, expense.payment_method)

        values = [
            date_to_display(expense.date),
            expense.description,
            expense.category,
            None,           # método de pago — se renderiza como badge
            format_clp(expense.amount),
            expense.notes or "—",
        ]

        for col_idx, val in enumerate(values):
            if col_idx == 3:
                # Payment method badge
                badge = ctk.CTkLabel(
                    row, text=pm_label, font=(s.FONT_FAMILY, 10, "bold"),
                    text_color=s.PAYMENT_TEXT_COLOR,
                    fg_color=pm_color, corner_radius=4,
                    padx=6, pady=2,
                )
                badge.grid(row=0, column=col_idx, sticky="w", padx=(s.PAD_SM, 0), pady=4)
            else:
                anchor = "e" if col_idx == 4 else "w"
                ctk.CTkLabel(
                    row, text=str(val), font=s.FONT_SM,
                    text_color=s.COLOR_TEXT, anchor=anchor,
                ).grid(row=0, column=col_idx, sticky="ew", padx=(s.PAD_SM, 0))

        # Action buttons
        action_frame = ctk.CTkFrame(row, fg_color="transparent")
        action_frame.grid(row=0, column=6, sticky="e", padx=(0, s.PAD_SM))

        ctk.CTkButton(
            action_frame, text="Editar", width=55, height=26, font=s.FONT_SM,
            fg_color=s.COLOR_WARNING, hover_color=s.COLOR_WARNING_HOVER,
            command=lambda e=expense: self._edit(e),
        ).grid(row=0, column=0, padx=(0, 4))

        ctk.CTkButton(
            action_frame, text="Eliminar", width=60, height=26, font=s.FONT_SM,
            fg_color=s.COLOR_DANGER, hover_color=s.COLOR_DANGER_HOVER,
            command=lambda e=expense: self._delete(e),
        ).grid(row=0, column=1)

    # ── Actions ───────────────────────────────────────────────────────────────

    def _edit(self, expense: Expense):
        if self._on_edit:
            self._on_edit(expense)

    def _delete(self, expense: Expense):
        dialog = ctk.CTkInputDialog(
            text=f'Escribe "sí" para confirmar la eliminación de:\n"{expense.description}"',
            title="Confirmar Eliminación",
        )
        answer = dialog.get_input()
        if answer and answer.strip().lower() in ("sí", "si"):
            delete_expense(expense.id)
            self.refresh()

    def _clear_filters(self):
        self._month_var.set("")
        self._cat_var.set("")
        self._pm_var.set("")
        self._cat_combo.set("(todos)")
        self._pm_combo.set("(todos)")
        self.refresh()

    def _load_categories(self) -> list[str]:
        try:
            return fetch_category_names()
        except Exception:
            return []
