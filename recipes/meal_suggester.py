from openai import OpenAI


class MealSuggester:
    def __init__(self, api_key, user_manager, kitchen):
        self.client = OpenAI(api_key=api_key)
        self.user_manager = user_manager
        self.kitchen = kitchen

    def suggest_meals(self):
        user = self.user_manager.user

        if not user:
            print("No user profile found. Please set a user profile first.")
            return

        if not self.kitchen.inventory:
            print("No inventory found. Please add products to the inventory first.")
            return

        inventory_details = self.get_inventory()

        user_diet = user.diet

        messages = self.generate_messages(user_diet, inventory_details)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )

            suggestions = response.choices[0].message.content.strip()
            print("\n--- Meal Suggestions ---")
            print(suggestions)

        except Exception as e:
            print(f"Error generating meal suggestions: {e}")

    def get_inventory(self):
        return [
            f"{product}: {details['quantity']} {details['unit']} (exp: {details['expiration_date']})"
            for product, details in self.kitchen.inventory.items()
        ]

    def generate_messages(self, user_diet, inventory_details):
        inventory_text = "\n".join(inventory_details)
        messages = [
            {"role": "system", "content": "You are a helpful assistant that provides meal suggestions based on user preferences and available ingredients."},
            {"role": "user", "content": (
                f"Based on the user's diet preferences and available kitchen inventory, suggest three meal recipes.\n\n"
                f"User Diet: {user_diet}\n\n"
                f"Kitchen Inventory:\n{inventory_text}\n\n"
                f"Please format the suggestions as follows:\n\n"
                f"1. Recipe Name\n   - Ingredients: List of ingredients\n   - Steps: Step-by-step instructions\n\n"
                f"Provide three recipes that are simple to prepare and take advantage of ingredients nearing expiration."
            )}
        ]
        return messages
