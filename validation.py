def get_name():
     while True:
        username = input("Enter your profile username: ")
        if len(username) < 3:
            print("Username should be at least 3 characters long.")
        else:
            return username
        
def get_measurement(message):
    while True:
        measurement = input(message)
        try:
            measurement = int(measurement)
            if measurement <= 0:
                print("Measurement should be a positive number.")
            else:
                return measurement
        except ValueError:
            print("Invalid measurement. Please enter a valid number.")

def get_optional_measurement(message):
    while True:
        measurement = input(message)
        if not measurement.strip():  # If the input is empty
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
