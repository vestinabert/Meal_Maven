from validation import get_name, get_diet, get_positive_integer, get_goal, get_gender, get_optional_measurement

class User:
    def __init__(self, name, gender, weight, height, age, activity_level, daily_calories, daily_water, diet, goal):
        """Initializes the User with the given attributes."""
        self.name = name
        self.gender = gender
        self.weight = weight
        self.height = height
        self.age = age
        self.activity_level = activity_level
        self.daily_calories = daily_calories
        self.daily_water = daily_water
        self.diet = diet
        self.goal = goal

    @staticmethod
    def create_user():
        """Creates a new User object based on user input."""
        print("\n--- User Information ---")
        name = get_name("Enter your name: ")
        gender = get_gender()
        weight = get_positive_integer("Enter your weight (kg): ")
        height = get_positive_integer("Enter your height (cm): ")
        age = get_positive_integer("Enter your age: ")
        workout_days = get_positive_integer("Enter the number of how many times you work out per week: ")
        goal = get_goal()

        daily_calories = get_optional_measurement("Enter your daily calorie intake (kcal) or press Enter to calculate: ")
        if daily_calories is None:
            daily_calories = User.calculate_calories(weight, height, age, gender, workout_days, goal)
            print(f"Calculated daily calorie intake based on your goal: {daily_calories} kcal")
        else:
            daily_calories = int(daily_calories)

        daily_water = get_optional_measurement("Enter your daily water intake (liters) or press Enter to calculate: ")
        if daily_water is None:
            daily_water = User.calculate_water(weight, workout_days)
            print(f"Calculated daily water intake: {daily_water} liters")
        else:
            daily_water = float(daily_water)

        diet = get_diet()
        return User(name, gender, weight, height, age, workout_days, daily_calories, daily_water, diet, goal)

    def display_user_info(self):
        """Displays the user profile information."""
        print("\n--- User Profile ---")
        print(f"Name: {self.name}")
        print(f"Gender: {self.gender}")
        print(f"Weight: {self.weight} kg")
        print(f"Height: {self.height} cm")
        print(f"Age: {self.age}")
        print(f"Activity Level: {self.activity_level}")
        print(f"Goal: {self.goal}")
        print(f"Daily Calories: {self.daily_calories} kcal")
        print(f"Daily Water Intake: {self.daily_water} liters")
        print(f"Diet: {self.diet}")

    @staticmethod
    def calculate_calories(weight, height, age, gender, workout_days, goal):
        """Calculates daily calorie needs dynamically based on workout days."""
        # Basal Metabolic Rate (BMR)
        if gender == "man":
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        elif gender == "woman":
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        elif gender == "prefer not to say":
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age) # Don't know how to calculate BMR for this case
        else:
            raise ValueError("Invalid gender. Must be 'man' or 'woman'.")

        # Dynamic Activity Multiplier
        min_multiplier = 1.2 
        max_multiplier = 1.9
        activity_multiplier = min_multiplier + (max_multiplier - min_multiplier) * (workout_days / 7)

        # Total Daily Energy Expenditure (TDEE)
        tdee = bmr * activity_multiplier

        # Adjust for Goal
        if goal.lower() == "lose":
            return int(tdee - 500)  # Moderate deficit for fat loss
        elif goal.lower() == "gain":
            return int(tdee + 500)  # Moderate surplus for muscle gain
        else:
            return int(tdee)

    @staticmethod
    def calculate_water(weight, workout_days):
        """Calculates daily water intake based on various factors."""
        # Base water intake (liters per kg body weight)
        base_water = weight * 0.03

        # Additional water for activity level
        additional_water_per_day = 0.3  # Fixed extra water per workout day
        activity_water = workout_days * (additional_water_per_day / 7)  # Spread across the week

        total_water = (base_water + activity_water)
        return round(total_water, 1)

    def to_dict(self):
        """Converts the User object to a dictionary."""
        return {
            "name": self.name,
            "gender": self.gender,
            "weight": self.weight,
            "height": self.height,
            "age": self.age,
            "activity_level": self.activity_level,
            "goal": self.goal,
            "daily_calories": self.daily_calories,
            "daily_water": self.daily_water,
            "diet": self.diet
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
            activity_level=data["activity_level"],
            goal=data["goal"],
            daily_calories=data["daily_calories"],
            daily_water=data["daily_water"],
            diet=data["diet"]
        )
