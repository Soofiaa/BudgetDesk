"""
add_expense_frame.py
Form to create or edit an expense.
"""
from __future__ import annotations

import tkinter as tk
from datetime import date as dt_date
import customtkinter as ctk

from database import insert_expense, update_expense, fetch_category_names
from models.expense import Expense
from services import validate_expense, PAYMENT_METHODS, PAYMENT_DISPLAY_NAMES, PAYMENT_DISPLAY_TO_METHOD, PAYMENT_METHOD_TO_DISPLAY
from utils import date_to_display, date_to_db
from ui import styles as s


class AddExpenseFrame(ctk.CTkFrame):
    def __init__(self, master, on_saved_callback=None, **kwargs):
        super().__init__(master, fg_color=s.COLOR_BG, **kwargs)
        self._on_saved = on_saved_callback
        self._editing_expense: Expense | None = None
        self._build_ui()

    # ── Build ─────────────────────────────────────────────────────────────────

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)

        # Title
        self._title_label = ctk.CTkLabel(
            self, text="Agregar Gasto", font=s.FONT_XL, text_color=s.COLOR_TEXT
        )
        self._title_label.grid(row=0, column=0, sticky="w", padx=s.PAD_LG, pady=(s.PAD_LG, s.PAD_SM))

        # Card
        card = ctk.CTkFrame(self, fg_color=s.COLOR_CARD, corner_radius=s.CORNER_RADIUS)
        card.grid(row=1, column=0, sticky="nsew", padx=s.PAD_LG, pady=s.PAD_MD)
        card.grid_columnconfigure((0, 1), weight=1)

        # ── Row 0: Amount + Date ──────────────────────────────────────────────
        self._amount_var = tk.StringVar()
        self._date_var = tk.StringVar(value=dt_date.today().strftime("%d/%m/%Y"))

        self._add_field(card, row=0, col=0, label="Monto (CLP) *", var=self._amount_var, placeholder="ej. 5000")
        self._add_field(card, row=0, col=1, label="Fecha *", var=self._date_var, placeholder="DD/MM/AAAA")

        # ── Row 1: Description ────────────────────────────────────────────────
        self._desc_var = tk.StringVar()
        desc_label = ctk.CTkLabel(card, text="Descripción *", font=s.FONT_SM, text_color=s.COLOR_TEXT_MUTED, anchor="w")
        desc_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=s.PAD_MD, pady=(s.PAD_SM, 2))
        ctk.CTkEntry(card, textvariable=self._desc_var, placeholder_text="¿En qué gastaste?", font=s.FONT_MD, height=38) \
            .grid(row=3, column=0, columnspan=2, sticky="ew", padx=s.PAD_MD, pady=(0, s.PAD_SM))

        # ── Row 2: Category + Payment Method ─────────────────────────────────
        # Categoría
        ctk.CTkLabel(card, text="Categoría *", font=s.FONT_SM, text_color=s.COLOR_TEXT_MUTED, anchor="w") \
            .grid(row=4, column=0, sticky="w", padx=s.PAD_MD, pady=(s.PAD_SM, 2))
        self._category_var = tk.StringVar()
        self._category_combo = ctk.CTkComboBox(
            card,
            variable=self._category_var,
            values=self._load_categories(),
            font=s.FONT_MD,
            height=38,
            state="readonly",
        )
        self._category_combo.grid(row=5, column=0, sticky="ew", padx=s.PAD_MD, pady=(0, s.PAD_SM))

        # Método de pago
        ctk.CTkLabel(card, text="Método de Pago *", font=s.FONT_SM, text_color=s.COLOR_TEXT_MUTED, anchor="w") \
            .grid(row=4, column=1, sticky="w", padx=s.PAD_MD, pady=(s.PAD_SM, 2))
        self._payment_var = tk.StringVar(value=PAYMENT_DISPLAY_NAMES[0])
        ctk.CTkComboBox(
            card,
            variable=self._payment_var,
            values=PAYMENT_DISPLAY_NAMES,
            font=s.FONT_MD,
            height=38,
            state="readonly",
        ).grid(row=5, column=1, sticky="ew", padx=s.PAD_MD, pady=(0, s.PAD_SM))

        # ── Row 3: Notes ──────────────────────────────────────────────────────
        ctk.CTkLabel(card, text="Notas (opcional)", font=s.FONT_SM, text_color=s.COLOR_TEXT_MUTED, anchor="w") \
            .grid(row=6, column=0, columnspan=2, sticky="w", padx=s.PAD_MD, pady=(s.PAD_SM, 2))
        self._notes_text = ctk.CTkTextbox(card, height=70, font=s.FONT_MD)
        self._notes_text.grid(row=7, column=0, columnspan=2, sticky="ew", padx=s.PAD_MD, pady=(0, s.PAD_MD))

        # ── Error label ───────────────────────────────────────────────────────
        self._error_label = ctk.CTkLabel(card, text="", font=s.FONT_SM, text_color=s.COLOR_DANGER)
        self._error_label.grid(row=8, column=0, columnspan=2, sticky="w", padx=s.PAD_MD)

        # ── Buttons ───────────────────────────────────────────────────────────
        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.grid(row=9, column=0, columnspan=2, sticky="e", padx=s.PAD_MD, pady=s.PAD_MD)

        self._cancel_btn = ctk.CTkButton(
            btn_row, text="Cancelar", width=110, height=38, font=s.FONT_MD,
            fg_color=s.COLOR_BORDER, hover_color=s.COLOR_CARD_HOVER,
            command=self.reset,
        )
        self._cancel_btn.grid(row=0, column=0, padx=(0, s.PAD_SM))
        self._cancel_btn.grid_remove()

        self._save_btn = ctk.CTkButton(
            btn_row, text="Guardar Gasto", width=140, height=38, font=s.FONT_MD,
            fg_color=s.COLOR_ACCENT, hover_color=s.COLOR_ACCENT_HOVER,
            command=self._save,
        )
        self._save_btn.grid(row=0, column=1)

    def _add_field(self, parent, row, col, label, var, placeholder=""):
        ctk.CTkLabel(parent, text=label, font=s.FONT_SM, text_color=s.COLOR_TEXT_MUTED, anchor="w") \
            .grid(row=row * 2, column=col, sticky="w", padx=s.PAD_MD, pady=(s.PAD_SM, 2))
        ctk.CTkEntry(parent, textvariable=var, placeholder_text=placeholder, font=s.FONT_MD, height=38) \
            .grid(row=row * 2 + 1, column=col, sticky="ew", padx=s.PAD_MD, pady=(0, s.PAD_SM))

    # ── Public API ────────────────────────────────────────────────────────────

    def load_expense(self, expense: Expense):
        """Precarga el formulario para editar un gasto existente."""
        self._editing_expense = expense
        self._title_label.configure(text="Editar Gasto")
        self._save_btn.configure(text="Actualizar Gasto")
        self._cancel_btn.grid()

        self._amount_var.set(str(int(expense.amount)))
        self._date_var.set(date_to_display(expense.date))
        self._desc_var.set(expense.description)
        self._category_var.set(expense.category)
        self._payment_var.set(PAYMENT_METHOD_TO_DISPLAY.get(expense.payment_method, expense.payment_method))
        self._notes_text.delete("1.0", "end")
        self._notes_text.insert("1.0", expense.notes or "")

    def reset(self):
        """Limpia el formulario y vuelve al modo de alta."""
        self._editing_expense = None
        self._title_label.configure(text="Agregar Gasto")
        self._save_btn.configure(text="Guardar Gasto")
        self._cancel_btn.grid_remove()

        self._amount_var.set("")
        self._date_var.set(dt_date.today().strftime("%d/%m/%Y"))
        self._desc_var.set("")
        self._category_var.set("")
        self._payment_var.set(PAYMENT_DISPLAY_NAMES[0])
        self._notes_text.delete("1.0", "end")
        self._error_label.configure(text="")

    def refresh_categories(self):
        """Reload category list from the database (called when categories change)."""
        names = self._load_categories()
        self._category_combo.configure(values=names)

    # ── Internals ─────────────────────────────────────────────────────────────

    def _load_categories(self) -> list[str]:
        try:
            return fetch_category_names()
        except Exception:
            return []

    def _save(self):
        self._error_label.configure(text="")
        amount_str = self._amount_var.get()
        description = self._desc_var.get().strip()
        date = self._date_var.get().strip()
        category = self._category_var.get().strip()
        # Convertir valores del formulario a formato interno
        payment = PAYMENT_DISPLAY_TO_METHOD.get(self._payment_var.get().strip(), self._payment_var.get().strip())
        date_display = self._date_var.get().strip()
        notes = self._notes_text.get("1.0", "end").strip()

        ok, msg = validate_expense(amount_str, description, date_display, category, payment)
        if not ok:
            self._error_label.configure(text=msg)
            return

        expense = Expense(
            id=self._editing_expense.id if self._editing_expense else None,
            amount=float(amount_str.replace(".", "").replace(",", ".")),
            description=description,
            date=date_to_db(date_display),
            category=category,
            payment_method=payment,
            notes=notes,
        )

        if self._editing_expense:
            update_expense(expense)
        else:
            insert_expense(expense)

        self.reset()
        if self._on_saved:
            self._on_saved()
