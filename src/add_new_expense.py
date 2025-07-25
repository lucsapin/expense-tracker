from datetime import datetime

default_date = datetime.now().strftime("%d/%m/%Y")
date = input(f"Enter the date (dd/mm/yyyy) [{default_date}]: ").strip()
if not date:
    date = default_date

COMPTE = [
    "Commun",
    "Luc",
    "Laura"
]

account_input = input(f"Enter the account (Commun/Luc/Laura): ").strip()
if account_input in COMPTE:
    account = account_input
else:
    print("Valeur par défaut: Commun")
    account = 'Commun'

CATEGORIES = [
    'Maison',
    'Transport',
    'Santé',
    'Restaurant',
    'Courses',
    'Bien-être',
    'Culture',
    'Sport',
    'Shopping',
    'Saucisse',
    'Liquide',
    'Economie',
    'Cadeau',
    'Autre'
]


print("Select a category from the following list:")
for idx, cat in enumerate(CATEGORIES, 1):
    print(f"{idx}. {cat}")
cat_choice = input("Enter the number corresponding to the category: ").strip()
try:
    cat_idx = int(cat_choice) - 1
    if 0 <= cat_idx < len(CATEGORIES):
        category = CATEGORIES[cat_idx]
    else:
        print("Invalid category. Defaulting to 'Autre'.")
        category = 'Autre'
except ValueError:
    print("Invalid input. Defaulting to 'Autre'.")
    category = 'Autre'

description = input("Enter a 1-word description: ").strip().replace(',', '')

amount = input("Enter the amount (€): ").strip()

with open("../expenses_working.txt", "a") as f:
    f.write(f"\n{date},{account},{category},{description},{amount}")
