import json

class Configuration:
    def __init__(self, filename):
        self.filename = filename
        self.reload_config()

    def reload_config(self):
        self.config = None
        data = open(self.filename)
        self.config = json.load(data)

    def get_database_location(self):
        return self.config['databaselocation']

    def get_fetch_limit(self):
        return self.config['fetch_limit']