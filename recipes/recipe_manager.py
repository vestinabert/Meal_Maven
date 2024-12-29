# clean uderstandable code
import json


class RecipeManager:
    def __init__(self, recipe_file):
        """Initializes the RecipeManager with a JSON file."""
        self._recipe_file = recipe_file
        self._recipes = self._load_recipes()

    def _load_recipes(self):
        """Loads recipes from the JSON file."""
        try:
            with open(self._recipe_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def _save_recipes(self) -> None:
        """Saves the recipes back to the JSON file."""
        with open(self._recipe_file, "w") as file:
            json.dump(self._recipes, file, indent=4)

    @property
    def recipes(self):
        """Getter for recipes."""
        return self._recipes
