from user_manager import UserManager
from recipe_suggester import RecipeSuggester
from kitchen_inventory import KitchenInventory
from user import User

def main():
    kitchen_file = "kitchen_inventory.json"
    user_file = "user_profile.json"
    kitchen = KitchenInventory(kitchen_file)
    user_manager = UserManager(user_file)

    while True:
        print("\n--- Main Menu ---")
        print("1. View Inventory")
        print("2. Add Product")
        print("3. Remove Product")
        print("4. Get Recipe Suggestions")
        print("5. Set User Profile")
        print("6. View User Profile")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("\nCurrent Inventory:")
            for product, quantity in kitchen.inventory.items():
                print(f"- {product}: {quantity}")

        elif choice == "2":
            product = input("Enter product name: ")
            quantity = int(input("Enter quantity: "))
            kitchen.add_product(product, quantity)
            print(f"Added {quantity} of {product}.")

        elif choice == "3":
            product = input("Enter product name to remove: ")
            try:
                kitchen.remove_product(product)
                print(f"Removed {product} from inventory.")
            except KeyError as e:
                print(e)

        elif choice == "4":
            print("Fetching recipe suggestions...")
            suggester = RecipeSuggester(kitchen.inventory)
            print(suggester.get_recipes())

        elif choice == "5":
            user = User.create_user()
            user_manager.save_user(user)
            print("User profile saved.")

        elif choice == "6":
            if user_manager.user:
                user_manager.user.display_user_info()
            else:
                print("No user profile found. Please set a user profile first.")

        elif choice == "7":
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
