import json
from pathlib import Path
import __main__


class Config():
    def __init__(self):
        # Modified flag used for check if saving is needed
        self.modified = False
        self.config_path = Path(__main__.__file__).parent.resolve() / "simple_manga_downloader_config.json"

        # Loads the config or creates the base one if not present
        if self.config_path.is_file():
            with open(self.config_path, "r") as f:
                config = json.load(f)
        else:
            self.modified = True
            config = {"manga_directory": self.config_path.parent / "Manga",
                      "tracking": {}}

        # Gets the useful data for easy access
        self.manga_directory = Path(config["manga_directory"])
        self.tracked_manga = config["tracking"]

        # Creates manga download folder if not present
        try:
            self.manga_directory.mkdir(parents=True)
        except FileExistsError:
            pass

    def add_tracked(self, Manga):
        '''Adds manga to the tracked list'''
        if Manga.series_title not in self.tracked_manga:
            self.tracked_manga[Manga.series_title] = Manga.manga_link
            self.modified = True
            print(f"Added to tracked:  {Manga.series_title}")
        else:
            print(f"Already tracked:  {Manga.series_title}")

    def remove_tracked(self, delete):
        '''Removes manga from the tracked list
        Accepts only a list as an argument'''
        to_remove = set()
        for n in delete:
            if n in self.tracked_manga:
                to_remove.add(n)
            elif "/" in n:
                for key, value in self.tracked_manga.items():
                    if value == n:
                        to_remove.add(key)
                        break
                else:
                    print("Link not found")
            else:
                try:
                    index = int(n)
                    if index > len(self.tracked_manga):
                        print("Number out of index")
                    to_remove.add(list(self.tracked_manga)[index - 1])
                except ValueError:
                    print("Not a index, link or title")

        for r in to_remove:
            del self.tracked_manga[r]
            print(f"Removed from tracked: {r}")
        if to_remove:
            self.modified = True

    def change_dir(self, dire):
        '''Changes the manga download directory'''
        self.manga_directory = Path(dire).resolve()
        self.modified = True

    def clear_tracked(self):
        '''Clears the tracked shows'''
        confirm = input("Are you sure you want to clear tracked manga? "
                        "[y to confirm/anything else to cancel]").lower()
        if confirm == "y":
            self.tracked_manga = {}
            self.modified = True
            print("Tracked cleared")

    def reset_config(self):
        '''Resets the config to the defaults'''
        confirm = input("Are you sure you want to reset the config file to the defaults? "
                        "[y to confirm/anything else to cancel]").lower()
        if confirm == "y":
            self.manga_directory = self.config_path.parent / "Manga"
            self.tracked_manga = {}
            self.modified = True
            print("Config was reset")

    def change_position(self):
        if len(self.tracked_manga) < 2:
            print("Less than 2 manga tracked")
            return
        self.list_tracked()

        try:
            select = int(input("Which manga do you want to move?: ")) - 1
        except ValueError:
            print("Not a number, aborting")
            return
        if select not in range(len(self.tracked_manga)):
            print("Number out of index range, aborting")
            return
        try:
            move_index = int(input("Where do you want to move it?: ")) - 1
        except ValueError:
            print("Not a number, aborting")
            return
        if move_index not in range(len(self.tracked_manga)):
            print("Number out of index range, aborting")
            return

        keys = list(self.tracked_manga)
        get = keys.pop(select)
        keys.insert(move_index, get)
        self.tracked_manga = dict([(k, self.tracked_manga[k]) for k in keys])

        self.modified = True
        print(f"Entry \"{get}\" moved to {move_index + 1}")

    def list_tracked(self):
        '''Lists the tracked manga'''
        if not self.tracked_manga:
            print("No shows tracked!")
            return
        print("\nCurrently tracked manga:")
        for n, link in enumerate(self.tracked_manga, 1):
            print(f"{n}. {link}")
        print()

    def save_config(self):
        config = {"manga_directory": str(self.manga_directory),
                  "tracking": self.tracked_manga}
        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=4)
