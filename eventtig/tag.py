class Tag:
    def __init__(self):
        pass

    def load_from_yaml_data(self, id, data):
        self.title = data.get("title")
        self.id = id
        self.extra = data.get("extra", {})

    def load_from_database_row(self, data):
        self.title = data["title"]
        self.id = data["id"]

    def get_api_json_contents(self):
        return {
            "id": self.id,
            "title": self.title,
        }
