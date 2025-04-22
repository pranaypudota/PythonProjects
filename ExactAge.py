from datetime import datetime
from dateutil.relativedelta import relativedelta

# Input dates from user
date_format = "%d-%m-%Y"
date1_str = input("Enter the first date (DD-MM-YYYY): ")
date2_str = input("Enter the second date (DD-MM-YYYY): ")

# Convert strings to datetime objects
date1 = datetime.strptime(date1_str, date_format)
date2 = datetime.strptime(date2_str, date_format)

# Calculate the difference
diff = abs(date2 - date1)

# Ensure date1 is earlier
if date2 < date1:
    date1, date2 = date2, date1

diff = relativedelta(date2, date1)     #---- Calculate difference using relativedelta -----

print(f"Exact difference: {diff.years} years, {diff.months} months, {diff.days} days")
