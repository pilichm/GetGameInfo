class Game:
    def __init__(self, name):
        self.screenshots = []
        self.genres = []
        self.cover_url = ""
        self.name = name
        self.summary = ""

    def to_string(self):
        print("\n")
        print(f"name: {self.name}")
        print(f"summary: {self.summary}")
        print(f"cover url: {self.cover_url}")
        print(f"genres: {self.genres}")
        print(f"Screenshots: {self.screenshots}")
        print("\n")
