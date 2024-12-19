class User:
    def __init__(self, name, gender, weight, daily_calories, daily_water, diet):
        self.name = name
        self.gender = gender
        self.weight = weight
        self.daily_calories = daily_calories
        self.daily_water = daily_water
        self.diet = diet

    def to_dict(self):
        return {
            "name": self.name,
            "gender": self.gender,
            "weight": self.weight,
            "daily_calories": self.daily_calories,
            "daily_water": self.daily_water,
            "diet": self.diet
        }

    @staticmethod
    def from_dict(data):
        return User(
            name=data["name"],
            gender=data["gender"],
            weight=data["weight"],
            daily_calories=data["daily_calories"],
            daily_water=data["daily_water"],
            diet=data["diet"]
        )

    @staticmethod
    def calculate_calories(weight, gender):
        if gender.lower() == "man":
            return int(88.362 + (13.397 * weight) + (4.799 * 175) - (5.677 * 30))
        elif gender.lower() == "woman":
            return int(447.593 + (9.247 * weight) + (3.098 * 175) - (4.330 * 30))
        return 2000  # Default value

    @staticmethod
    def calculate_water(weight):
        return round(weight * 0.033, 2)

    @staticmethod
    def create_user():
        print("\n--- User Information ---")
        name = input("Enter your name: ")
        gender = input("Are you a man or a woman? (man/woman): ")
        weight = float(input("Enter your weight (kg): "))

        daily_calories = input("Enter your recommended daily calorie intake or type 'I don't know': ")
        if daily_calories.lower() == "i don't know":
            daily_calories = User.calculate_calories(weight, gender)
            print(f"Calculated daily calorie intake: {daily_calories} kcal")
        else:
            daily_calories = int(daily_calories)

        daily_water = input("Enter your recommended daily water intake (liters) or type 'I don't know': ")
        if daily_water.lower() == "i don't know":
            daily_water = User.calculate_water(weight)
            print(f"Calculated daily water intake: {daily_water} liters")
        else:
            daily_water = float(daily_water)

        diet = input("What diet are you on? (e.g., vegetarian, keto, etc.): ")
        return User(name, gender, weight, daily_calories, daily_water, diet)

    def display_user_info(self):
        print("\n--- User Profile ---")
        print(f"Name: {self.name}")
        print(f"Gender: {self.gender}")
        print(f"Weight: {self.weight} kg")
        print(f"Daily Calories: {self.daily_calories} kcal")
        print(f"Daily Water Intake: {self.daily_water} liters")
        print(f"Diet: {self.diet}")
