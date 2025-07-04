# At the end of the month, archive the expenses.csv file

import os
from datetime import datetime
import shutil

# Get the current month and year
current_month = datetime.now().strftime("%B_%Y")

# Create the archive directory if it doesn't exist
archive_dir = "Archive"
os.makedirs(archive_dir, exist_ok=True)

# Move the expenses.csv file to the archive directory
shutil.move("../Export/expenses.csv", f"../{archive_dir}/{current_month}_expenses.csv")

