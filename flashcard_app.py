#Author Tania Akter Rahima
#gre_flashcard_app
import tkinter as tk
import csv
import random

#for storing  known words I use this
known_words = set()

# Load words from CSV by category.
# there are three types of categories - easy, medium, hard
#newline='': Prevents blank lines between rows when reading.
#encoding='utf-8': Ensures it reads non-English characters properly.

def load_words(selected_category):
    with open("gre_words.csv", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        word_list = [
            row for row in reader    #enumerate(..., 1) adds line numbers starting from 1.
                                     #i is the line number, and row is the current row as a dictionary.
            if row["Category"].strip().lower() == selected_category.lower()
        ]

        return word_list



def filter_words_by_category(category):
    return [word for word in all_words if word["Category"] == category]

# for cancel timer
def cancel_timer():
    global timer_id
    if timer_id is not None:
        root.after_cancel(timer_id)
        timer_id = None

# Show next card on the display
def next_card():
    global current_word, word_index, timer_id, words

    cancel_timer()


    if not words:
        word_label.config(text="Well done! 🎉")
        meaning_label.config(text="You've reviewed all words.")
        disable_buttons()
        return

    if shuffle_enabled.get():
        current_word = random.choice(words) # random word is picked from the list.
    else:
        if word_index >= len(words):
            word_label.config(text="Well done! 🎉")
            meaning_label.config(text="You've reviewed all words.")
            disable_buttons()
            return
        current_word = words[word_index]
        word_index += 1  # to move to the next one next time.

#Displays the new word on the screen.
    print(current_word)
    word_label.config(text=current_word["Word"])
    meaning_label.config(text="")

    timer_id = root.after(5000, mark_unknown)  # I use root.after() to run a function after a delay.

# Disable all buttons
def disable_buttons():
    show_button.config(state=tk.DISABLED)
    know_button.config(state=tk.DISABLED)
    dont_know_button.config(state=tk.DISABLED)

# Show the meaning of the word
def show_meaning():
    cancel_timer()
    meaning_label.config(text=current_word["Meaning"])

# If "I Know" is clicked, increase score
def mark_known():
    global score
    cancel_timer()

    word_text = current_word["Word"]

    if word_text not in known_words:
        known_words.add(word_text)
        score += 1
        score_label.config(text=f"Score: {score}")

    next_card()


# If "I Don't Know" is clicked
def mark_unknown():
    cancel_timer()
    next_card()

# When category is changed
def update_category(event=None):
    global words, word_index, score
    selected_category_local = category_var.get()
    words = load_words(selected_category_local)
    word_index = 0
    score = 0
    score_label.config(text="Score: 0")
    next_card()



# ===== UI Setup =====
root = tk.Tk()
root.title("GRE Flashcard App")
root.geometry("480x480")
root.config(bg="#2e2e2e")


# Load all words once to extract categories
with open("gre_words.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile) #reads each row as a dictionary
    all_words = list(reader)

categories = sorted(set(word["Category"].strip().lower() for word in all_words if word["Category"].strip()))
category_var = tk.StringVar()
category_var.set(categories[0])
selected_category = category_var.get()
words = load_words(selected_category)

words.clear()
current_word = {}
word_index = 0
score = 0
timer_id = None

# Category dropdown menu
categories = sorted(set(word["Category"] for word in all_words))
category_var = tk.StringVar(value=categories[0])
category_menu = tk.OptionMenu(root, category_var, *categories, command=update_category)
category_menu.config(font=("Helvetica", 12), bg="white")
category_menu.pack(pady=10)

# Shuffle mode toggle
shuffle_enabled = tk.BooleanVar(value=True)
shuffle_check = tk.Checkbutton(root, text="Shuffle Mode", variable=shuffle_enabled,
                               bg="#2e2e2e", fg="white", selectcolor="#2e2e2e",
                               font=("Helvetica", 12))
shuffle_check.pack(pady=5)


# Word display
word_label = tk.Label(root, text="", font=("Helvetica", 24), bg="#2e2e2e", fg="white")
word_label.pack(pady=20)

# Score display
meaning_label = tk.Label(root, text="", font=("Helvetica", 16), bg="#2e2e2e", fg="lightgreen")
meaning_label.pack()

# Score display
score_label = tk.Label(root, text="Score: 0", font=("Helvetica", 14), bg="#2e2e2e", fg="orange")
score_label.pack(pady=5)

# Buttons
button_frame = tk.Frame(root, bg="#2e2e2e")
button_frame.pack(pady=20)

# button for display meaning
show_button = tk.Button(button_frame, text="Show Meaning", command=show_meaning, width=15)
show_button.grid(row=0, column=0, padx=5)

# for ' I know ' button
know_button = tk.Button(button_frame, text="I Know", command=mark_known, width=15, bg="green", fg="white")
know_button.grid(row=0, column=1, padx=5)

#for ' I don't know' button
dont_know_button = tk.Button(button_frame, text="I Don't Know", command=mark_unknown, width=15, bg="red", fg="white")
dont_know_button.grid(row=0, column=2, padx=5)


# Load first category and show a word
update_category()


# Start app
root.mainloop()

