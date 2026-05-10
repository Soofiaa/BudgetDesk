"""
styles.py
Central design tokens for the MonthlyExpenseTracker UI.
"""

# ── CustomTkinter appearance ──────────────────────────────────────────────────
CTK_APPEARANCE = "dark"
CTK_THEME = "blue"

# ── Window ────────────────────────────────────────────────────────────────────
APP_TITLE = "BudgetDesk — Gastos Mensuales"
APP_MIN_WIDTH = 1100
APP_MIN_HEIGHT = 680
APP_START_WIDTH = 1200
APP_START_HEIGHT = 740

# ── Colors ────────────────────────────────────────────────────────────────────
COLOR_BG = "#1A1D2E"          # Main background
COLOR_CARD = "#242738"        # Card / panel background
COLOR_CARD_HOVER = "#2C3050"
COLOR_ACCENT = "#5B8DEF"      # Primary accent (blue)
COLOR_ACCENT_HOVER = "#4070D4"
COLOR_SUCCESS = "#3DBC78"     # Green — totals, positive
COLOR_DANGER = "#E05252"      # Red — delete, errors
COLOR_DANGER_HOVER = "#C43C3C"
COLOR_WARNING = "#F0A050"     # Orange — edit
COLOR_WARNING_HOVER = "#D48830"
COLOR_TEXT = "#E8ECF4"        # Primary text
COLOR_TEXT_MUTED = "#9099B2"  # Secondary / label text
COLOR_BORDER = "#333654"      # Subtle border

# ── Payment method badge colors ───────────────────────────────────────────────
PAYMENT_COLORS = {
    "debit": "#3DBC78",
    "bank_transfer": "#5B8DEF",
    "credit_card": "#B06EF5",
}
PAYMENT_TEXT_COLOR = "#FFFFFF"

# ── Fonts ─────────────────────────────────────────────────────────────────────
FONT_FAMILY = "Segoe UI"
FONT_SM = (FONT_FAMILY, 11)
FONT_MD = (FONT_FAMILY, 13)
FONT_LG = (FONT_FAMILY, 16, "bold")
FONT_XL = (FONT_FAMILY, 22, "bold")
FONT_MONO = ("Consolas", 11)

# ── Padding / spacing ─────────────────────────────────────────────────────────
PAD_SM = 6
PAD_MD = 12
PAD_LG = 20
CORNER_RADIUS = 10

# ── Table row height ──────────────────────────────────────────────────────────
TABLE_ROW_HEIGHT = 36
