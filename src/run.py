#!/usr/bin/env python3
"""
Expense Tracker Launcher
Main entry point for all expense tracking tools.
"""

import sys
import subprocess
from pathlib import Path

def main():
    print("💰 ENHANCED EXPENSE TRACKER")
    print("="*40)
    print("1. 💰 Main Expense Tracker")
    print("2. 🎯 Budget Manager")
    print("3. 📊 Data Analyzer")
    print("4. ➕ Quick Add Expense (Legacy)")
    print("5. 📈 Monthly Summary (Legacy)")
    print("6. 📁 Archive Month (Legacy)")
    print("7. 🚪 Exit")
    print("="*40)
    
    choice = input("\nSelect a tool (1-7): ").strip()
    
    scripts = {
        '1': 'src/expense_tracker.py',
        '2': 'src/budget_tracker.py',
        '3': 'src/data_analyzer.py',
        '4': 'src/add_new_expense.py',
        '5': 'src/monthly_expenses_monitor.py',
        '6': 'src/end_of_month_archive.py'
    }
    
    if choice in scripts:
        script_path = Path(__file__).parent / scripts[choice]
        if script_path.exists():
            print(f"\n🚀 Launching {scripts[choice]}...")
            subprocess.run([sys.executable, str(script_path)])
        else:
            print(f"❌ Script not found: {scripts[choice]}")
    elif choice == '7':
        print("👋 Goodbye!")
        return
    else:
        print("❌ Invalid choice. Please select 1-7.")
    
    input("\nPress Enter to return to main menu...")
    main()  # Restart the menu

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("Press Enter to exit...") 