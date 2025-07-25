#!/usr/bin/env python3
"""
Enhanced Expense Tracker
A comprehensive tool for tracking personal and shared expenses with improved features.
"""

import csv
import os
import sys
from datetime import datetime, date
from pathlib import Path
import pandas as pd
from typing import Dict, List, Optional, Tuple

class ExpenseTracker:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.expenses_file = self.base_dir / "Expenses" / "expenses_working.csv"
        self.fixed_charges_file = self.base_dir / "budget/charges_fixes.csv"
        self.income_file = self.base_dir / "budget/income.csv"
        self.summary_dir = self.base_dir / "Summary"
        self.history_dir = self.base_dir / "History"
        
        # Ensure directories exist
        self.expenses_file.parent.mkdir(exist_ok=True)
        self.summary_dir.mkdir(exist_ok=True)
        self.history_dir.mkdir(exist_ok=True)
        
        # Categories with emojis for better UX
        self.categories = {
            '🏠': 'Maison',
            '🚗': 'Transport', 
            '🏥': 'Santé',
            '🍽️': 'Restaurant',
            '🛒': 'Courses',
            '💆': 'Bien-être',
            '🎭': 'Culture',
            '🏃': 'Sport',
            '🛍️': 'Shopping',
            '🌭': 'Saucisse',
            '💵': 'Liquide',
            '💰': 'Economie',
            '🎁': 'Cadeau',
            '📦': 'Autre'
        }
        
        # Accounts
        self.accounts = ['Commun', 'Luc', 'Laura']
        
        # Initialize files if they don't exist
        self._initialize_files()
    
    def _initialize_files(self):
        """Initialize CSV files with headers if they don't exist."""
        headers = ['Date', 'Compte', 'Categorie', 'Description', 'Montant']
        
        if not self.expenses_file.exists():
            with open(self.expenses_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
        
        if not self.fixed_charges_file.exists():
            with open(self.fixed_charges_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
        
        if not self.income_file.exists():
            with open(self.income_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
    
    def _validate_date(self, date_str: str) -> bool:
        """Validate date format dd/mm/yyyy."""
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return True
        except ValueError:
            return False
    
    def _validate_amount(self, amount_str: str) -> Optional[float]:
        """Validate and convert amount to float."""
        try:
            amount = float(amount_str.replace(',', '.'))
            return amount if amount >= 0 else None
        except ValueError:
            return None
    
    def _get_user_input(self, prompt: str, default: str = "", validator=None) -> str:
        """Get user input with validation."""
        while True:
            user_input = input(f"{prompt} [{default}]: ").strip()
            if not user_input and default:
                return default
            if validator is None or validator(user_input):
                return user_input
            print("❌ Invalid input. Please try again.")
    
    def add_expense(self):
        """Add a new expense entry with improved UX."""
        print("\n" + "="*50)
        print("💰 ADD NEW EXPENSE")
        print("="*50)
        
        # Date input
        default_date = datetime.now().strftime("%d/%m/%Y")
        date_input = self._get_user_input(
            "Enter the date (dd/mm/yyyy)",
            default_date,
            self._validate_date
        )
        
        # Account selection
        print(f"\n📋 Select account:")
        for i, account in enumerate(self.accounts, 1):
            print(f"  {i}. {account}")
        
        while True:
            try:
                account_choice = int(input(f"Enter account number (1-{len(self.accounts)}): "))
                if 1 <= account_choice <= len(self.accounts):
                    account = self.accounts[account_choice - 1]
                    break
                else:
                    print("❌ Invalid choice. Please select a valid number.")
            except ValueError:
                print("❌ Please enter a number.")
        
        # Category selection
        print(f"\n📂 Select category:")
        category_items = list(self.categories.items())
        for i, (emoji, category) in enumerate(category_items, 1):
            print(f"  {i}. {emoji} {category}")
        
        while True:
            try:
                cat_choice = int(input(f"Enter category number (1-{len(category_items)}): "))
                if 1 <= cat_choice <= len(category_items):
                    category = category_items[cat_choice - 1][1]
                    break
                else:
                    print("❌ Invalid choice. Please select a valid number.")
            except ValueError:
                print("❌ Please enter a number.")
        
        # Description
        description = self._get_user_input("Enter description").replace(',', ' ').strip()
        if not description:
            description = "No description"
        
        # Amount
        while True:
            amount_str = input("Enter amount (€): ").strip()
            amount = self._validate_amount(amount_str)
            if amount is not None:
                break
            print("❌ Invalid amount. Please enter a positive number.")
        
        # Save to file
        with open(self.expenses_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([date_input, account, category, description, f"{amount:.2f}"])
        
        print(f"\n✅ Expense added successfully!")
        print(f"   📅 Date: {date_input}")
        print(f"   👤 Account: {account}")
        print(f"   📂 Category: {category}")
        print(f"   📝 Description: {description}")
        print(f"   💰 Amount: €{amount:.2f}")
    
    def view_recent_expenses(self, limit: int = 10):
        """View recent expenses."""
        if not self.expenses_file.exists():
            print("❌ No expenses found.")
            return
        
        df = pd.read_csv(self.expenses_file)
        if df.empty:
            print("❌ No expenses found.")
            return
        
        print(f"\n📊 RECENT EXPENSES (Last {limit})")
        print("="*60)
        
        # Convert date and sort
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
        df = df.sort_values('Date', ascending=False).head(limit)
        
        for _, row in df.iterrows():
            date_str = pd.to_datetime(row['Date']).strftime("%d/%m/%Y")
            print(f"{date_str} | {row['Compte']:8} | {row['Categorie']:12} | {row['Description']:20} | €{row['Montant']:8.2f}")
    
    def monthly_summary(self):
        """Generate monthly summary with improved formatting."""
        if not self.expenses_file.exists():
            print("❌ No expenses found.")
            return
        
        df = pd.read_csv(self.expenses_file)
        if df.empty:
            print("❌ No expenses found.")
            return
        
        # Convert date and extract month
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
        df['Month'] = df['Date'].dt.to_period('M').astype(str)
        
        current_month = datetime.now().strftime("%Y-%m")
        
        print(f"\n📈 MONTHLY SUMMARY - {current_month}")
        print("="*60)
        
        # Summary by account
        for account in self.accounts:
            account_df = df[df['Compte'] == account]
            if not account_df.empty:
                total = account_df['Montant'].sum()
                print(f"\n👤 {account}: €{total:.2f}")
                
                # By category
                category_summary = account_df.groupby('Categorie')['Montant'].sum().to_frame().sort_values('Montant', ascending=False)
                for category, amount in category_summary['Montant']:
                    percentage = (amount / total) * 100
                    print(f"   📂 {category}: €{amount:.2f} ({percentage:.1f}%)")
        
        # Overall summary
        total_expenses = df['Montant'].sum()
        print(f"\n💰 TOTAL EXPENSES: €{total_expenses:.2f}")
        
        # Save summary to file
        self._save_monthly_summary(df, current_month)
    
    def _save_monthly_summary(self, df: pd.DataFrame, month: str):
        """Save monthly summary to CSV files."""
        month_name = datetime.strptime(month + "-01", "%Y-%m-%d").strftime("%B_%Y")
        
        for account in self.accounts:
            account_df = df[df['Compte'] == account]
            if not account_df.empty:
                monthly_summary = account_df.groupby(['Month', 'Categorie'])['Montant'].sum().reset_index()
                filename = f"{month_name}_summary_{account.lower()}.csv"
                filepath = self.summary_dir / filename
                monthly_summary.to_csv(filepath, index=False)
                print(f"💾 Summary saved: {filename}")
    
    def archive_month(self):
        """Archive current month's expenses."""
        if not self.expenses_file.exists():
            print("❌ No expenses to archive.")
            return
        
        current_month = datetime.now().strftime("%B_%Y")
        archive_file = self.history_dir / f"{current_month}_expenses.csv"
        
        # Copy current expenses to archive
        import shutil
        shutil.copy2(self.expenses_file, archive_file)
        
        # Clear current expenses file (keep header)
        with open(self.expenses_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Date', 'Compte', 'Categorie', 'Description', 'Montant'])
        
        print(f"✅ Month archived: {archive_file}")
        print("📁 Current expenses file cleared for new month.")
    
    def show_menu(self):
        """Display main menu."""
        print("\n" + "="*50)
        print("💰 EXPENSE TRACKER")
        print("="*50)
        print("1. ➕ Add new expense")
        print("2. 📊 View recent expenses")
        print("3. 📈 Monthly summary")
        print("4. 📁 Archive month")
        print("5. 🚪 Exit")
        print("="*50)

def main():
    tracker = ExpenseTracker()
    
    while True:
        tracker.show_menu()
        choice = input("\nSelect an option (1-5): ").strip()
        
        if choice == '1':
            tracker.add_expense()
        elif choice == '2':
            tracker.view_recent_expenses()
        elif choice == '3':
            tracker.monthly_summary()
        elif choice == '4':
            tracker.archive_month()
        elif choice == '5':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select 1-5.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main() 