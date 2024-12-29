import json
from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QTextEdit, QScrollArea
)
from PyQt5.QtCore import Qt

class RecipeViewer(QMainWindow):
    def __init__(self, recipe_file, filtered_recipes):
        super().__init__()
        self.recipe_file = recipe_file
        self.recipes = self.load_recipes(filtered_recipes)

        self.init_ui()

    def load_recipes(self, filtered_recipes=None):
        """Load recipes from the JSON file, applying filters if provided."""
        try:
            with open(self.recipe_file, "r") as file:
                all_recipes = json.load(file)
                if filtered_recipes:
                    return {name: details for name, details in all_recipes.items() if name in filtered_recipes}
                return all_recipes
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            print("Error decoding recipe file.")
            return {}

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Recipe Viewer")
        self.setGeometry(100, 100, 900, 700)

        # Central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Scrollable area for recipe list
        self.scroll_area = QScrollArea(self)
        self.scroll_area_widget = QWidget()
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_widget)
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        # Details area
        self.details_widget = QWidget()
        self.details_layout = QVBoxLayout(self.details_widget)
        self.details_widget.hide()
        self.layout.addWidget(self.details_widget)

        # Details - Recipe title
        self.title_label = QLabel("", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")
        self.details_layout.addWidget(self.title_label)

        # Details - Description
        self.description_text = QTextEdit(self)
        self.description_text.setReadOnly(True)
        self.description_text.setStyleSheet("font-size: 16px; background-color: #ecf0f1; border-radius: 5px;")
        self.description_text.setFixedHeight(100)
        self.details_layout.addWidget(self.description_text)

        # Details - Ingredients
        self.ingredients_label = QLabel("Ingredients:", self)
        self.ingredients_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #34495e;")
        self.details_layout.addWidget(self.ingredients_label)

        self.ingredients_text = QTextEdit(self)
        self.ingredients_text.setReadOnly(True)
        self.ingredients_text.setStyleSheet("font-size: 16px; background-color: #ecf0f1; border-radius: 5px;")
        self.details_layout.addWidget(self.ingredients_text)

        # Details - Instructions
        self.instructions_label = QLabel("Instructions:", self)
        self.instructions_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #34495e;")
        self.details_layout.addWidget(self.instructions_label)

        self.instructions_text = QTextEdit(self)
        self.instructions_text.setReadOnly(True)
        self.instructions_text.setStyleSheet("font-size: 16px; background-color: #ecf0f1; border-radius: 5px;")
        self.instructions_text.setFixedHeight(300)
        self.details_layout.addWidget(self.instructions_text)

        # Back button
        self.back_button = QPushButton("Back", self)
        self.back_button.setStyleSheet("font-size: 16px; padding: 10px; background-color: #e74c3c; color: white; border-radius: 5px;")
        self.back_button.clicked.connect(self.show_recipe_list)
        self.details_layout.addWidget(self.back_button)

        self.populate_recipe_list()

    def populate_recipe_list(self):
        """Populate the recipe list with buttons."""
        for recipe_name, details in self.recipes.items():
            button = QPushButton(f"{recipe_name} - Tags: {', '.join(details.get('tags', []))}", self)
            button.setStyleSheet("font-size: 16px; padding: 10px; background-color: #3498db; color: white; border-radius: 5px;")
            button.clicked.connect(lambda checked, name=recipe_name: self.display_recipe(name))
            self.scroll_area_layout.addWidget(button)

    def display_recipe(self, recipe_name):
        """Display the selected recipe."""
        recipe = self.recipes.get(recipe_name, {})

        # Update details
        self.title_label.setText(recipe_name)
        self.description_text.setText(recipe.get("description", "No description available."))

        ingredients = recipe.get("ingredients", [])
        ingredients_list = "\n".join(
            f"- {ingredient['name']}: {ingredient['quantity']} {ingredient['unit']}" for ingredient in ingredients
        )
        self.ingredients_text.setText(ingredients_list)

        instructions = recipe.get("instructions", [])
        instructions_list = "\n".join(f"Step {i+1}: {step}" for i, step in enumerate(instructions))
        self.instructions_text.setText(instructions_list)

        # Switch view
        self.scroll_area.hide()
        self.details_widget.show()

    def show_recipe_list(self):
        """Show the recipe list view."""
        self.details_widget.hide()
        self.scroll_area.show()
