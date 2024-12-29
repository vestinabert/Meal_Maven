import requests
import json

class MealPlanner:
    def __init__(self, api_key, user_manager):
        self.api_key = api_key
        self.user_manager = user_manager
        self.plan_file = "json/meal_plan.json"

    def plan_meals(self):
        if not self.user_manager.user:
            print("No user profile found. Please set a user profile first.")
            return

        try:
            user = self.user_manager.user
            calories = user.daily_calories
            diet = user.diet.lower()

            response = requests.get(
                "https://api.spoonacular.com/mealplanner/generate",
                params={
                    "apiKey": self.api_key,
                    "timeFrame": "day",
                    "targetCalories": calories,
                    "diet": diet,
                },
            )

            if response.status_code == 200:
                meal_plan = response.json()

                for meal in meal_plan.get("meals", []):
                    nutrition = self.fetch_recipe_nutrition(meal['id'])
                    meal["nutrition"] = nutrition if nutrition else {}

                self.save_plan(meal_plan)
                self.display_meal_plan(meal_plan)
            else:
                print(f"Error: Unable to fetch meal plan. {response.status_code} - {response.text}")

        except Exception as e:
            print(f"An error occurred while generating the meal plan: {e}")

    def fetch_recipe_nutrition(self, recipe_id):
        try:
            response = requests.get(
                f"https://api.spoonacular.com/recipes/{recipe_id}/nutritionWidget.json",
                params={"apiKey": self.api_key},
            )

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching nutrition for recipe {recipe_id}: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            print(f"An error occurred while fetching nutrition data: {e}")
            return None

    def display_meal_plan(self, meal_plan):
        print("\n--- Daily Meal Plan ---")
        total_calories = meal_plan.get("nutrients", {}).get("calories", 0)
        total_protein = meal_plan.get("nutrients", {}).get("protein", 0)
        total_fat = meal_plan.get("nutrients", {}).get("fat", 0)
        total_carbs = meal_plan.get("nutrients", {}).get("carbs", 0)

        print(f"Total Calories: {total_calories} kcal")
        print(f"Total Protein: {total_protein} g")
        print(f"Total Fat: {total_fat} g")
        print(f"Total Carbs: {total_carbs} g\n")

        for meal in meal_plan.get("meals", []):
            nutrition = meal.get("nutrition", {})
            calories = nutrition.get('calories', 'N/A')
            protein = nutrition.get('protein', 'N/A')
            fat = nutrition.get('fat', 'N/A')
            carbs = nutrition.get('carbs', 'N/A')
            print(f"Meal: {meal['title']}")
            print(f"Calories: {calories} kcal")
            print(f"Protein: {protein}")
            print(f"Fat: {fat}")
            print(f"Carbs: {carbs}")
            print(f"Servings: {meal['servings']}")
            print(f"Ready in: {meal['readyInMinutes']} minutes")
            print(f"Recipe Link: {meal['sourceUrl']}\n")

    def save_plan(self, meal_plan):
        try:
            simplified_plan = {
                "nutrients": meal_plan.get("nutrients", {}),
                "meals": []
            }

            for meal in meal_plan.get("meals", []):
                nutrition = meal.get("nutrition", {})
                simplified_meal = {
                    "title": meal.get("title"),
                    "calories": nutrition.get("calories", "N/A"),
                    "protein": nutrition.get("protein", "N/A"),
                    "fat": nutrition.get("fat", "N/A"),
                    "carbs": nutrition.get("carbs", "N/A"),
                    "image": meal.get("image", "N/A"),
                    "ingredients": [],
                    "instructions": "N/A"
                }

                try:
                    recipe_response = requests.get(
                        f"https://api.spoonacular.com/recipes/{meal['id']}/information",
                        params={"apiKey": self.api_key}
                    )
                    if recipe_response.status_code == 200:
                        recipe_data = recipe_response.json()
                        simplified_meal["ingredients"] = [
                            ingredient.get("original") for ingredient in recipe_data.get("extendedIngredients", [])
                        ]
                        simplified_meal["instructions"] = recipe_data.get("instructions", "No instructions provided")
                except Exception as e:
                    print(f"Error fetching recipe details for {meal['title']}: {e}")

                simplified_plan["meals"].append(simplified_meal)

            with open(self.plan_file, "w") as file:
                json.dump(simplified_plan, file, indent=4)
            print(f"Meal plan saved to {self.plan_file}")

        except Exception as e:
            print(f"Error saving meal plan: {e}")

