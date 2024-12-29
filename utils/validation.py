from datetime import datetime


def get_name(message) -> str:
    while True:
        name = input(message)
        if len(name) < 3:
            print("Name should be at least 3 characters long.")
        else:
            return name


def get_positive_integer(message) -> int:
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


def get_optional_measurement(message) -> float:
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
            print(
                "Invalid measurement. Please enter a valid number or press Enter to calculate."
            )


def get_goal() -> str:
    while True:
        goal = input("Enter your goal (lose, maintain, gain) weight: ").lower()
        if goal not in ["lose", "maintain", "gain"]:
            print("Invalid goal. Please enter 'lose', 'maintain', or 'gain'.")
        else:
            return goal


def get_diet() -> str:
    while True:
        diet = input(
            "Enter your diet preference (vegan, vegetarian, pescatarian, etc.): "
        ).lower()
        if len(diet) < 3:
            print("Diet preference should be at least 3 characters long.")
        else:
            return diet


def get_gender() -> str:
    while True:
        gender = (
            input("Enter your gender (woman/man/prefer not to say): ").strip().lower()
        )
        if gender not in ["woman", "man", "prefer not to say"]:
            print("Invalid input. Please enter 'woman', 'man', or 'prefer not to say'.")
        else:
            return gender


def get_unit() -> str:
    while True:
        VALID_UNITS = ["g", "ml", "pcs"]
        unit = input("Enter unit (e.g., g, ml, pcs): ").strip()
        if unit not in VALID_UNITS:
            print(f"Invalid unit '{unit}'. Allowed units are: {VALID_UNITS}")
        else:
            return unit


def get_expiration_date() -> str:
    """
    Prompts the user to enter an expiration date and returns it in 'YYYY-MM-DD' format.
    Returns None if the user skips entering the date.
    """
    while True:
        expiration_date = input(
            "Enter expiration date (YYYY-MM-DD). Press Enter to skip: "
        ).strip()
        if not expiration_date:
            return None
        try:
            parsed_date = datetime.strptime(expiration_date, "%Y-%m-%d")
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD format.")


def get_filter() -> set:
    VALID_FILTERS = {
        "baking",
        "stove-top",
        "no-cook",
        "vegetarian",
        "vegan",
        "gluten-free",
        "dairy-free",
        "keto",
        "paleo",
        "high-protein",
        "low-fat",
        "chicken",
        "beef",
        "pork",
        "turkey",
        "lamb",
        "fish",
        "seafood",
        "meatless",
        "breakfast",
        "lunch",
        "dinner",
        "snack",
        "dessert",
        "brunch",
        "15min",
        "30min",
        "60min",
        "appetizer",
        "main",
        "side",
        "soup",
        "drink",
    }

    while True:
        user_input = (
            input("\nEnter your filters (comma-separated) or press Enter to skip: ")
            .strip()
            .lower()
        )
        if not user_input:
            return set()

        filters = {
            f.strip() for f in user_input.split(",")
        }  # Create a set of input filters
        invalid_filters = filters - VALID_FILTERS  # Identify invalid filters

        if invalid_filters:
            print(f"Invalid filter(s): {', '.join(invalid_filters)}")
            print(f"Choose from: {', '.join(VALID_FILTERS)}")
        else:
            return filters
