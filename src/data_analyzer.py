#!/usr/bin/env python3
"""
Data Analyzer
Analyze expense data and provide insights and trends.
"""

import csv
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import seaborn as sns

class DataAnalyzer:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.expenses_file = self.base_dir / "Expenses" / "expenses_working.txt"
        self.fixed_charges_file = self.base_dir / "fixed_charges.csv"
        self.income_file = self.base_dir / "income.csv"
        self.history_dir = self.base_dir / "History"
        
        # Set up plotting style
        plt.style.use('default')
        sns.set_palette("husl")
    
    def load_all_data(self) -> pd.DataFrame:
        """Load and combine all expense data."""
        all_data = []
        
        # Load current expenses
        if self.expenses_file.exists():
            df = pd.read_csv(self.expenses_file)
            if not df.empty:
                all_data.append(df)
        
        # Load fixed charges
        if self.fixed_charges_file.exists():
            df = pd.read_csv(self.fixed_charges_file)
            if not df.empty:
                all_data.append(df)
        
        # Load historical data
        if self.history_dir.exists():
            for file in self.history_dir.glob("*.csv"):
                df = pd.read_csv(file)
                if not df.empty:
                    all_data.append(df)
        
        if not all_data:
            return pd.DataFrame()
        
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df['Date'] = pd.to_datetime(combined_df['Date'], dayfirst=True)
        return combined_df
    
    def spending_trends(self, months: int = 6):
        """Analyze spending trends over time."""
        df = self.load_all_data()
        if df.empty:
            print("❌ No data available for analysis.")
            return
        
        # Filter to last N months
        cutoff_date = datetime.now() - timedelta(days=months*30)
        df_filtered = df[df['Date'] >= cutoff_date].copy()
        
        if df_filtered.empty:
            print(f"❌ No data available for the last {months} months.")
            return
        
        print(f"\n📈 SPENDING TRENDS (Last {months} months)")
        print("="*50)
        
        # Monthly totals
        monthly_totals = df_filtered.groupby(df_filtered['Date'].dt.to_period('M'))['Montant'].sum()
        
        print("\n📊 Monthly Totals:")
        for month, total in monthly_totals.items():
            print(f"   {month}: €{total:.2f}")
        
        # Average daily spending
        daily_avg = df_filtered.groupby(df_filtered['Date'].dt.date)['Montant'].sum().mean()
        print(f"\n📅 Average daily spending: €{daily_avg:.2f}")
        
        # Top spending categories
        print("\n🏆 Top Spending Categories:")
        category_totals = df_filtered.groupby('Categorie')['Montant'].sum().sort_values(ascending=False)
        for category, total in category_totals.head(5).items():
            percentage = (total / category_totals.sum()) * 100
            print(f"   {category}: €{total:.2f} ({percentage:.1f}%)")
        
        # Account breakdown
        print("\n👥 Account Breakdown:")
        account_totals = df_filtered.groupby('Compte')['Montant'].sum().sort_values(ascending=False)
        for account, total in account_totals.items():
            percentage = (total / account_totals.sum()) * 100
            print(f"   {account}: €{total:.2f} ({percentage:.1f}%)")
    
    def category_analysis(self):
        """Detailed category analysis."""
        df = self.load_all_data()
        if df.empty:
            print("❌ No data available for analysis.")
            return
        
        print("\n📂 CATEGORY ANALYSIS")
        print("="*50)
        
        # Category statistics
        category_stats = df.groupby('Categorie').agg({
            'Montant': ['sum', 'mean', 'count']
        }).round(2)
        
        category_stats.columns = ['Total', 'Average', 'Count']
        category_stats = category_stats.sort_values('Total', ascending=False)
        
        print("\n📊 Category Statistics:")
        for category, row in category_stats.iterrows():
            print(f"   {category}:")
            print(f"     Total: €{row['Total']:.2f}")
            print(f"     Average: €{row['Average']:.2f}")
            print(f"     Transactions: {row['Count']}")
            print()
    
    def account_comparison(self):
        """Compare spending between accounts."""
        df = self.load_all_data()
        if df.empty:
            print("❌ No data available for analysis.")
            return
        
        print("\n👥 ACCOUNT COMPARISON")
        print("="*50)
        
        # Account totals
        account_totals = df.groupby('Compte')['Montant'].sum().sort_values(ascending=False)
        
        print("\n💰 Total Spending by Account:")
        for account, total in account_totals.items():
            print(f"   {account}: €{total:.2f}")
        
        # Account vs Category matrix
        print("\n📊 Spending by Account and Category:")
        pivot_table = df.pivot_table(
            values='Montant', 
            index='Categorie', 
            columns='Compte', 
            aggfunc='sum', 
            fill_value=0
        )
        
        print(pivot_table.round(2))
    
    def generate_charts(self, save_path: str = None):
        """Generate and save charts."""
        df = self.load_all_data()
        if df.empty:
            print("❌ No data available for charts.")
            return
        
        if save_path is None:
            save_path = self.base_dir / "charts"
        
        save_path = Path(save_path)
        save_path.mkdir(exist_ok=True)
        
        # Create subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Expense Analysis Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Monthly spending trend
        monthly_data = df.groupby(df['Date'].dt.to_period('M'))['Montant'].sum()
        axes[0, 0].plot(range(len(monthly_data)), monthly_data.values, marker='o', linewidth=2)
        axes[0, 0].set_title('Monthly Spending Trend')
        axes[0, 0].set_xlabel('Month')
        axes[0, 0].set_ylabel('Amount (€)')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Category breakdown (pie chart)
        category_totals = df.groupby('Categorie')['Montant'].sum()
        axes[0, 1].pie(category_totals.values, labels=category_totals.index, autopct='%1.1f%%')
        axes[0, 1].set_title('Spending by Category')
        
        # 3. Account breakdown (bar chart)
        account_totals = df.groupby('Compte')['Montant'].sum()
        axes[1, 0].bar(account_totals.index, account_totals.values, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        axes[1, 0].set_title('Spending by Account')
        axes[1, 0].set_ylabel('Amount (€)')
        
        # 4. Daily spending distribution
        daily_spending = df.groupby(df['Date'].dt.date)['Montant'].sum()
        axes[1, 1].hist(daily_spending.values, bins=20, alpha=0.7, color='#96CEB4')
        axes[1, 1].set_title('Daily Spending Distribution')
        axes[1, 1].set_xlabel('Amount (€)')
        axes[1, 1].set_ylabel('Frequency')
        
        plt.tight_layout()
        
        # Save chart
        chart_file = save_path / "expense_analysis.png"
        plt.savefig(chart_file, dpi=300, bbox_inches='tight')
        print(f"📊 Charts saved to: {chart_file}")
        
        plt.show()
    
    def spending_insights(self):
        """Generate spending insights and recommendations."""
        df = self.load_all_data()
        if df.empty:
            print("❌ No data available for insights.")
            return
        
        print("\n💡 SPENDING INSIGHTS")
        print("="*50)
        
        # Most expensive day
        daily_totals = df.groupby(df['Date'].dt.date)['Montant'].sum()
        most_expensive_day = daily_totals.idxmax()
        most_expensive_amount = daily_totals.max()
        print(f"💰 Most expensive day: {most_expensive_day} (€{most_expensive_amount:.2f})")
        
        # Most expensive category
        category_totals = df.groupby('Categorie')['Montant'].sum()
        most_expensive_category = category_totals.idxmax()
        most_expensive_category_amount = category_totals.max()
        print(f"📂 Most expensive category: {most_expensive_category} (€{most_expensive_category_amount:.2f})")
        
        # Average transaction size
        avg_transaction = df['Montant'].mean()
        print(f"📊 Average transaction size: €{avg_transaction:.2f}")
        
        # Spending frequency
        total_days = (df['Date'].max() - df['Date'].min()).days + 1
        days_with_expenses = df['Date'].dt.date.nunique()
        spending_frequency = (days_with_expenses / total_days) * 100
        print(f"📅 Spending frequency: {spending_frequency:.1f}% of days")
        
        # Recommendations
        print(f"\n🎯 RECOMMENDATIONS:")
        
        if spending_frequency > 80:
            print("   ⚠️  You're spending almost every day. Consider setting spending-free days.")
        
        if avg_transaction > 50:
            print("   💰 Your average transaction is high. Look for ways to reduce large purchases.")
        
        # Find potential savings
        small_expenses = df[df['Montant'] < 10]
        if not small_expenses.empty:
            small_total = small_expenses['Montant'].sum()
            print(f"   💡 Small expenses (<€10) total: €{small_total:.2f} - consider tracking these better.")

def main():
    analyzer = DataAnalyzer()
    
    while True:
        print("\n" + "="*40)
        print("📊 DATA ANALYZER")
        print("="*40)
        print("1. 📈 Spending trends")
        print("2. 📂 Category analysis")
        print("3. 👥 Account comparison")
        print("4. 📊 Generate charts")
        print("5. 💡 Spending insights")
        print("6. 🚪 Exit")
        print("="*40)
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == '1':
            months = input("Number of months to analyze (default 6): ").strip()
            months = int(months) if months.isdigit() else 6
            analyzer.spending_trends(months)
        elif choice == '2':
            analyzer.category_analysis()
        elif choice == '3':
            analyzer.account_comparison()
        elif choice == '4':
            analyzer.generate_charts()
        elif choice == '5':
            analyzer.spending_insights()
        elif choice == '6':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main() 