#!/usr/bin/env python3
"""
Budget Tracker
Track monthly budgets by category and provide spending alerts.
"""

import csv
import json
from datetime import datetime
from pathlib import Path
import pandas as pd
from typing import Dict, Optional

class BudgetTracker:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.expenses_file = self.base_dir / "expenses" / "expenses_working.csv"
        self.initial_budget_file = self.base_dir / "budget" / "initial_budget.json"
        self.summary_dir = self.base_dir / "summary"
        # Load fixed charges and use as category structure
        self.charges_fixes = self._load_initial_budget()
        self.categories = list(self.charges_fixes.keys())
        self.subcategories = {cat: list(sub.keys()) for cat, sub in self.charges_fixes.items()}
    
    def _load_initial_budget(self):
        """Load fixed charges and category structure from JSON file."""
        if self.initial_budget_file.exists():
            try:
                with open(self.initial_budget_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        else:
            return {}
        
    def get_expenses_by_category(self, 
                            account: Optional[str] = None, 
                            month: Optional[str] = None) -> Dict[str, Dict[str, float]]:
        """Gather all expenses grouped by category and subcategory."""
        if not self.expenses_file.exists():
            return {}
        df = pd.read_csv(self.expenses_file)
        if df.empty:
            return {}
        if month:
            df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
            df['Month'] = df['Date'].dt.to_period('M').astype(str)
            df = df[df['Month'] == month]
        if account:
            df = df[df['Compte'] == account]
        summary = {cat: {subcat: 0.0 for subcat in self.subcategories[cat]} for cat in self.categories}
        for _, row in df.iterrows():
            cat = row['Categorie']
            subcat = row['Sous-categorie'] if 'Sous-categorie' in row else None
            montant = row['Montant']
            if cat in summary:
                if subcat and subcat in summary[cat]:
                    summary[cat][subcat] += montant
                elif subcat is None:
                    # If no subcategory, sum to a generic 'Autre' if exists
                    if 'autre' in summary[cat]:
                        summary[cat]['autre'] += montant
        return summary
        
    def save_expenses_summary(self, 
                        account: Optional[str] = None, 
                        month: Optional[str] = None):
        """Save summary of expenses grouped by category and subcategory."""
        current_month = datetime.now().strftime("%Y-%m") if month is None else month
        summary = self.get_expenses_by_category(account, current_month)

        # Save summary to file
        self.summary_dir.mkdir(exist_ok=True)
        filename = f"summary_{account or 'all'}_{current_month}.json"
        summary_path = self.summary_dir / filename
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        print(f"\n📁 Summary saved to {summary_path}")

def main():
    tracker = BudgetTracker()
    
    while True:
        print("\n" + "="*40)
        print("EXPENSES TRACKER")
        print("="*40)
        print("1. 📊 Global expenses summary")
        print("2. 🔍 Specific account summary")
        print("3. 🚪 Exit")
        print("="*40)
        choice = input("\nSelect option (1-3): ").strip()
        if choice == '1':
            # Validate month input:
            month = input("Enter month (YYYY-MM) or leave empty for current month: ").strip()
            if not month:
                month = None
            else:
                try:
                    datetime.strptime(month, "%Y-%m")
                except ValueError:
                    print("❌ Invalid format. Defaulting to current month.")
                    month = None
            tracker.save_expenses_summary(month=month)
        elif choice == '2':
            # Validate month input:
            month = input("Enter month (YYYY-MM) or leave empty for current month: ").strip()
            if not month:
                month = None
            else:
                try:
                    datetime.strptime(month, "%Y-%m")
                except ValueError:
                    print("❌ Invalid format. Defaulting to current month.")
                    month = None
            account = input("Enter account ([Commun]/Luc/Laura): ").strip()
            tracker.save_expenses_summary(account=account, month=month)
        elif choice == '3':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select a valid option (1-3).")
        
        try:    
            input("\nPress Enter to continue...")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()