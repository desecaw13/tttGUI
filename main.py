# Joe Olpin
# GUI Tic Tac Toe
# 9/9-/2012

from tkinter import *
from random import randrange


class cButton:
    def __init__(self, parent):
        self.parent = parent
        self.value = StringVar(parent)
        self.button = Button(parent, textvariable=self.value, command=self.clicked)

    def clicked(self):
        if self.value.get():
            return False
        else:
            self.value.set('X' if turn.get() % 2 == 0 else 'Y')
            changeTurn(self.parent.master)
            if mode and turn.get() % 2 != 0:
                computerTurn()
            # todo update tkinter widgets
            return True


def changeTurn(window):
    turn.set(turn.get() + 1)
    winner = hasWon()
    if winner:
        openWin(winner)
        window.destroy()
    # todo update widgets


def computerTurn():
    if not board[randrange(0, len(board))][randrange(0, len(board))].clicked() and not hasWon():  # opens two won ?
        computerTurn()


def hasWon():
    for s in ('X', 'Y'):
        for x in range(len(board)):
            for y in range(len(board)):
                if board[x][y].value.get() != s:
                    break
                if y == len(board)-1:
                    return s

        for y in range(len(board)):
            for x in range(len(board)):
                if board[x][y].value.get() != s:
                    break
                if x == len(board)-1:
                    return s

        for i in range(len(board)):
            if board[i][i].value.get() != s:
                break
            if i == len(board)-1:
                return s

        for i in range(len(board)):
            if board[i][(len(board)-1)-i].value.get() != s:
                break
            if i == len(board)-1:
                return s

    if turn.get() >= len(board) ** 2:
        return 'Tie'

    return False


def openWin(winner):
    root.withdraw()

    win = Toplevel(root)
    # start.title('todo') details, add widgets

    Label(win, text=winner).grid()

    def back():
        root.deiconify()
        turn.set(0)
        win.destroy()
    Button(win, text='Back to menu', command=back).grid()

    win.focus_force()


def openGame(size):
    root.withdraw()

    game = Toplevel(root)
    # game.title('todo') details, add widgets
    game.grid_columnconfigure(0, weight=1)
    game.grid_rowconfigure(0, weight=1)

    outer = Frame(game)
    outer.grid(sticky=EW+NS)

    # setup
    global board
    board = [[cButton(outer) for _ in range(size)] for __ in range(size)]
    for x in range(size):
        for y in range(size):
            outer.grid_columnconfigure(x, weight=1)
            outer.grid_rowconfigure(y, weight=1)
            board[x][y].button.grid(row=x, column=y, sticky=EW+NS)  # todo start as squares

    # testing thing for later
    foot = Frame(game)
    foot.grid()
    Label(foot, text='test').grid()

    def back():
        root.deiconify()
        game.destroy()
    Button(foot, text='Back to menu', command=back).grid(row=0, column=1)

    game.focus_force()


def openStart():
    root.withdraw()

    start = Toplevel(root)
    # start.title('todo') details, add widgets

    size = IntVar(start)  # empty? root?
    Entry(start, textvariable=size).grid()  # todo set limits of 3 - 9, odd?

    def play():
        openGame(size.get())
        start.destroy()
    Button(start, text='Start game', command=play).grid()

    def back():
        root.deiconify()
        start.destroy()
    Button(start, text='Back to menu', command=back).grid()

    start.focus_force()


if __name__ == '__main__':
    board = []  # makes board global

    mode = False  # true is multiplayer

    root = Tk()
    root.title('Noughts and Crosses')
    root.config(bg='#808080')
    root.grid_columnconfigure(0, weight=1)
    root.minsize(root.winfo_screenwidth()//4, root.winfo_screenheight()//4)

    # todo colors and all

    Label(root, bg='#F8F8F8', text='Tic Tac Toe').grid(ipadx=1, ipady=1, padx=5, pady=5, sticky=EW)

    turn = IntVar(root)

    def begin(m):
        global mode
        mode = m
        openStart()
    Button(root, text='Single player', command=lambda: begin(False)).grid(ipadx=3, ipady=3, padx=1, pady=1)
    Button(root, text='Multiplayer', command=lambda: begin(True)).grid(ipadx=3, ipady=3, padx=1, pady=1)

    Button(root, text='Exit', command=root.destroy).grid(ipadx=3, ipady=3, padx=1, pady=1)

    root.mainloop()
