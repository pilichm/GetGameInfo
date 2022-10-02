import tkinter as tk

from IGDBApiWrapper import IGDBApiWrapper

login_screen_labels = []
login_screen_entries = []
login_screen_buttons = []

label_names = ["IGDB client id", "IGDB client secret", ""]
button_names = ["Cancel", "Log in"]


def resize_all_labels(labels):
    label_width_list = [len(element) for element in labels]
    max_width = max(label_width_list)

    for label in login_screen_labels:
        label.config(width=max_width)


def action_on_log_in():
    print("Verifying submitted credentials.")
    api = IGDBApiWrapper(oa_client_id=login_screen_entries[0].get(), oa_client_secret=login_screen_entries[1].get())

    if api.can_download:
        print("API created.")
        result_desc = api.get_or_refresh_auth_token()

        if result_desc is not None and result_desc != "":
            login_screen_labels[2].config(text=result_desc, fg="#F00")
            new_labels_list = label_names[:-1]
            new_labels_list.append(result_desc)
            resize_all_labels(new_labels_list)
    else:
        login_screen_labels[2].config(text="Missing oa_client_id or oa_client_secret!", fg="#F00")
        new_labels_list = label_names[:-1]
        new_labels_list.append("Missing oa_client_id or oa_client_secret!")
        resize_all_labels(new_labels_list)


def set_up_login_window():
    window = tk.Tk()
    window.title("Get game info - login.")

    # Add labels.
    for index, text in enumerate(label_names):
        label = tk.Label(window, width=15, text=text, anchor='w')
        login_screen_labels.append(label)
        login_screen_labels[index].grid(row=index)

    resize_all_labels(label_names)

    # Add text inputs.
    for index in range(2):
        entry = tk.Entry(window)
        entry.grid(row=index, column=1)
        login_screen_entries.append(entry)

    # Add buttons.
    for index, text in enumerate(button_names):
        if index == 0:
            button = tk.Button(window, text=text, command=lambda: window.quit)
        elif index == 1:
            button = tk.Button(window, text=text, command=lambda: action_on_log_in())
        else:
            break

        button.grid(row=3, column=index, sticky=tk.W, pady=4)
        login_screen_buttons.append(button)

    tk.Button(window, text='Log in', command=action_on_log_in).grid(row=3, column=1, sticky=tk.W, pady=4)

    window.mainloop()


if __name__ == '__main__':
    print("App - start.")

    # set_up_login_window()

    print("App - end.")
