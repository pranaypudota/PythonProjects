import datetime

def get_day_of_week(day: int, month: int, year: int) -> str:
    date = datetime.date(year, month, day)
    return date.strftime('%A')  # Returns the full weekday name

# Example Usage
#print(get_day_of_week(21, 4, 2025))  # Output: Monday
def main():
    day = int(input("Enter day (DD): "))
    month = int(input("Enter month (MM): "))
    year = int(input("Enter year (YYYY): "))

    try:
        day_name = get_day_of_week(day, month, year)
        print(f"The day was: {day_name}")
    except ValueError as e:
        print("Invalid date:", e)

if __name__ == "__main__":
    main()

