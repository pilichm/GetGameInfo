import tkinter as tk
from tkinter import ttk
import requests
import shutil
import random

from PIL import ImageTk, Image
from IGDBApiWrapper import IGDBApiWrapper

login_screen_labels = []
login_screen_entries = []
login_screen_buttons = []

label_names = ["IGDB client id", "IGDB client secret", ""]
button_names = ["Cancel", "Log in"]

pb = None

# Method for evenly resizing labels in login screen.
def resize_all_labels(labels):
    label_width_list = [len(element) for element in labels]
    max_width = max(label_width_list)

    for label in login_screen_labels:
        label.config(width=max_width)


# Class for managing application windows.
class RootWindow:

    def __init__(self):
        self.root = None
        self.game = None
        self.api = None

    # Displays log in screen.
    def set_up_login_window(self):
        self.root = tk.Tk()
        self.root.title("Get game info - login.")

        # Add labels.
        for index, text in enumerate(label_names):
            label = tk.Label(self.root, width=15, text=text, anchor='w')
            login_screen_labels.append(label)
            login_screen_labels[index].grid(row=index)

        resize_all_labels(label_names)

        # Add text inputs.
        for index in range(2):
            entry = tk.Entry(self.root)
            entry.grid(row=index, column=1)
            login_screen_entries.append(entry)

        # Add buttons.
        for index, text in enumerate(button_names):
            if index == 0:
                button = tk.Button(self.root, text=text, command=lambda: self.root.quit)
            elif index == 1:
                button = tk.Button(self.root, text=text, command=lambda: self.action_on_log_in())
            else:
                break

            button.grid(row=3, column=index, sticky=tk.W, pady=4)
            login_screen_buttons.append(button)

        self.root.mainloop()

    def action_on_log_in(self):
        print("Verifying submitted credentials.")
        self.api = IGDBApiWrapper(oa_client_id=login_screen_entries[0].get(), oa_client_secret=login_screen_entries[1].get())

        if self.api.can_download:
            print("API created.")
            result_desc = self.api.get_or_refresh_auth_token()

            if result_desc is not None and result_desc != "":
                login_screen_labels[2].config(text=result_desc, fg="#F00")
                new_labels_list = label_names[:-1]
                new_labels_list.append(result_desc)
                resize_all_labels(new_labels_list)
            else:
                self.root.destroy()
                self.set_up_search_window()
        else:
            login_screen_labels[2].config(text="Missing oa_client_id or oa_client_secret!", fg="#F00")
            new_labels_list = label_names[:-1]
            new_labels_list.append("Missing oa_client_id or oa_client_secret!")
            resize_all_labels(new_labels_list)

    # Method searching for game by submitted name.
    def action_on_search(self, name):
        if self.api.can_download:
            if pb is not None:
                pb.start()
            self.game = self.api.get_game_info_by_name(name)
            self.root.destroy()
            self.set_up_game_info_window()
            if pb is not None:
                pb.stop()
        else:
            print("Cannot download info, api not set up correctly.")

    # Display window in which user can type in name of game for searching.
    def set_up_search_window(self):
        self.root = tk.Tk()
        self.root.title("Type in game name:")

        entry = tk.Entry(self.root)
        entry.grid(row=0, column=2)

        button = tk.Button(self.root, text="Search", command=lambda: self.action_on_search(entry.get()))
        button.grid(row=0, column=0, sticky=tk.W, pady=4)

        label = tk.Label(self.root, width=15, text="Enter game name", anchor='w')
        label.grid(row=0, column=1, sticky=tk.W, pady=4)

        pb = ttk.Progressbar(
            self.root,
            orient='horizontal',
            mode='indeterminate')
        pb.grid(row=0, column=4, columnspan=3, sticky=tk.W, pady=4)

        self.root.mainloop()

    # Displays downloaded game info for user.
    def set_up_game_info_window(self):
        self.root = tk.Tk()
        self.root.title(self.game.name)


        # Download cover image.
        self.download_image("cover.png", self.game.cover_url)

        # Display cover image.
        coverImage = Image.open("cover.png")
        coverImage = coverImage.resize((200, 300), Image.ANTIALIAS)
        tkImage = ImageTk.PhotoImage(coverImage)
        label = tk.Label(image=tkImage, anchor='w')
        label.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=4)

        # Display text info.

        # Download screenshots.
        self.download_three_random_screenshots()

        screenshot_labels = []
        # Display screenshots.
        for index in range(3):
            screenshotImage = Image.open(f"screenshot_{index}.png")
            screenshotImage = screenshotImage.resize((200, 100), Image.ANTIALIAS)
            sLabel = tk.Label(image=ImageTk.PhotoImage(screenshotImage))
            screenshot_labels.append(sLabel)
            screenshot_labels[index].grid(row=1, column=index)

        self.root.mainloop()


    # Downloads images from submitted url.
    def download_image(self, img_name, img_url):
        print(f"http:{self.game.cover_url}")
        response = requests.get(f"http:{img_url}", stream=True)

        with open(img_name, 'wb') as file:
            shutil.copyfileobj(response.raw, file)

    # Download max three screenshots of all available.
    def download_three_random_screenshots(self):
        for index, img_url in enumerate(random.sample(self.game.screenshots, 3)):
            self.download_image(f"screenshot_{index}.png", img_url)

    # Default method for starting app, displays windows in correct order.
    def run(self):
        self.set_up_login_window()
