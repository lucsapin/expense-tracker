# Enhanced Expense Tracker

A comprehensive, user-friendly tool for tracking personal and shared expenses with advanced features including budget tracking, data analysis, and visualizations.

## ✨ New Features

- **🎯 Budget Tracking**: Set monthly budgets by category and get alerts
- **📊 Data Analysis**: Detailed insights and spending trends
- **📈 Visualizations**: Charts and graphs for better understanding
- **🔍 Smart Search**: Find expenses by date, category, or amount
- **📱 Better UX**: Emoji-enhanced interface with validation
- **💾 Data Integrity**: Robust error handling and data validation
- **📁 Organized Structure**: Better file management and organization

## 🏗️ Project Structure

```bash
Expense Tracker/
├── src/
│   └── add_new_expense.py           # Legacy simple expense adder
│   └── budget_tracker.py            # Budget management and alerts
│   └── data_analyzer.py             # Data analysis and visualizations
│   └── end_of_month_archive.py      # Legacy archiving
│   └── expense_tracker.py           # Main expense tracking application
│   └── monthly_expenses_monitor.py  # Legacy monthly summary
│   └── run.py                       # Main entry point for initializing and running the application
│   └── setup.py                     # setup instructions for the expense tracker project
├── Expenses/
│   └── expenses_working.csv         # Current month's expenses
│   └── expenses_template.txt        # Current month's expenses
├── History/                         # Archived monthly data
├── Summary/                         # Monthly summaries
├── Budget/                          # Monthly summaries
│   └── charges.json                 # Current month's expenses
│   └── income.csv                   # Income tracking
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Enhanced Tracker

```bash
python src/expense_tracker.py
```

## 📋 Main Features

### 💰 Expense Tracking (`expense_tracker.py`)

- **Add Expenses**: Intuitive interface with category selection
- **View Recent**: See your latest transactions
- **Monthly Summary**: Comprehensive spending overview
- **Archive Month**: End-of-month data management

### 🎯 Budget Management (`budget_tracker.py`)

- **Set Budgets**: Configure monthly limits by category
- **Track Progress**: Monitor spending vs. budget
- **Get Alerts**: Warnings when approaching limits
- **Interactive Setup**: Easy budget configuration

### 📊 Data Analysis (`data_analyzer.py`)

- **Spending Trends**: Analyze patterns over time
- **Category Analysis**: Detailed breakdown by category
- **Account Comparison**: Compare spending between accounts
- **Generate Charts**: Visual representations of your data
- **Smart Insights**: AI-powered recommendations

## 🎮 Usage Examples

### Adding an Expense

```bash
python src/expense_tracker.py
# Select option 1: Add new expense
# Follow the interactive prompts
```

### Setting Up Budgets

```bash
python src/budget_tracker.py
# Select option 3: Setup budgets
# Configure limits for each category
```

### Analyzing Your Data

```bash
python src/data_analyzer.py
# Select option 1: Spending trends
# View insights and recommendations
```

## 📊 Sample Output

### Monthly Summary

```bash
📈 MONTHLY SUMMARY - 2025-01
============================================================

👤 Commun: €1,847.35
   📂 Maison: €1,141.35 (61.8%)
   📂 Transport: €63.00 (3.4%)
   📂 Courses: €141.00 (7.6%)
   📂 Culture: €14.00 (0.8%)
   📂 Autre: €488.00 (26.4%)

👤 Luc: €1,147.00
   📂 Restaurant: €66.00 (5.8%)
   📂 Shopping: €258.00 (22.5%)
   📂 Autre: €823.00 (71.7%)

💰 TOTAL EXPENSES: €2,994.35
```

### Budget Alerts

```bash
📊 Budget Status: Luc - Shopping
   💰 Budget: €150.00
   💸 Spent: €258.00
   📈 Percentage: 172.0%
   ⚠️  WARNING: Budget exceeded!
```

## 🔧 Configuration

### Categories

The system includes these expense categories:

- 🏠 Maison (Home)
- 🚗 Transport
- 🏥 Santé (Health)
- 🍽️ Restaurant
- 🛒 Courses (Groceries)
- 💆 Bien-être (Wellness)
- 🎭 Culture
- 🏃 Sport
- 🛍️ Shopping
- 🌭 Saucisse (Food)
- 💵 Liquide (Cash)
- 💰 Economie (Savings)
- 🎁 Cadeau (Gifts)
- 📦 Autre (Other)

### Accounts

- **Commun**: Shared expenses
- **Luc**: Personal expenses
- **Laura**: Personal expenses

## 📈 Data Export

The system automatically generates:

- **Monthly summaries** in CSV format
- **Charts and visualizations** as PNG files
- **Archived data** for historical analysis

## 🛠️ Customization

### Adding New

Edit the `categories` dictionary in `expense_tracker.py`:

```python
self.categories = {
    '🏠': 'Maison',
    '🚗': 'Transport',
    # Add your new categories here
    '🎮': 'Gaming',
}
```

### Modifying Budgets

Edit `budgets.json` or use the interactive setup:

```json
{
  "Commun": {
    "Maison": 1500,
    "Transport": 200
  }
}
```

## 🔄 Migration from Legacy

If you're upgrading from the old system:

1. Your existing data files are compatible
2. Run the new tracker to get enhanced features
3. Set up budgets for better tracking
4. Use data analysis for insights

## 🤝 Contributing

Feel free to customize and extend this project:

- Add new features
- Improve the UI
- Add more analysis tools
- Create custom reports

## 📝 Notes

- All amounts are stored in euros (€)
- Dates use DD/MM/YYYY format
- Data is automatically backed up in the History folder
- Charts are saved in a `charts/` directory

---

Happy tracking! 💰📊
