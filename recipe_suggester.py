import json
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


class RecipeSuggester:
    def __init__(self, inventory):
        self.inventory = inventory

    def get_recipes(self):
        """Fetches recipes based on the current inventory using the OpenAI API."""
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": (
                    "You are a helpful assistant. Based on the following kitchen inventory, "
                    "suggest recipes that can be made today. Only use the ingredients listed.\n\n"
                    f"Inventory: {json.dumps(self.inventory, indent=2)}\n\n"
                    "Provide a list of recipe suggestions."
                ),
            },
        ]

        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=messages)

        return response.choices[0].message.content
