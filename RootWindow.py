import random
import shutil
import tkinter as tk
from threading import Thread
from tkinter import ttk

import requests
from PIL import ImageTk, Image

from IGDBApiWrapper import IGDBApiWrapper

login_screen_labels = []
login_screen_entries = []
login_screen_buttons = []

label_names = ["IGDB client id", "IGDB client secret", ""]
button_names = ["Cancel", "Log in"]


# Method for evenly resizing labels in login screen.
def resize_all_labels(labels):
    label_width_list = [len(element) for element in labels]
    max_width = max(label_width_list)

    for label in login_screen_labels:
        label.config(width=max_width)


# Class for managing application windows.
def prepare_label_with_image(image_name, image_size):
    image = Image.open(image_name)
    image = image.resize(image_size, Image.ANTIALIAS)
    tkImage = ImageTk.PhotoImage(image)
    return tk.Label(image=tkImage, anchor='w')


class RootWindow:

    def __init__(self):
        self.root = None
        self.game = None
        self.api = None
        self.pb = None

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
            if index == 1:
                entry = tk.Entry(self.root, show="*")
            else:
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
        self.api = IGDBApiWrapper(oa_client_id=login_screen_entries[0].get(),
                                  oa_client_secret=login_screen_entries[1].get())

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

    def thread_task(self, name):
        self.game = self.api.get_game_info_by_name(name)
        if self.pb is not None:
            self.pb.stop()
        self.root.destroy()
        self.set_up_game_info_window()

    # Method searching for game by submitted name.
    def action_on_search(self, name):
        if self.api.can_download:
            if self.pb is not None:
                self.pb.start()

            print(f">>>>>>>>>> {name}")
            thread = Thread(target=self.thread_task, args=[name])
            thread.start()
            # self.game = self.api.get_game_info_by_name(name)
            # self.root.destroy()
            # self.set_up_game_info_window()
            # if self.pb is not None:
            #     self.pb.stop()
        else:
            print("Cannot download info, api not set up correctly.")

    # Display window in which user can type in name of game for searching.
    def set_up_search_window(self):
        self.root = tk.Tk()
        self.root.title("Type in game name:")

        entry = tk.Entry(self.root)
        entry.grid(row=0, column=2)

        self.pb = ttk.Progressbar(
            self.root,
            orient='horizontal',
            mode='indeterminate')
        self.pb.grid(row=0, column=4, columnspan=3, sticky=tk.W, pady=4)

        button = tk.Button(self.root, text="Search", command=lambda: self.action_on_search(entry.get()))
        button.grid(row=0, column=0, sticky=tk.W, pady=4)

        label = tk.Label(self.root, width=15, text="Enter game name", anchor='w')
        label.grid(row=0, column=1, sticky=tk.W, pady=4)

        self.root.mainloop()

    # Displays enlarged image after it was clicked.
    def enlarge_image_on_click(self, image_name):
        tempRoot = tk.Toplevel()
        image = Image.open(image_name)
        imageTk = ImageTk.PhotoImage(image)
        label = tk.Label(tempRoot, image=imageTk, anchor='w')
        label.grid(row=0, column=0, sticky=tk.W, pady=4, columnspan=1, rowspan=1)
        tempRoot.attributes('-topmost', False)
        tempRoot.mainloop()

    # Displays downloaded game info for user.
    def set_up_game_info_window(self):
        self.root = tk.Tk()
        self.root.title(self.game.name)
        screenshot_size = (250, 150)

        # Download cover image.
        self.download_image("cover.png", self.game.cover_url)

        # Display cover image.
        coverImage = Image.open("cover.png")
        coverImage = coverImage.resize((200, 300), Image.ANTIALIAS)
        tkImage = ImageTk.PhotoImage(coverImage)
        label = tk.Label(image=tkImage, anchor='w')
        label.grid(row=0, column=0, sticky=tk.W, pady=4, columnspan=1, rowspan=3)
        label.bind("<Button-1>", lambda e: self.enlarge_image_on_click("cover.png"))

        # Display text info.
        gameNameLabel = tk.Label(self.root, width=50, text=self.game.name, anchor='n')
        gameNameLabel.grid(row=0, column=1, sticky=tk.W, pady=4)

        gameDescriptionLabel = tk.Label(self.root, width=50, wraplength=250, text=self.game.summary, anchor='n')
        gameDescriptionLabel.grid(row=1, column=1, sticky=tk.W, pady=4)

        genres = "Genres:"
        for genre in self.game.genres:
            genres = f"{genres}, {genre}"

        gameGenresLabel = tk.Label(self.root, width=50, text=genres, anchor='n', wraplength=250,
                                   font='Helvetica 8 bold')
        gameGenresLabel.grid(row=2, column=1, sticky=tk.W, pady=4)

        # Download screenshots.
        self.download_three_random_screenshots()
        labels = []
        images = []

        for index in range(3):
            img = Image.open(f"screenshot_{index}.png")
            img = img.resize(screenshot_size, Image.ANTIALIAS)
            images.append(ImageTk.PhotoImage(img))

            if index == 1:
                labels.append(tk.Label(image=images[index], anchor='w'))
                labels[index].grid(row=3, column=index, sticky=tk.S, pady=4, columnspan=1, rowspan=1)
            else:
                labels.append(tk.Label(image=images[index], anchor='c'))
                labels[index].grid(row=3, column=index, sticky=tk.W, pady=4, columnspan=1, rowspan=1)

            labels[index].bind("<Button-1>", lambda e: self.enlarge_image_on_click(f"screenshot_{index}.png"))

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

    # Function for testing positioning of elements in window.
    def display_window_with_mock_data(self):
        self.root = tk.Tk()
        self.root.title("mock")
        screenshot_size = (250, 150)

        # Display cover image.
        coverImage = Image.open("cover.png")
        coverImage = coverImage.resize((200, 300), Image.ANTIALIAS)
        tkImage = ImageTk.PhotoImage(coverImage)
        label = tk.Label(image=tkImage, anchor='w')
        label.grid(row=0, column=0, sticky=tk.W, pady=4, columnspan=2, rowspan=3)
        label.bind("<Button-1>", lambda e: self.enlarge_image_on_click("cover.png"))

        gameNameLabel = tk.Label(self.root, width=50, text="Mass Effect 2", anchor='n')
        gameNameLabel.grid(row=0, column=1, sticky=tk.W, pady=4)

        gameDescriptionLabel = tk.Label(self.root, width=50, wraplength=250,
                                        text="Are you prepared to lose everything to save the galaxy? You'll need to be, Commander Shephard. It's time to bring together your greatest allies and recruit the galaxy's fighting elite to continue the resistance against the invading Reapers. So steel yourself, because this is an astronomical mission where sacrifices must be made. You'll face tougher choices and new, deadlier enemies. Arm yourself and prepare for an unforgettable intergalactic adventure.",
                                        anchor='n')
        gameDescriptionLabel.grid(row=1, column=1, sticky=tk.W, pady=4)

        gameGenresLabel = tk.Label(self.root, width=50, wraplength=250,
                                   text="Genre: Adventure, Role-playing (RPG), Shooter, Simulator", anchor='n')
        gameGenresLabel.grid(row=2, column=1, sticky=tk.W, pady=4)

        labels = []
        images = []

        for i in range(3):
            img = Image.open(f"screenshot_{i}.png")
            img = img.resize(screenshot_size, Image.ANTIALIAS)
            images.append(ImageTk.PhotoImage(img))

            if i == 1:
                labels.append(tk.Label(image=images[i], anchor='w'))
                labels[i].grid(row=3, column=i, sticky=tk.S, pady=4, columnspan=1, rowspan=1)
            else:
                labels.append(tk.Label(image=images[i], anchor='c'))
                labels[i].grid(row=3, column=i, sticky=tk.W, pady=4, columnspan=1, rowspan=1)

            labels[i].bind("<Button-1>", lambda e: self.enlarge_image_on_click(f"screenshot_{i}.png"))

        self.root.mainloop()

    # Default method for starting app, displays windows in correct order.
    def run(self):
        self.set_up_login_window()
