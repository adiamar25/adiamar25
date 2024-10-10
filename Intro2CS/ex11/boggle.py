#################################################################
# FILE : boggle.py
# WRITERS : Adi Amar, adi.amar1, 315244624,
#           Benjamin Teitler, benjamin.t, 328966346
# EXERCISE : intro2cs1 ex11 2023
# DESCRIPTION: A simple program that makes Boggle game by GUI
# STUDENTS I DISCUSSED THE EXERCISE WITH: Nobody
# WEB PAGES I USED: None
# NOTES: Nothing special
#################################################################

#################################################################
############################ IMPORTS ############################
#################################################################

from ex11_utils import *
from boggle_board_randomizer import *
import tkinter as tk

#################################################################
############################# CODE ##############################
#################################################################


class Game:

    def __init__(self):
        """ Initialaizing the board """

        self.__words = open("boggle_dict.txt").read().split("\n")
        self.__root = tk.Tk()
        self.__root.geometry("800x800")
        self.__root.title("Boggle")

        # title label
        self.__text_label = self.title_label()

        # the top frame, contains the "start" button, the timer label
        # and the score label
        self.__time_left = "3:00"
        self.__score = "score: 0"
        top_frame = self.configure_top_frame()
        self.__start_button = self.configure_start_button(top_frame)
        self.__timer_label = self.configure_timer_label(top_frame)
        self.__score_label = self.configure_score_label(top_frame)
        top_frame.pack(fill="x")

        # a frame shows the current word the user is choosing
        self.__curr_word = "current word: "
        curr_word_frame = self.configure_current_word_frame()
        self.__curr_word_label = self.configure_current_word_label(
            curr_word_frame)

        # a frame shows all the words the user has already found
        self.__words_found = "words found: "
        words_found_frame = self.configure_words_found_frame()
        self.__words_found_label = self.configure_words_found_label(
            words_found_frame)

        # initiate the board frame
        self.__game_board = randomize_board()
        self.__curr_loc = (0, 0)
        self.__path = []
        self.__board_frame = self.configure_board_frame()

        # a "game over" message and a "play again" button
        self.__game_over_label = tk.Label(
            self.__root, text="Game Over!", font=("Helvetica", 28))
        self.__play_again_button = tk.Button(self.__root, text="play again",
                                             command=self.game_start,
                                             font=("Helvetica", 20))

        # Delete and enter buttons
        self.__delete_and_enter_frame = self.configure_del_and_en_frame()
        self.__delete_and_enter_buttons = self.delete_and_enter_buttons()

    def title_label(self) -> tk.Label:
        """ Making the title label. """
        text_label = tk.Label(self.__root, text="Boggle!",
                              font=("Helvetica", 18))
        text_label.pack(padx=20, pady=20)
        return text_label

    def configure_top_frame(self) -> tk.Frame:
        """ Configurate the top frame of the board.
            this frame contains the "start" button, 
            the "timer" label and the "score" label. """
        top_frame = tk.Frame(self.__root)
        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=1)
        top_frame.columnconfigure(2, weight=1)
        return top_frame

    def configure_start_button(self, top_frame) -> tk.Button:
        """ Configure the start button. """
        start_button = tk.Button(top_frame, text="Start",
                                 command=self.game_start,
                                 font=("Helvetica", 20))
        start_button.grid(row=0, column=0, sticky=tk.W+tk.E)
        return start_button

    def configure_score_label(self, top_frame) -> tk.Label:
        """ Configure the score label. """
        score_label = tk.Label(
            top_frame, text=self.__score, font=("Helvetica", 20))
        score_label.grid(row=0, column=2, sticky=tk.W+tk.E)
        return score_label

    def configure_timer_label(self, top_frame) -> tk.Label:
        """ Configure the timer label. """
        timer_label = tk.Label(
            top_frame, text=self.__time_left, font=("Helvetica", 20))
        timer_label.grid(row=0, column=1, sticky=tk.W+tk.E)
        return timer_label

    def configure_current_word_frame(self) -> tk.Frame:
        """ Configure the current word frame, which
            contains the "current word" label, that 
            shows the current word the user is choosing. """
        curr_word_frame = tk.Frame(self.__root)
        curr_word_frame.pack(fill="x")
        return curr_word_frame

    def configure_current_word_label(self, curr_word_frame) -> tk.Label:
        """ Configure the current word label. """
        curr_word_label = tk.Label(
            curr_word_frame, text=self.__curr_word,
            font=("Helvetica", 20))
        curr_word_label.grid(row=5, column=0, sticky=tk.W+tk.E)
        return curr_word_label

    def configure_words_found_label(self, words_found_frame) -> tk.Label:
        """ Configure the words found frame, which
            contains the "words found" label, that 
            shows all the valid words the user has found. """
        words_found_label = tk.Label(
            words_found_frame, text=self.__words_found,
            font=("Helvetica", 20))
        words_found_label.grid(row=10, column=0, sticky=tk.W+tk.E)
        return words_found_label

    def configure_words_found_frame(self) -> tk.Frame:
        """ Configure the words found label. """
        words_found_frame = tk.Frame(self.__root)
        words_found_frame.pack(fill="x")
        return words_found_frame

    def configure_board_frame(self) -> tk.Frame:
        """ Configure the board frame, which contains all the buttons
            of the game board. """
        board_frame = tk.Frame(self.__root)
        board_frame.columnconfigure(0, weight=1)
        board_frame.columnconfigure(1, weight=1)
        board_frame.columnconfigure(2, weight=1)
        board_frame.columnconfigure(3, weight=1)
        return board_frame

    def configure_del_and_en_frame(self):
        delete_and_enter_frame = tk.Frame(self.__root)
        delete_and_enter_frame.columnconfigure(0, weight=1)
        delete_and_enter_frame.columnconfigure(1, weight=1)
        return delete_and_enter_frame

    def game_start(self):
        """ A function that actually starts the game.
            when clicked on "start" button or "play again" button,
            it randomize a game board and initiate the countdown. also, 
            it destroy the "start" button after clicked. """
        self.__start_button.destroy()
        self.__time_left = "3:00"
        self.timer()
        self.__root.after(181100, self.play_again)
        self.__game_over_label.pack_forget()
        self.__play_again_button.pack_forget()
        self.__score_label.configure(text=self.__score)
        self.__game_board = randomize_board()
        for row_ind in range(len(self.__game_board)):
            for col_ind in range(len(self.__game_board[0])):
                #self.__curr_loc = (row_ind, col_ind)
                loc = (row_ind, col_ind)
                button_text = self.__game_board[row_ind][col_ind]
                button = tk.Button(self.__board_frame,
                                   text=button_text,
                                   font=("Helvetica", 20), height=3,
                                   width=3)
                button.configure(fg="Black", command=lambda i=loc,
                                 j=button: self.add_char(i, j))

                button.grid(row=row_ind, column=col_ind, sticky=tk.W+tk.E)
        self.__board_frame.pack(fill="x")
        self.__delete_and_enter_frame.pack(fill="x")

    def delete_and_enter_buttons(self):
        #delete_and_enter_frame = tk.Frame(self.__root)
        #delete_and_enter_frame.columnconfigure(0, weight=1)
        #delete_and_enter_frame.columnconfigure(1, weight=1)
        delete_button = tk.Button(self.__delete_and_enter_frame, text="Delete",
                                  font=("Helvetica", 20), height=1,
                                  width=7, fg="Black", command=self.delete_command)
        delete_button.grid(row=0, column=0, sticky=tk.W+tk.E)
        enter_button = tk.Button(self.__delete_and_enter_frame, text="Enter",
                                 font=("Helvetica", 20), height=1,
                                 width=7, fg="Black",
                                 command=self.enter_command)
        enter_button.grid(row=0, column=1, sticky=tk.W+tk.E)
        # delete_and_enter_frame.pack(fill="x")

    def delete_command(self):
        self.__path = self.__path[:-1]
        self.__curr_word = "current word: " + \
            build_word(self.__game_board, self.__path)
        self.__curr_word_label.configure(text=self.__curr_word)

    def enter_command(self):
        if (self.__curr_word[14:] in self.__words
                and self.__curr_word[14:] not in self.__words_found):
            self.__words_found += self.__curr_word[14:] + ", "
            self.__curr_word = self.__curr_word[:14]
            self.__curr_word_label.configure(text=self.__curr_word)
            self.__words_found_label.configure(text=self.__words_found)
            self.update_score()
        self.__path = []
        self.__curr_word = "current word: "
        self.__curr_word_label.configure(text=self.__curr_word)

    def play_again(self):
        """ A function that announce when the game is over,
            and give a chance for another game, by packing
            "play again" button. """
        self.__delete_and_enter_frame.pack_forget()
        self.__game_over_label.pack()
        self.__play_again_button.pack()
        self.__score = "score: 0"
        self.__curr_word = "current word: "
        self.__words_found = "words found: "
        self.__curr_word_label.configure(text=self.__curr_word)
        self.__words_found_label.configure(text=self.__words_found)
        self.__path = []

    def timer(self):
        """ A function that updates the timer of the game"""
        if self.__time_left == "0:00":
            self.__timer_label.configure(text="0:00")
        else:
            self.__timer_label.after(1000, self.timer)
            self.__timer_label.configure(text=self.__time_left)
            # print(self.__time_left)
            min = int(self.__time_left[0])
            sec1 = int(self.__time_left[2])
            sec2 = int(self.__time_left[-1])
            min, sec1, sec2 = self.change_time(min, sec1, sec2)
            self.__time_left = str(min) + ":" + str(sec1) + str(sec2)

    def change_time(self, min: int, sec1: int, sec2: int) -> Tuple:
        """ A helper function for the timer() function.
            this function return a string contains the the time remain. """
        if min > 0:
            if sec1 == 0 and sec2 == 0:
                min, sec1, sec2 = min-1, 5, 9
            elif sec1 > 0 and sec2 == 0:
                min, sec1, sec2 = min, sec1-1, 9
            elif sec2 > 0:
                min, sec1, sec2 = min, sec1, sec2-1
        else:
            if sec2 > 0:
                min, sec1, sec2 = min, sec1, sec2-1
            elif sec1 > 0 and sec2 == 0:
                min, sec1, sec2 = min, sec1-1, 9
        return min, sec1, sec2

    def add_char(self, loc, button: tk.Button):
        """ A function that recieve an event, and derive its text.
            the text is the char appears on the clicked button, from which
            the event has been driven.
            than, the function confugure the "curr_word_label" so it 
            adds this char to the end of the current text shows there. """
        if self.__time_left != "0:00":
            self.__path += is_valid_click(self.__path, loc)
            self.__curr_word = "current word: " + \
                build_word(self.__game_board, self.__path)
            self.__curr_word_label.configure(text=self.__curr_word)

    def update_score(self):
        """ A function that update the score if the chosen button
            created a legal path. """
        if is_valid_path(self.__game_board, self.__path, self.__words) != None:
            self.__score = int(self.__score[7:])
            self.__score += (len(self.__path) ** 2)
            self.__score = "score: " + str(self.__score)
            self.__score_label.configure(text=self.__score)
            self.__path = []

    def run(self):
        """ The function that runs the game by entering the event loop. """
        self.__root.mainloop()


if __name__ == '__main__':
    boggle = Game()
    boggle.run()
