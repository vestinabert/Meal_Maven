from user.user_manager import UserManager
from inventory.kitchen_inventory import KitchenInventory
from user.user import User
from utils.validation import get_name, get_positive_integer, get_unit, get_expiration_date, get_filter
from recipes.recipe_manager import RecipeManager
from dotenv import load_dotenv
from recipes.meal_suggester import MealSuggester
from recipes.recipe_viewer import RecipeViewer
from recipes.meal_planner import MealPlanner
from PyQt5.QtWidgets import QApplication
import sys
import os

class KitchenApp:
    def __init__(self):
        load_dotenv()
        self.spoonacular_api_key = os.getenv("SPOONACULAR_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        self.kitchen_file = "json/kitchen_inventory.json"
        self.user_file = "json/user_profile.json"
        self.recipe_file = "json/recipe_book.json"

        self.kitchen = KitchenInventory(self.kitchen_file)
        self.user_manager = UserManager(self.user_file)
        self.recipe_manager = RecipeManager(self.recipe_file)
        self.meal_suggester = MealSuggester(self.openai_api_key, self.user_manager, self.kitchen)
        self.meal_planner = MealPlanner(self.spoonacular_api_key, self.user_manager)


    def run(self):
        while True:
            self.display_menu()
            choice = get_positive_integer("Enter your choice: ")
            self.handle_choice(choice)

    def display_menu(self):
        print("\n--- Main Menu ---")
        print("1. View Inventory")
        print("2. View User Profile")
        print("3. Show Recipe Book")
        print("4. Remove Product")
        print("5. Add Product")
        print("6. Set User Profile")
        print("7. Suggest Meals")
        print("8. Plan Meals for the Day")
        print("9. Exit")

    def handle_choice(self, choice):
        if choice == 1:
            self.view_inventory()
        elif choice == 2:
            self.view_user_profile()
        elif choice == 3:
            self.show_recipe_book()
        elif choice == 4:
            self.remove_product()
        elif choice == 5:
            self.add_product()
        elif choice == 6:
            self.set_user_profile()
        elif choice == 7:
            self.suggest_meals()
        elif choice == 8:
            self.meal_planner.plan_meals()
        elif choice == 9:
            print("Exiting program.")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

    def view_inventory(self):
        print("\nCurrent Inventory:")
        for product, details in self.kitchen.inventory.items():
            quantity = details.get("quantity")
            unit = details.get("unit")
            expiration_date = details.get("expiration_date")
            print(f"- {product}: {quantity} {unit}, Expiration Date: {expiration_date}")

    def add_product(self):
        product = get_name("Enter product name: ").lower()
        unit = get_unit()
        quantity = get_positive_integer("Enter quantity: ")
        expiration_date = get_expiration_date()

        try:
            self.kitchen.add_product(product, quantity, unit, expiration_date)
            print(f"Added {quantity} {unit} of {product}.")
        except ValueError as ve:
            print(f"Error: {ve}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def remove_product(self):
        product = input("Enter product name to remove: ")
        try:
            self.kitchen.remove_product(product)
            print(f"Removed {product} from inventory.")
        except KeyError as e:
            print(e)

    def set_user_profile(self):
        try:
            user = User.create_user_from_input()
            self.user_manager.save_user(user)
            print("User profile saved successfully.")
        except Exception as e:
            print(f"An error occurred while creating the user profile: {e}")

    def view_user_profile(self):
        if self.user_manager.user:
            self.user_manager.user.display_user_info()
        else:
            print("No user profile found. Please set a user profile first.")

    def show_recipe_book(self):
        print("\nAvailable Filters:")
        print("Cooking Style: baking, stove-top, no-cook")
        print("Diet: vegetarian, vegan, gluten-free, dairy-free, keto, paleo, high-protein, low-fat")
        print("Meat: chicken, beef, pork, turkey, lamb, fish, seafood, meatless")
        print("Time of the Day: breakfast, lunch, dinner, snack, dessert, brunch")
        print("Time to Prepare: 15min, 30min, 60min")
        print("Meal Type: appetizer, main, side, soup, drink")

        selected_filters = get_filter()

        recipes = self.recipe_manager.recipes
        filtered_recipes = [
            recipe_name for recipe_name, recipe_details in recipes.items()
            if selected_filters.issubset(recipe_details.get("tags", set()))
        ]

        if filtered_recipes:
            print("\nLaunching Recipe Viewer with filtered recipes...")
        
            app = QApplication([])
            viewer = RecipeViewer(self.recipe_file, filtered_recipes)
            viewer.show()
            app.exec_()
        else:
            print("No recipes match the selected filters.")

    def suggest_meals(self):
        self.meal_suggester.suggest_meals()

    
if __name__ == "__main__":
    app = KitchenApp()
    app.run()

