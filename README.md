# Kitchen Manager App

A Python-based application that helps users manage their kitchen inventory, plan meals, and get recipe suggestions based on dietary preferences and available ingredients.

## Features

- **Inventory Management**: Add, view, and remove items in the kitchen inventory.
- **User Profile Management**: Create and manage user profile with details like weight, height, age, dietary preferences, and fitness goals.
- **Recipe Viewer**: Browse recipes with filters like cooking style, dietary restrictions, and preparation time.
- **Meal Suggestions**: Get meal suggestions tailored to your inventory and dietary preferences using OpenAI GPT-based recommendations.
- **Meal Planning**: Plan daily meals based on caloric goals and dietary restrictions using Spoonacular API.
- **Interactive User Interface**: Includes PyQt5-based UI components for an intuitive experience.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/vestinabert/Meal_Maven.git
   cd kitchen-manager

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt

3. Set up environment variables:
- Create a .env file in the root directory.
- Add your API keys for OpenAI and Spoonacular:
    ```bash
    SPOONACULAR_API_KEY=your_spoonacular_api_key
    OPENAI_API_KEY=your_openai_api_key

4. Run the application:
    ```bash
    python main.py
