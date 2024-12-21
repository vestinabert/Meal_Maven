from user.user_manager import UserManager
from recipe_suggester import RecipeSuggester
from kitchen_inventory import KitchenInventory
from user.user import User
from validation import get_name, get_positive_integer, get_unit, get_expiration_date, get_filter
from recipe_manager import RecipeManager


def main():
    kitchen_file = "json/kitchen_inventory.json"
    user_file = "json/user_profile.json"
    recipe_file = "json/recipe_book.json"

    kitchen = KitchenInventory(kitchen_file)
    user_manager = UserManager(user_file)
    recipe_manager = RecipeManager(recipe_file)

    while True:
        print("\n--- Main Menu ---")
        print("1. View Inventory")
        print("2. Add Product")
        print("3. Remove Product")
        print("4. Get Recipe Suggestions")
        print("5. Set User Profile")
        print("6. View User Profile")
        print("7. List All Recipes")
        print("8. Exit")

        choice = get_positive_integer("Enter your choice: ")

        if choice == 1:
            print("\nCurrent Inventory:")
            for product, details in kitchen.inventory.items():
                quantity = details.get("quantity")
                unit = details.get("unit")
                expiration_date = details.get("expiration_date", "None")
                print(f"- {product}: {quantity} {unit}, Expiration Date: {expiration_date}")

        elif choice == 2:
            product = get_name("Enter product name: ").lower()
            quantity = get_positive_integer("Enter quantity: ")
            unit = get_unit()
            expiration_date = get_expiration_date()

            try:
                kitchen.add_product(product, quantity, unit, expiration_date)
                print(f"Added {quantity} {unit} of {product}.")
            except ValueError as ve:
                print(f"Error: {ve}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        elif choice == 3:
            product = input("Enter product name to remove: ")
            try:
                kitchen.remove_product(product)
                print(f"Removed {product} from inventory.")
            except KeyError as e:
                print(e)

        elif choice == 4:
            print("Fetching recipe suggestions...")
            suggester = RecipeSuggester(kitchen.inventory)
            print(suggester.get_recipes())

        elif choice == 5:
            user = User.create_user()
            user_manager.save_user(user)
            print("User profile saved.")

        elif choice == 6:
            if user_manager.user:
                user_manager.user.display_user_info()
            else:
                print("No user profile found. Please set a user profile first.")

        elif choice == 7:
            print("\nAvailable Filters:")
            print("Cooking Style: baking, stove-top, no-cook")
            print("Diet: vegetarian, vegan, gluten-free, dairy-free, keto, paleo, high-protein, low-fat")
            print("Meat: chicken, beef, pork, turkey, lamb, fish, seafood, meatless")
            print("Time of the Day: breakfast, lunch, dinner, snack, dessert, brunch")
            print("Time to Prepare: 15min, 30min, 60min")
            print("Meal Type: appetizer, main, side, soup, drink")

            selected_filters = get_filter()

            recipes = recipe_manager.recipes  # Assuming recipe_manager.recipes is a dictionary
            filtered_recipes = {
                recipe_name: recipe_details.get("tags", set())
                for recipe_name, recipe_details in recipes.items()
                if selected_filters.issubset(recipe_details.get("tags", set()))
            }

            if filtered_recipes:
                print("\nAvailable Recipes:")
                for recipe_name, tags in filtered_recipes.items():
                    print(f"- {recipe_name} ({', '.join(tags)})")
            else:
                print("No recipes match the selected filters.")

                    
        elif choice == 8:
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
