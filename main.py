# Joe Olpin
# GUI Tic Tac Toe
# 9/9-/2012

from tkinter import *
from random import randrange


class cButton:
    def __init__(self, parent):
        self.parent = parent
        self.value = StringVar(parent)
        self.button = Button(parent, textvariable=self.value, command=self.clicked, width=2, height=1)

    def clicked(self):
        if self.value.get():
            return False
        else:
            self.value.set('X' if turn.get() % 2 == 0 else 'Y')
            changeTurn(self.parent.master)
            if mode and turn.get() % 2 != 0:
                computerTurn()
            return True


def changeTurn(window):
    turn.set(turn.get() + 1)
    winner = hasWon()
    if winner:
        openWin(winner)
        window.destroy()


def computerTurn():
    # todo fix sometimes opens two won toplevels when multiplayer and???
    if not board[randrange(0, len(board))][randrange(0, len(board))].clicked() and not hasWon():
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

    win = Toplevel(root, bg='#808080')
    win.title('Game Over')
    win.minsize(root.winfo_screenwidth()//4, root.winfo_screenheight()//4)

    Label(win, bg='#F8F8F8', text='There was a tie.' if winner == 'Tie' else f'{winner} won the game.').grid()

    def back():
        root.deiconify()
        turn.set(0)
        win.destroy()
    Button(win, text='Back to menu', command=back).grid(ipadx=3, ipady=3, padx=1, pady=1)

    win.focus_force()


def openGame(size):
    root.withdraw()

    game = Toplevel(root, bg='#808080')
    game.title('Playing')
    game.grid_columnconfigure(0, weight=1)
    game.grid_rowconfigure(0, weight=1)
    game.minsize(120, 120)

    outer = Frame(game)
    outer.grid(padx=5, pady=5, sticky=NSEW)

    # setup
    global board
    board = [[cButton(outer) for _ in range(size)] for __ in range(size)]
    for x in range(size):
        for y in range(size):
            outer.grid_columnconfigure(x, weight=1)
            outer.grid_rowconfigure(y, weight=1)
            board[x][y].button.grid(row=x, column=y, sticky=NSEW)

    foot = Frame(game, bg='#808080')
    foot.grid(padx=5, pady=5)

    Label(foot, bg='#F8F8F8', text='Turns:').grid()
    Label(foot, bg='#F8F8F8', textvariable=turn).grid(row=0,  column=1)

    Frame(foot, bg='#808080').grid(row=0, column=2, padx=2)

    def back():
        root.deiconify()
        game.destroy()
    Button(foot, text='Back to menu', command=back).grid(row=0, column=3, ipadx=3, ipady=3)

    game.focus_force()


def openStart():
    root.withdraw()

    start = Toplevel(root, bg='#808080')
    start.title('Starting...')
    start.minsize(root.winfo_screenwidth()//6, root.winfo_screenheight()//6)

    size = IntVar(start)
    Entry(start, bg='#F8F8F8', textvariable=size).grid(row=0, column=1, ipadx=1, ipady=1, padx=5, pady=5)
    Label(start, bg='#F8F8F8', text='Size of game \n(3 to 9)').grid(row=0, column=0, ipadx=1, ipady=1, padx=5, pady=5)

    def play():
        # todo size limit of 3 - 9. warning if odd?
        openGame(size.get())
        start.destroy()
    Button(start, text='Start game', command=play).grid(ipadx=3, ipady=3, padx=1, pady=1, columnspan=2)

    def back():
        root.deiconify()
        start.destroy()
    Button(start, text='Back to menu', command=back).grid(ipadx=3, ipady=3, padx=1, pady=1, columnspan=2)

    start.focus_force()


if __name__ == '__main__':
    board = []  # makes board global

    mode = False  # true is multiplayer

    root = Tk()
    root.config(bg='#808080')
    root.title('Noughts and Crosses')
    root.grid_columnconfigure(0, weight=1)
    root.minsize(root.winfo_screenwidth()//4, root.winfo_screenheight()//4)

    # todo colors and all, check everything for everything

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
# todo make comments
