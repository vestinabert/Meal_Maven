from user import User
import json


class UserManager:
    def __init__(self, json_file):
        """Initializes the UserManager with a JSON file."""
        self._json_file = json_file
        self.user = self._load_user()

    def _load_user(self):
        """Loads user profile from the JSON file."""
        try:
            with open(self._json_file, 'r') as file:
                data = json.load(file)
                return User.from_dict(data)
        except FileNotFoundError:
            return None

    def save_user(self, user):
        """Saves the user profile back to the JSON file."""
        self.user = user
        with open(self._json_file, 'w') as file:
            json.dump(self.user.to_dict(), file, indent=4)

