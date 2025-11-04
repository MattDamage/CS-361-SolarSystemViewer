import json
import os


# The goal of this class is to provide simple functionality for bookmark handling
class BookmarkManager:
    def __init__(self, filepath="data/bookmarks.json"):
        self.filepath = filepath
        self.bookmarks = self.load_bookmarks()

    def load_bookmarks(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def save_bookmarks(self):
        with open(self.filepath, "w") as f:
            json.dump(self.bookmarks, f, indent=2)

    def add_bookmark(self, name):
        if name not in self.bookmarks:
            self.bookmarks.append(name)
            self.save_bookmarks()

    def remove_bookmark(self, name):
        if name in self.bookmarks:
            self.bookmarks.remove(name)
            self.save_bookmarks()

    def list_bookmarks(self):
        return self.bookmarks
