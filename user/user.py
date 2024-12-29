from utils.validation import (
    get_name,
    get_positive_integer,
    get_optional_measurement,
    get_goal,
    get_diet,
    get_gender,
)


class User:
    def __init__(
        self,
        name,
        gender,
        weight,
        height,
        age,
        workout_days,
        daily_calories,
        daily_water,
        diet,
        goal,
    ):
        """Initializes the User with the given attributes."""
        self.name = name
        self.gender = gender
        self.weight = weight
        self.height = height
        self.age = age
        self.workout_days = workout_days
        self.daily_calories = daily_calories
        self.daily_water = daily_water
        self.diet = diet
        self.goal = goal

    @staticmethod
    def create_user_from_input():
        """Creates a new User object based on user input."""
        print("\n--- User Information ---")
        name = get_name("Enter your name: ")
        gender = get_gender()
        weight = get_positive_integer("Enter your weight (kg): ")
        height = get_positive_integer("Enter your height (cm): ")
        age = get_positive_integer("Enter your age: ")
        workout_days = get_positive_integer(
            "Enter the number of how many times you work out per week: "
        )
        goal = get_goal()

        daily_calories = get_optional_measurement(
            "Enter your daily calorie intake (kcal) or press Enter to calculate: "
        )
        if daily_calories is None:
            daily_calories = User.calculate_calories(
                weight, height, age, gender, workout_days, goal
            )
            print(
                f"Calculated daily calorie intake based on your goal: {daily_calories} kcal"
            )
        else:
            daily_calories = int(daily_calories)

        daily_water = get_optional_measurement(
            "Enter your daily water intake (liters) or press Enter to calculate: "
        )
        if daily_water is None:
            daily_water = User.calculate_water(weight, workout_days)
            print(f"Calculated daily water intake: {daily_water} liters")
        else:
            daily_water = float(daily_water)

        diet = get_diet()
        return User(
            name,
            gender,
            weight,
            height,
            age,
            workout_days,
            daily_calories,
            daily_water,
            diet,
            goal,
        )

    @staticmethod
    def calculate_calories(weight, height, age, gender, workout_days, goal):
        """Calculates daily calorie needs dynamically based on workout days."""
        if gender == "man":
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        elif gender == "woman":
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

        min_multiplier = 1.2
        max_multiplier = 1.9
        activity_multiplier = min_multiplier + (max_multiplier - min_multiplier) * (
            workout_days / 7
        )
        tdee = bmr * activity_multiplier

        if goal.lower() == "lose":
            return int(tdee - 500)
        elif goal.lower() == "gain":
            return int(tdee + 500)
        else:
            return int(tdee)

    @staticmethod
    def calculate_water(weight, workout_days):
        """Calculates daily water intake based on weight and activity."""
        base_water = weight * 0.03
        additional_water = workout_days * (0.3 / 7)
        return round(base_water + additional_water, 1)

    def display_user_info(self) -> None:
        """Displays the user profile information."""
        print("\n--- User Profile ---")
        print(f"Name: {self.name}")
        print(f"Gender: {self.gender}")
        print(f"Weight: {self.weight} kg")
        print(f"Height: {self.height} cm")
        print(f"Age: {self.age}")
        print(f"Workout days: {self.workout_days}")
        print(f"Goal: {self.goal}")
        print(f"Daily Calories: {self.daily_calories} kcal")
        print(f"Daily Water Intake: {self.daily_water} liters")
        print(f"Diet: {self.diet}")

    def to_dict(self):
        """Converts the User object to a dictionary."""
        return {
            "name": self.name,
            "gender": self.gender,
            "weight": self.weight,
            "height": self.height,
            "age": self.age,
            "workout_days": self.workout_days,
            "goal": self.goal,
            "daily_calories": self.daily_calories,
            "daily_water": self.daily_water,
            "diet": self.diet,
        }

    @staticmethod
    def from_dict(data):
        """Creates a User object from a dictionary."""
        return User(
            name=data["name"],
            gender=data["gender"],
            weight=data["weight"],
            height=data["height"],
            age=data["age"],
            workout_days=data["workout_days"],
            daily_calories=data["daily_calories"],
            daily_water=data["daily_water"],
            diet=data["diet"],
            goal=data["goal"],
        )
