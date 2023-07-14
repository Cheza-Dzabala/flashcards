import random
from tkinter import *

import pandas
from pandas import *

BACKGROUND_COLOR = "#B1DDC6"
FONT = "Arial"
translations = []
words_to_learn = []
LANGUAGE = "French"
timer = None
current_word = {}


# ---------------------------- Load Flash Cards ------------------------------- #
def flip_card(item):
    window.after_cancel(timer)
    english = item['English']
    canvas.itemconfig(canvas_image, image=back_image)
    canvas.itemconfig(translation_language, text="English", fill="white")
    canvas.itemconfig(translation_text, text=F"{english}", fill="white")


def copy():
    words_data_frame = pandas.read_csv("./data/french_words.csv")
    new_csv = pandas.DataFrame(words_data_frame)
    new_csv.to_csv('./data/words_to_learn.csv', index=FALSE)
    load_new_word()


def load_new_word():
    global current_word
    global translations
    global timer

    try:
        words_data_frame = pandas.read_csv("./data/words_to_learn.csv")
    except FileNotFoundError:
        copy()
    else:
        if len(words_data_frame) == 0:
            copy()
        else:
            translations = words_data_frame.to_dict(orient="records")
            item = translations[random.randint(0, len(translations))]
            current_word = item
            word = item["French"]
            canvas.itemconfig(translation_text, text=F"{word}", fill="black")
            canvas.itemconfig(canvas_image, image=front_image)
            canvas.itemconfig(translation_language, text="French", fill="black")
            timer = window.after(3000, flip_card, item)


def word_correct():
    words_data_frame = pandas.read_csv("./data/words_to_learn.csv")
    dict_words = words_data_frame.to_dict(orient="records")
    dict_words.remove(current_word)
    new_csv = pandas.DataFrame(dict_words)
    new_csv.to_csv("./data/words_to_learn.csv",  index=FALSE)
    load_new_word()


# ---------------------------- Layout ------------------------------- #

window = Tk()
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50, width=1000, height=1000)

canvas = Canvas()
front_image = PhotoImage(file="./images/card_front.png")
back_image = PhotoImage(file="./images/card_back.png")
canvas_image = canvas.create_image(500, 300, image=front_image)
canvas.config(width=1000, height=600, highlightthickness=0, bg=BACKGROUND_COLOR)
translation_language = canvas.create_text(500, 130, fill="black", text="French", font=(FONT, 40, "italic"))
translation_text = canvas.create_text(500, 250, fill="black", text="French", font=(FONT, 60, "bold"))
canvas.grid(column=1, row=1, columnspan=2)

button_wrong = Button(command=load_new_word)
button_wrong_image = PhotoImage(file="./images/wrong.png")
button_wrong.config(image=button_wrong_image, bg=BACKGROUND_COLOR, highlightthickness=0, border=0, borderwidth=0)
button_wrong.grid(column=1, row=2)

button_right = Button(command=word_correct)
button_right_image = PhotoImage(file="./images/right.png")
button_right.config(image=button_right_image, bg=BACKGROUND_COLOR, highlightthickness=0, border=0, borderwidth=0)
button_right.grid(column=2, row=2)

load_new_word()

window.mainloop()
