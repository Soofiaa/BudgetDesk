"""
categories_frame.py
Tab for managing user-defined categories.
"""
from __future__ import annotations

import tkinter as tk
import customtkinter as ctk

from database import (
    fetch_all_categories,
    insert_category,
    delete_category,
    count_expenses_by_category,
    reassign_expenses_category,
)
from ui import styles as s


class CategoriesFrame(ctk.CTkFrame):
    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, fg_color=s.COLOR_BG, **kwargs)
        self._on_change = on_change_callback
        self._build_ui()
        self.refresh()

    # ── Build ─────────────────────────────────────────────────────────────────

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Title
        ctk.CTkLabel(
            self,
            text="Gestionar Categorías",
            font=s.FONT_XL,
            text_color=s.COLOR_TEXT,
        ).grid(row=0, column=0, sticky="w", padx=s.PAD_LG, pady=(s.PAD_LG, s.PAD_SM))

        # Content card
        card = ctk.CTkFrame(self, fg_color=s.COLOR_CARD, corner_radius=s.CORNER_RADIUS)
        card.grid(row=1, column=0, sticky="nsew", padx=s.PAD_LG, pady=s.PAD_MD)
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(1, weight=1)

        # Add-category row
        add_row = ctk.CTkFrame(card, fg_color="transparent")
        add_row.grid(row=0, column=0, sticky="ew", padx=s.PAD_MD, pady=s.PAD_MD)
        add_row.grid_columnconfigure(0, weight=1)

        self._new_name_var = tk.StringVar()
        self._entry = ctk.CTkEntry(
            add_row,
            textvariable=self._new_name_var,
            placeholder_text="Nombre de la nueva categoría…",
            font=s.FONT_MD,
            height=38,
        )
        self._entry.grid(row=0, column=0, sticky="ew", padx=(0, s.PAD_SM))
        self._entry.bind("<Return>", lambda _: self._add_category())

        ctk.CTkButton(
            add_row,
            text="+ Agregar Categoría",
            command=self._add_category,
            font=s.FONT_MD,
            fg_color=s.COLOR_ACCENT,
            hover_color=s.COLOR_ACCENT_HOVER,
            height=38,
            width=180,
        ).grid(row=0, column=1)

        # Error label
        self._error_label = ctk.CTkLabel(
            card,
            text="",
            font=s.FONT_SM,
            text_color=s.COLOR_DANGER,
        )
        self._error_label.grid(row=1, column=0, sticky="w", padx=s.PAD_MD)

        # Scrollable list
        self._list_frame = ctk.CTkScrollableFrame(
            card,
            fg_color="transparent",
            label_text="",
        )
        self._list_frame.grid(row=2, column=0, sticky="nsew", padx=s.PAD_MD, pady=(0, s.PAD_MD))
        card.grid_rowconfigure(2, weight=1)
        self._list_frame.grid_columnconfigure(0, weight=1)

    # ── Data ──────────────────────────────────────────────────────────────────

    def refresh(self):
        """Reload categories from the database and rebuild the list."""
        for widget in self._list_frame.winfo_children():
            widget.destroy()

        categories = fetch_all_categories()
        if not categories:
            ctk.CTkLabel(
                self._list_frame,
                text="No hay categorías. Agrega una arriba.",
                font=s.FONT_MD,
                text_color=s.COLOR_TEXT_MUTED,
            ).grid(row=0, column=0, pady=s.PAD_LG)
            return

        for idx, cat in enumerate(categories):
            self._build_category_row(idx, cat)

    def _build_category_row(self, row_idx: int, cat):
        bg = s.COLOR_CARD if row_idx % 2 == 0 else s.COLOR_BG
        row = ctk.CTkFrame(self._list_frame, fg_color=bg, corner_radius=6, height=40)
        row.grid(row=row_idx, column=0, sticky="ew", pady=2)
        row.grid_columnconfigure(0, weight=1)
        row.grid_propagate(False)

        ctk.CTkLabel(
            row,
            text=cat.name,
            font=s.FONT_MD,
            text_color=s.COLOR_TEXT,
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=s.PAD_MD)

        ctk.CTkButton(
            row,
            text="Eliminar",
            width=80,
            height=28,
            font=s.FONT_SM,
            fg_color=s.COLOR_DANGER,
            hover_color=s.COLOR_DANGER_HOVER,
            command=lambda c=cat: self._delete_category(c),
        ).grid(row=0, column=1, padx=(0, s.PAD_SM), pady=4)

    # ── Actions ───────────────────────────────────────────────────────────────

    def _add_category(self):
        name = self._new_name_var.get().strip()
        try:
            insert_category(name)
            self._new_name_var.set("")
            self._error_label.configure(text="")
            self.refresh()
            if self._on_change:
                self._on_change()
        except ValueError as exc:
            self._error_label.configure(text=str(exc))

    def _delete_category(self, cat):
        count = count_expenses_by_category(cat.name)

        if count == 0:
            dialog = ctk.CTkInputDialog(
                text=f'Escribe "sí" para confirmar la eliminación de la categoría:\n"{cat.name}"',
                title="Confirmar Eliminación",
            )
            answer = dialog.get_input()
            if answer and answer.strip().lower() in ("sí", "si"):
                delete_category(cat.id)
                self._finish_change()
            return

        other_names = [c.name for c in fetch_all_categories() if c.id != cat.id]
        if not other_names:
            self._show_no_alternative_dialog(cat, count)
        else:
            self._show_reassign_dialog(cat, count, other_names)

    def _finish_change(self):
        self.refresh()
        if self._on_change:
            self._on_change()

    def _show_reassign_dialog(self, cat, count, other_names):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Reasignar Gastos")
        dialog.geometry("420x220")
        dialog.transient(self)
        dialog.grab_set()
        dialog.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            dialog,
            text=(
                f'{count} gasto(s) usan la categoría "{cat.name}".\n'
                "Elige a qué categoría reasignarlos, o cancela."
            ),
            font=s.FONT_MD,
            text_color=s.COLOR_TEXT,
            wraplength=380,
            justify="left",
        ).grid(row=0, column=0, sticky="w", padx=s.PAD_MD, pady=(s.PAD_MD, s.PAD_SM))

        target_var = tk.StringVar(value=other_names[0])
        ctk.CTkComboBox(
            dialog,
            variable=target_var,
            values=other_names,
            state="readonly",
            font=s.FONT_MD,
        ).grid(row=1, column=0, sticky="ew", padx=s.PAD_MD, pady=(0, s.PAD_MD))

        btn_row = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_row.grid(row=2, column=0, sticky="e", padx=s.PAD_MD, pady=(0, s.PAD_MD))

        def _confirm():
            reassign_expenses_category(cat.name, target_var.get())
            delete_category(cat.id)
            dialog.destroy()
            self._finish_change()

        ctk.CTkButton(
            btn_row, text="Cancelar", width=100, font=s.FONT_MD,
            fg_color=s.COLOR_BORDER, hover_color=s.COLOR_CARD_HOVER,
            command=dialog.destroy,
        ).grid(row=0, column=0, padx=(0, s.PAD_SM))

        ctk.CTkButton(
            btn_row, text="Reasignar y Eliminar", width=170, font=s.FONT_MD,
            fg_color=s.COLOR_DANGER, hover_color=s.COLOR_DANGER_HOVER,
            command=_confirm,
        ).grid(row=0, column=1)

    def _show_no_alternative_dialog(self, cat, count):
        dialog = ctk.CTkToplevel(self)
        dialog.title("No se puede eliminar")
        dialog.geometry("380x180")
        dialog.transient(self)
        dialog.grab_set()
        dialog.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            dialog,
            text=(
                f'No se puede eliminar "{cat.name}": {count} gasto(s) la usan '
                "y es la única categoría disponible para reasignarlos.\n\n"
                "Crea otra categoría primero."
            ),
            font=s.FONT_MD,
            text_color=s.COLOR_TEXT,
            wraplength=340,
            justify="left",
        ).grid(row=0, column=0, sticky="w", padx=s.PAD_MD, pady=s.PAD_MD)

        ctk.CTkButton(
            dialog, text="Entendido", font=s.FONT_MD,
            fg_color=s.COLOR_ACCENT, hover_color=s.COLOR_ACCENT_HOVER,
            command=dialog.destroy,
        ).grid(row=1, column=0, pady=(0, s.PAD_MD))
