import json

class KitchenInventory:
    def __init__(self, json_file):
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

    @inventory.setter
    def inventory(self, new_inventory):
        """Setter for inventory."""
        if isinstance(new_inventory, dict):
            self._inventory = new_inventory
            self._save_inventory()
        else:
            raise ValueError("Inventory must be a dictionary.")

    def add_product(self, product, quantity):
        """Adds or updates a product in the inventory."""
        self._inventory[product] = self._inventory.get(product, 0) + quantity
        self._save_inventory()

    def remove_product(self, product):
        """Removes a product from the inventory."""
        if product in self._inventory:
            del self._inventory[product]
            self._save_inventory()
        else:
            raise KeyError(f"Product '{product}' not found in inventory.")
