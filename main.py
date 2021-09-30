import tkinter as tk
from tkinter import messagebox
from functools import partial
import random
from pygame import mixer


class Hangman(tk.Tk):
    def __init__(self):
        super().__init__()

        self.my_font = ("tkDefaultFont", 18)
        self.init_ui()
        self.audio = Audio()

        with open('word_list.txt', 'r') as f:
            self.words = f.read().strip().split('\n')

        self.run = False
        self.guesses = 0
        self.word = None
        self.board = []
        self.muted = False

    def init_ui(self):
        self.title('Hangman')
        self.iconbitmap('images/icon.ico')
        self.resizable(False, False)
        self.config(bg='#3F88C5')
        self.noose_states = [tk.PhotoImage(file='images/stage0.png'), tk.PhotoImage(file='images/stage1.png'),
                             tk.PhotoImage(file='images/stage2.png'), tk.PhotoImage(file='images/stage3.png'),
                             tk.PhotoImage(file='images/stage4.png'), tk.PhotoImage(file='images/stage5.png'),
                             tk.PhotoImage(file='images/stage6.png'), tk.PhotoImage(file='images/stage7.png'),
                             tk.PhotoImage(file='images/stage8.png'), tk.PhotoImage(file='images/stage9.png')]

        self.win_lbl = tk.Label(self, text='Welcome to Hangman', bg='#3F88C5', fg='white', font=self.my_font)
        self.win_lbl.grid(row=0, column=0, columnspan=9, padx=5, pady=5)

        self.noose_lbl = tk.Label(self, image=self.noose_states[0], bg='#3F88C5')
        self.noose_lbl.grid(row=1, column=0, columnspan=9, padx=5, pady=5)

        self.board_lbl = tk.Label(self, text='', bg='#3F88C5', fg='white', font=self.my_font)
        self.board_lbl.grid(row=2, column=0, columnspan=9, padx=5, pady=5)

        self.letter_btns = [tk.Button(self, text=char, command=partial(self.guess, char), font=self.my_font, height=1, width=4) for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']

        self.a_on = tk.PhotoImage(file='images/audioOn.png')
        self.a_off = tk.PhotoImage(file='images/audioOff.png')
        self.audio_btn = tk.Button(self, image=self.a_on, bg='#3F88C5', bd=0, command=self.mute_audio)
        self.audio_btn.grid(row=0, column=8, sticky=tk.NE, padx=5, pady=5)

        for i, b in enumerate(self.letter_btns):
            c = i % 9
            r = (i - c) // 9 + 4
            b.grid(row=r, column=c)
            b.config(state=tk.DISABLED, bg='#393e41')

        reset_btn = tk.Button(self, text='New', bg='#E94F37', command=self.new_game, font=self.my_font, height=1, width=4)
        reset_btn.grid(row=6, column=8)

    def mute_audio(self):
        if self.muted:
            self.muted = False
            for sound in self.audio.all_sounds:
                mixer.Sound.set_volume(sound, 1)
            self.audio_btn.config(image=self.a_on)
        else:
            self.muted = True
            for sound in self.audio.all_sounds:
                mixer.Sound.set_volume(sound, 0)
            self.audio_btn.config(image=self.a_off)

    def new_game(self):
        if not self.run:
            self.reset()
            return

        again = messagebox.askyesno(title='test', message='Are you sure you want to restart the game?')
        if again:
            self.reset()

    def reset(self):
        for b in self.letter_btns:
            b.config(state=tk.NORMAL, bg='#44BBA4')

        self.run = True
        self.guesses = 0
        self.get_word()
        self.setup_board()
        self.win_lbl.config(text='Pick a letter')
        self.board_lbl.config(text=self.str_board())
        self.noose_lbl.config(image=self.noose_states[self.guesses])

    def guess(self, guess):
        widget = self.letter_btns['ABCDEFGHIJKLMNOPQRSTUVWXYZ'.index(guess)]

        if guess in self.word:
            for count, char in enumerate(self.word):
                if guess == char:
                    self.board[count] = self.word[count]

            if not self.has_won():
                self.audio.correct.play()

        else:
            self.guesses += 1

            if not self.has_lost():
                self.audio.incorrect.play()

        self.noose_lbl.config(image=self.noose_states[self.guesses])
        self.board_lbl.config(text=self.str_board())

        widget.config(state=tk.DISABLED, bg='#393E41')

        self.check_win_lose()

    def check_win_lose(self):
        if self.has_won():
            self.audio.win.play()

            self.win_lbl.config(text='You win!')
            for b in self.letter_btns:
                b.config(state=tk.DISABLED)
            self.run = False

        if self.has_lost():
            self.audio.lose.play()

            self.win_lbl.config(text=f'You lost. The word was {self.word}')
            for b in self.letter_btns:
                b.config(state=tk.DISABLED)
            self.run = False

    def get_word(self):
        self.word = random.choice(self.words).upper()

    def setup_board(self):
        self.board = ['_'] * len(self.word)

    def has_won(self):
        return '_' not in self.board

    def has_lost(self):
        return self.guesses >= 9

    def str_board(self):
        b = ''
        for char in self.board:
            if char == '_':
                b += ' '
            b += char
            if char == '_':
                b += ' '
        return b


class Audio:
    def __init__(self):
        mixer.init()
        self.win = mixer.Sound('audio/youWin.wav')
        self.lose = mixer.Sound('audio/gameOver.wav')
        self.correct = mixer.Sound('audio/correct.wav')
        self.incorrect = mixer.Sound('audio/incorrect.wav')
        self.all_sounds = (self.win, self.lose, self.correct, self.incorrect)


if __name__ == '__main__':
    game = Hangman()
    game.mainloop()
