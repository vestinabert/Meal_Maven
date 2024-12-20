import json

class KitchenInventory:
    def __init__(self, json_file):
        """Initializes the KitchenInventory with a JSON file."""
        self._json_file = json_file
        self._inventory = self._load_inventory()

    def _load_inventory(self):
        """Loads inventory from the JSON file."""
        try:
            with open(self._json_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def _save_inventory(self):
        """Saves the inventory back to the JSON file."""
        with open(self._json_file, 'w') as file:
            json.dump(self._inventory, file, indent=4)

    @property
    def inventory(self):
        """Getter for inventory."""
        return self._inventory

    def add_product(self, product, quantity, unit):
        """Adds or updates a product in the inventory."""
        if product not in self._inventory:
            self._inventory[product] = {"quantity": 0, "unit": unit}
        elif self._inventory[product]["unit"] != unit:
            raise ValueError(f"Unit mismatch for '{product}'. Expected: {self._inventory[product]['unit']}")

        self._inventory[product]["quantity"] += quantity
        self._save_inventory()

    def update_product(self, product, quantity, unit):
        """Updates a product's quantity and unit."""
        if product in self._inventory:
            self._inventory[product] = {"quantity": quantity, "unit": unit}
            self._save_inventory()
        else:
            raise KeyError(f"Product '{product}' not found in inventory.")

    def remove_product(self, product):
        """Removes a product from the inventory."""
        if product in self._inventory:
            del self._inventory[product]
            self._save_inventory()
        else:
            raise KeyError(f"Product '{product}' not found in inventory.")
