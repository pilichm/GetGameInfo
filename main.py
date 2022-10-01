import tkinter as tk

login_screen_labels = []
login_screen_entries = []
login_screen_buttons = []

label_names = ["IGDB client id", "IGDB client secret", ""]
button_names = ["Cancel", "Log in"]


def action_on_log_in():
    print("Verifying submitted credentials.")


def set_up_login_window():
    window = tk.Tk()
    window.title("Get game info - login.")

    # Add labels.
    for index, text in enumerate(label_names):
        label = tk.Label(window, width=15, text=text, anchor='w').grid(row=index)
        login_screen_labels.append(label)

    # Add text inputs.
    for index in range(2):
        entry = tk.Entry(window)
        entry.grid(row=index, column=1)
        login_screen_entries.append(entry)

    # Add buttons.
    for index, text in enumerate(button_names):
        if index == 0:
            button = tk.Button(window, text=text, command=window.quit).grid(row=3, column=index, sticky=tk.W, pady=4)
        elif index == 1:
            button = tk.Button(window, text=text, command=action_on_log_in()).grid(row=3, column=index, sticky=tk.W, pady=4)
        else:
            break

        login_screen_buttons.append(button)

    tk.Button(window, text='Log in', command=action_on_log_in).grid(row=3, column=1, sticky=tk.W, pady=4)

    window.mainloop()


if __name__ == '__main__':
    print("App - start.")

    set_up_login_window()

    print("App - end.")
