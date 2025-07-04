from datetime import datetime

default_date = datetime.now().strftime("%d/%m/%Y")
date = input(f"Enter the date (dd/mm/yyyy) [{default_date}]: ").strip()
if not date:
    date = default_date

account_input = input(f"Enter the account ([P]ersonal/[s]hared): ").strip().upper()
if not account_input or account_input == 'P':
    account = 'Personal'
elif account_input == 'S':
    account = 'Shared'
else:
    print("Invalid account type. Defaulting to 'Personal'.")
    account = 'Personal'

categories = ['Groceries', 'Transport', 'Entertainment', 'Food&Drinks', 'Sports', 'Home', 'Other']
print("Select a category from the following list:")
for idx, cat in enumerate(categories, 1):
    print(f"{idx}. {cat}")
cat_choice = input("Enter the number corresponding to the category: ").strip()
try:
    cat_idx = int(cat_choice) - 1
    if 0 <= cat_idx < len(categories):
        category = categories[cat_idx]
    else:
        print("Invalid category. Defaulting to 'Other'.")
        category = 'Other'
except ValueError:
    print("Invalid input. Defaulting to 'Other'.")
    category = 'Other'

description = input("Enter a 1-word description: ").strip().replace(',', '')

amount = input("Enter the amount (€): ").strip()

with open("../expenses_working.txt", "a") as f:
    f.write(f"\n{date},{account},{category},{description},{amount}")

with open("../expenses_working.txt", "r") as src, open("../Export/expenses.csv", "w") as dst:
    dst.write(src.read())
