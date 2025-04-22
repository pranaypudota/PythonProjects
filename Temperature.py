class Temperature:
    def __init__(self, value, unit = 'C'):
        self.value = float (value)
        self.unit = unit.upper ()
        if self.unit not in ['C', 'F', 'K']:
            raise  ValueError ("Invalid Unit. Use 'C', 'F', 'K'")

    def to_celsius(self):
        if self.unit == 'C':
            return self.value
        elif self.unit == 'F':
            return (self.value - 32) * 5 / 9
        elif self.unit == 'K':
            return self.value - 273.15
        return None

    def to_fahrenheit(self):
        if self.unit == 'F'
            return self.value
        celsius = self.to_celsius()
        return (celsius * 9 / 5) + 32

    def to_kelvin(self):
        if self.unit == 'K':
            return self.value
        celsius = self.to_celsius()
        return celsius + 273.15

    def convert_to(self, target_unit):
        target_unit = target_unit.upper()
        if target_unit == 'C':
            return self.to_celsius()
        elif target_unit == 'F':
            return self.to_fahrenheit()
        elif target_unit == 'K':
            return self.to_kelvin()
        else:
            raise ValueError("Invalid target unit. Use 'C', 'F', or 'K'")

    def __str__(self):
                return f"{self.value:.2f}°{self.unit}"
def main():
    print("Temperature Conversion Program")
    print("Supported units: Celsius (C), Fahrenheit (F), Kelvin (K)")

    try:
        # Get user input
        value = float(input("Enter temperature value: "))
        unit = input("Enter original unit (C/F/K): ").upper()
        target = input("Enter target unit (C/F/K): ").upper()

        # Create Temperature object
        temp = Temperature(value, unit )

        # Convert and display result
        converted = temp.convert_to(target)
        print(f"{temp} = {converted:.2f}°{target}")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()