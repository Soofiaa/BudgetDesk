"""
app.py
Root window and tab orchestration for MonthlyExpenseTracker.
"""
from __future__ import annotations

import customtkinter as ctk

from ui import styles as s
from ui.add_expense_frame import AddExpenseFrame
from ui.expenses_table_frame import ExpensesTableFrame
from ui.summary_frame import SummaryFrame
from ui.categories_frame import CategoriesFrame


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ── Window setup ──────────────────────────────────────────────────────
        ctk.set_appearance_mode(s.CTK_APPEARANCE)
        ctk.set_default_color_theme(s.CTK_THEME)

        self.title(s.APP_TITLE)
        self.geometry(f"{s.APP_START_WIDTH}x{s.APP_START_HEIGHT}")
        self.minsize(s.APP_MIN_WIDTH, s.APP_MIN_HEIGHT)
        self.configure(fg_color=s.COLOR_BG)

        self._build_ui()
        self._bind_events()

    # ── Build ─────────────────────────────────────────────────────────────────

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header bar
        header = ctk.CTkFrame(self, fg_color=s.COLOR_CARD, corner_radius=0, height=52)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="💰  BudgetDesk — Gastos Mensuales",
            font=s.FONT_LG,
            text_color=s.COLOR_TEXT,
            anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=s.PAD_LG)

        # Tab view
        self._tabs = ctk.CTkTabview(
            self,
            fg_color=s.COLOR_BG,
            segmented_button_fg_color=s.COLOR_CARD,
            segmented_button_selected_color=s.COLOR_ACCENT,
            segmented_button_selected_hover_color=s.COLOR_ACCENT_HOVER,
            segmented_button_unselected_color=s.COLOR_CARD,
            segmented_button_unselected_hover_color=s.COLOR_CARD_HOVER,
            text_color=s.COLOR_TEXT,
        )
        self._tabs.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

        for tab_name in ("Gastos", "Agregar / Editar", "Resumen", "Categorías"):
            self._tabs.add(tab_name)
            self._tabs.tab(tab_name).grid_columnconfigure(0, weight=1)
            self._tabs.tab(tab_name).grid_rowconfigure(0, weight=1)

        # ── Instantiate frames ────────────────────────────────────────────────
        self._add_frame = AddExpenseFrame(
            self._tabs.tab("Agregar / Editar"),
            on_saved_callback=self._on_expense_saved,
        )
        self._add_frame.grid(row=0, column=0, sticky="nsew")

        self._table_frame = ExpensesTableFrame(
            self._tabs.tab("Gastos"),
            on_edit_callback=self._on_edit_requested,
        )
        self._table_frame.grid(row=0, column=0, sticky="nsew")

        self._summary_frame = SummaryFrame(self._tabs.tab("Resumen"))
        self._summary_frame.grid(row=0, column=0, sticky="nsew")

        self._categories_frame = CategoriesFrame(
            self._tabs.tab("Categorías"),
            on_change_callback=self._on_categories_changed,
        )
        self._categories_frame.grid(row=0, column=0, sticky="nsew")

    def _bind_events(self):
        """No se necesitan eventos virtuales: se usa callback directo."""
        pass

    # ── Callbacks ─────────────────────────────────────────────────────────────

    def _on_expense_saved(self):
        """Llamado al guardar o actualizar un gasto."""
        self._table_frame.refresh()
        self._summary_frame.refresh()
        self._tabs.set("Gastos")

    def _on_edit_requested(self, expense):
        """Navega al formulario y precarga los datos del gasto."""
        self._add_frame.load_expense(expense)
        self._tabs.set("Agregar / Editar")

    def _on_categories_changed(self, _event=None):
        """Propagate category list changes to both the form and the table filter."""
        self._add_frame.refresh_categories()
        self._table_frame.refresh_categories()
