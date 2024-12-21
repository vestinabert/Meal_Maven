import json

class RecipeManager:
    def __init__(self, recipe_file):
        self._recipe_file = recipe_file
        self._recipes = self._load_recipes()

    def _load_recipes(self):
        try:
            with open(self._recipe_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            print("Error decoding the recipe file.")
            return {}

    def _save_recipes(self):
        with open(self._recipe_file, "w") as file:
            json.dump(self._recipes, file, indent=4)

    @property
    def recipes(self):
        return self._recipes