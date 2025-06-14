import tkinter as tk
from random_word import RandomWords
from tkinter import messagebox

randomWordGenerator = RandomWords()
word = randomWordGenerator.get_random_word()
wordList = []
index = 0
wpm = 0
characters_typed = 0

def generate_words():
    for n in range(1,5):
        word = randomWordGenerator.get_random_word()
        wordList.append(word)


def color_word_correct(word_index, correct):
    start_pos = 0
    for i in range(word_index):
        start_pos += len(wordList[i]) + 1

    start_index = f"1.{start_pos}"
    end_index = f"1.{start_pos + len(wordList[word_index])}"

    if correct:
        wordsBox.tag_remove("wrong", start_index, end_index)
        wordsBox.tag_add("correct", start_index, end_index)
    else:
        wordsBox.tag_add("wrong", start_index, end_index)

def send_word_function(event=None):
    global index
    global wpm
    global characters_typed
    userWord = user_input.get()
    if userWord == wordList[index]:
        print("Correct!")
        color_word_correct(index, True)
        index += 1
        characters_typed += len(userWord)
        user_input.set("")
        if index == len(wordList):
            print("All done!")
            wpm = characters_typed / 5
            wordList.clear()
            generate_words()
            wordsBox.delete('1.0', tk.END)
            wordsBox.insert(tk.END, ' '.join(wordList))
            index = 0
    else:
        print("Incorrect!")
        color_word_correct(index, False)
        user_input.set("")

def freeze_game():
    start_button.config(state="disabled")

    textInput.config(state="disabled")
    textInput.unbind("<Return>")
    response = messagebox.showinfo("Game Over", f"Time's up! Thanks for playing. Your WPM is {wpm}")
    messagebox.unbind("<Return>")
    print("Your WPM is " + str(wpm))

    if response == "ok":
        window.destroy()

def count_time(current=0):
    start_button.config(state="disabled")
    if current <= 60:
        timeTextBox.config(text=f"Time: {current}")
        window.after(1000, count_time, current + 1)
    else:
        freeze_game()


if __name__ == "__main__":

    window = tk.Tk()

    generate_words()

    window.title("Typing Test")
    window.minsize(600,600)

    label = tk.Label(window, text = "Typing Test ", font=('Arial', 16))
    label.pack(pady=20)

    timeTextBox = tk.Label(window, text="Time: 0")
    timeTextBox.pack( padx=5)

    wordsBox = tk.Text(window, height=5, width=52)
    wordsBox.pack(pady=20)
    wordsBox.insert(tk.END, ' '.join(wordList))
    wordsBox.tag_configure("correct", foreground="green")
    wordsBox.tag_configure("wrong", foreground="red")

    start_button = tk.Button(window, text="Start Timer", command=lambda: count_time(0))
    start_button.pack()

    user_input = tk.StringVar(window)
    textInput = tk.Entry(window, textvariable=user_input, width=50)
    textInput.pack(pady=20)
    textInput.bind("<Return>", send_word_function)

    window.mainloop()
