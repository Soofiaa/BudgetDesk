"""
main.py
Entry point for MonthlyExpenseTracker.
"""
import sys
from pathlib import Path

# Make sure the project root is on sys.path when launched directly
sys.path.insert(0, str(Path(__file__).parent))

from database import initialize_db
from ui.app import App


def main() -> None:
    initialize_db()
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
