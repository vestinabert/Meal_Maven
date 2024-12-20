from datetime import datetime


def get_name(message):
     while True:
        name = input(message)
        if len(name) < 3:
            print("Name should be at least 3 characters long.")
        else:
            return name
        
def get_positive_integer(message):
    while True:
        measurement = input(message)
        try:
            measurement = int(measurement)
            if measurement <= 0:
                print("Answer should be a positive number.")
            else:
                return measurement
        except ValueError:
            print("Invalid answer. Please enter a valid number.")

def get_optional_measurement(message):
    while True:
        measurement = input(message)
        if not measurement.strip():
            return None
        try:
            measurement = float(measurement)
            if measurement <= 0:
                print("Measurement should be a positive number.")
            else:
                return measurement
        except ValueError:
            print("Invalid measurement. Please enter a valid number or press Enter to calculate.")

def get_goal():
    while True:
        goal = input("Enter your goal (lose, maintain, gain) weight: ").lower()
        if goal not in ["lose", "maintain", "gain"]:
            print("Invalid goal. Please enter 'lose', 'maintain', or 'gain'.")
        else:
            return goal
        
def get_diet():
    while True:
        diet = input("Enter your diet preference (vegan, vegetarian, pescatarian, etc.): ").lower()
        if len(diet) < 3:
            print("Diet preference should be at least 3 characters long.")
        else:
            return diet

def get_gender():
    while True:
        gender = input("Enter your gender (woman/man/prefer not to say): ").strip().lower()
        if gender not in ["woman", "man", "prefer not to say"]:
            print("Invalid input. Please enter 'woman', 'man', or 'prefer not to say'.")
        else:
            return gender

def get_unit():
    while True:
        VALID_UNITS = ["g", "ml", "pcs"]
        unit = input("Enter unit (e.g., g, ml, pcs): ").strip()
        if unit not in VALID_UNITS:
            print(f"Invalid unit '{unit}'. Allowed units are: {VALID_UNITS}")
        else:
            return unit
        
def get_expiration_date():
    """
    Prompts the user to enter an expiration date and returns it in 'YYYY-MM-DD' format.
    Returns None if the user skips entering the date.
    """
    while True:
        expiration_date = input("Enter expiration date (YYYY-MM-DD). Press Enter to skip: ").strip()
        if not expiration_date:
            return None
        try:
            parsed_date = datetime.strptime(expiration_date, "%Y-%m-%d")
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD format.")