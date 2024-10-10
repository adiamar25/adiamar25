from ex11_utils import *
from boggle_board_randomizer import *
import tkinter as tk
from tkinter import messagebox
import time


def callback():
    print('Button has been clicked!')


def game_over():
    label_text = tk.Label(root, text="Game Over", font=(
        "Helvetica", 25), bg="Red", fg="Black")
    label_text.grid(row=5000, column=(2500))


def timer(time: str):
    timer_label = tk.Label(root, text=time, font=(
        "Helvetica", 25), bg="Blue", fg="White")
    timer_label.grid(row=1000, column=1000)
    full_seconds = 180
    min = int(time[0])
    sec1 = int(time[2])
    sec2 = int(time[-1])

    if min > 0 and sec1 == 0 and sec2 == 0:
        min, sec1, sec2 = min-1, 5, 9
    if min > 0 and sec1 > 0 and sec2 == 0:
        min, sec1, sec2 = min, sec1-1, 9
    if min > 0 and sec1 == 0 and sec2 > 0:
        min, sec1, sec2 = min, sec1, sec2-1
    new_time = str(min) + ":" + str(sec1) + str(sec2)
    timer_label.configure(text=new_time)
    return timer_label, new_time


def game_start():
    game_board = randomize_board()
    for row_ind in range(len(game_board)):
        for col_ind in range(len(game_board[0])):
            button = tk.Button(root, text=game_board[row_ind][col_ind], command=callback,
                               font=("Helvetica", 20), height=3, width=7, bg="Purple", fg="White")
            button.grid(row=row_ind, column=col_ind)
    # timer_label = tk.Label(root, text="3:00", font=(
    #    "Helvetica", 25), bg="Blue", fg="White")
    #timer_label.grid(row=1000, column=1000)
    label_score = tk.Label(root, text='Score:', font=(
        "Helvetica", 25), height=5, width=10, bg="Green", fg="White")
    label_score.grid(row=1000, column=4000)
    game_time, new_time = timer("3:00")


if __name__ == "__main__":
    root = tk.Tk()
    label_text = tk.Label(root, text='Boggle!', font=(
        "Helvetica", 25), height=5, width=10, bg="Blue", fg="White")
    label_text.grid(row=1000, column=3000)
    start_button = tk.Button(root, text="New Game", command=game_start,
                             font=("Helvetica", 22), height=5, width=10, bg="Red", fg="White")
    start_button.grid(row=1000, column=2000)

    root.after(180000, game_over)

    root.mainloop()
