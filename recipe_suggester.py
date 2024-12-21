import json
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
spoonacular_api_key = os.getenv("SPOONACULAR_API_KEY")


class RecipeSuggester:
    def __init__(self, inventory):
        self.inventory = inventory
        self.api_key = spoonacular_api_key
        self.base_url = "https://api.spoonacular.com"
        self.recipes = []

    def get_recipes(self):
        """Fetches recipes based on the inventory using Spoonacular API."""
        # Join inventory items with commas
        ingredients = ",".join(self.inventory)

        # API endpoint for finding recipes by ingredients
        url = f"{self.base_url}/recipes/findByIngredients"
        params = {
            "ingredients": ingredients,
            "number": 3,  # Get three recipes
            "ranking": 1,
            "apiKey": self.api_key,
        }

        # Make the API request
        response = requests.get(url, params=params)

        if response.status_code == 200:
            self.recipes = response.json()
            print("Recipes Found:")
            for i, recipe in enumerate(self.recipes, 1):
                print(f"{i}. {recipe['title']}")
            self.prompt_user_for_recipe()
        else:
            print(f"Error: {response.status_code} - {response.text}")

    def prompt_user_for_recipe(self):
        """Prompts the user to select a recipe and fetches details."""
        try:
            recipe_number = int(input("\nEnter the number of the recipe you want to save: "))
            if 1 <= recipe_number <= len(self.recipes):
                selected_recipe = self.recipes[recipe_number - 1]
                self.get_recipe_details(selected_recipe["id"])
            else:
                print("Invalid recipe number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def get_recipe_details(self, recipe_id):
        """Fetches detailed instructions and ingredient quantities for the selected recipe."""
        # API endpoint for recipe details
        url = f"{self.base_url}/recipes/{recipe_id}/information"
        params = {
            "apiKey": self.api_key,
            "includeNutrition": True,  # Include detailed ingredient information in metric units
        }

        # Make the API request
        response = requests.get(url, params=params)

        if response.status_code == 200:
            recipe_details = response.json()

            # Ensure all ingredients are in metric units
            formatted_recipe = self.format_recipe(recipe_details)
            self.save_to_recipe_book(formatted_recipe)
        else:
            print(f"Error: {response.status_code} - {response.text}")

    def format_recipe(self, recipe):
        """Formats the recipe into the desired JSON structure."""
        formatted = {
            recipe["title"]: {
                "description": recipe.get("summary", "No description available."),
                "servings": recipe.get("servings", 1),
                "ingredients": [
                    self.extract_metric_ingredient(ingredient)
                    for ingredient in recipe["extendedIngredients"]
                ],
                "instructions": [
                    step["step"] for step in recipe.get("analyzedInstructions", [{}])[0].get("steps", [])
                ],
            }
        }
        return formatted

    def extract_metric_ingredient(self, ingredient):
        """Extracts ingredient details in metric units."""
        measures = ingredient.get("measures", {}).get("metric", {})
        return {
            "name": ingredient["name"],
            "quantity": measures.get("amount", ingredient["amount"]),  # Use metric amount if available
            "unit": measures.get("unitShort", ingredient["unit"]),     # Use metric unit if available
        }

    def save_to_recipe_book(self, recipe):
        """Saves the selected recipe to the recipe book in JSON format."""
        try:
            # Load the existing recipe book or create a new one
            if os.path.exists("recipe_book.json"):
                with open("recipe_book.json", "r") as file:
                    recipe_book = json.load(file)
            else:
                recipe_book = {}

            # Merge the new recipe into the recipe book
            recipe_book.update(recipe)

            # Save the updated recipe book
            with open("recipe_book.json", "w") as file:
                json.dump(recipe_book, file, indent=4)

            print("Recipe saved to recipe_book.json!")
        except Exception as e:
            print(f"An error occurred while saving the recipe: {e}")


