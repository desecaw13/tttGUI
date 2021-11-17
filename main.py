
from tkinter import *
import tkinter.messagebox as messagebox
from random import randrange


# handles a tkinter Button, its clicked command and a StringVar value that is the value of the button's text
class cButton:
    # creates an instance and its button and its value
    def __init__(self, parent):
        self.parent = parent
        self.value = StringVar(parent)
        self.button = Button(parent, textvariable=self.value, command=self.clicked, width=2, height=1)

    # sets the value if it's empty then handles computers turn if singleplayer
    def clicked(self):
        if self.value.get():
            return False
        else:
            self.value.set('X' if turn.get() % 2 == 0 else 'O')
            changeTurn(self.parent.master)
            if mode and turn.get() % 2 != 0:
                for w in self.parent.children.values():  # disables all buttons in board (parent is their frame in game)
                    w['state'] = DISABLED

                # function for parent.after()
                def move():
                    for w in self.parent.children.values():  # activates those buttons
                        w['state'] = ACTIVE
                    computerTurn()

                self.parent.after(375, move)  # sleep for .375 seconds then moves
            return True


# adds 1 to turn and checks for wins and handles them
def changeTurn(window):
    turn.set(turn.get() + 1)
    winner = hasWon()
    if winner:
        openWin(winner)
        turn.trace_remove('write', window.cbn)
        window.destroy()


# makes random moves until one is valid
def computerTurn():
    if not hasWon():
        if not board[randrange(0, len(board))][randrange(0, len(board))].clicked():
            computerTurn()


# determines if someone won and who
def hasWon():
    for s in ('X', 'O'):
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


# the win screen: displays who won
def openWin(winner):
    root.withdraw()

    win = Toplevel(root, bg='#808080')
    win.title('Game Over')
    win.grid_columnconfigure(0, weight=1)
    win.minsize(root.winfo_screenwidth()//5, root.winfo_screenheight()//5)

    Label(win, bg='#F8F8F8', relief=SOLID, bd=1, text='There was a tie.' if winner == 'Tie' else f'{winner} won the game.')\
        .grid(ipadx=3, ipady=3, padx=5, pady=5, sticky=EW)

    # brings user back to root window
    def back():
        root.deiconify()
        turn.set(0)
        win.destroy()
    Button(win, bg='#F0B070', activebackground='#FFBF7F', relief=FLAT, text='Back to menu', command=back)\
        .grid(ipadx=3, ipady=3, padx=5, pady=5)

    win.focus_force()


# the game screen: displays the buttons in board
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
    board = [[cButton(outer) for _ in range(size)] for __ in range(size)]  # creates the 2d list
    for x in range(size):
        for y in range(size):
            outer.grid_columnconfigure(x, weight=1)
            outer.grid_rowconfigure(y, weight=1)
            board[x][y].button.grid(row=x, column=y, sticky=NSEW)  # puts the buttons on the screen and makes then scale with the window

    foot = Frame(game, bg='#808080')
    foot.grid_columnconfigure(1, weight=1)
    foot.grid(padx=5, pady=5, sticky=EW)

    t_l = Label(foot, text="X's turn", bg='#F8F8F8')
    t_l.grid(sticky=W)
    game.cbn = turn.trace_add('write', lambda *args: t_l.config(text=f"{'X' if turn.get() % 2 == 0 else 'O'}'s turn"))
    # ^ keeps track of who's turn it is and displays that

    Frame(foot, bg='#808080').grid(row=0, column=1, padx=2)

    # brings user back to root window
    def back():
        root.deiconify()
        turn.set(0)
        turn.trace_remove('write', game.cbn)
        game.destroy()
    Button(foot, bg='#F0B070', activebackground='#FFBF7F', relief=FLAT, text='Back to menu', command=back)\
        .grid(row=0, column=2, ipadx=3, ipady=3, sticky=E)

    game.focus_force()


# the start
def openStart():
    root.withdraw()

    start = Toplevel(root, bg='#808080')
    start.title('Starting...')
    start.grid_columnconfigure(0, weight=1)
    start.grid_rowconfigure(0, weight=1)
    start.minsize(root.winfo_screenwidth()//6, root.winfo_screenheight()//6)

    f = Frame(start, bg='#808080')
    f.grid()

    size = IntVar(start)
    Entry(f, bg='#F8F8F8', textvariable=size).grid(row=0, column=1, ipadx=1, ipady=1, padx=5, pady=5)
    Label(f, bg='#F8F8F8', text='Size of game \n(3 to 9)').grid(row=0, column=0, ipadx=1, ipady=1, padx=5, pady=5)

    # validates input for size and it's Entry, then begins the game
    def play():
        try:  # handles error for input
            size.set(max(min(size.get(), 9), 3))  # enforces a 3-9 size limit
            openGame(size.get())
            start.destroy()
        except TclError:
            messagebox.showerror('Bad Input', 'Use a number.')
    Button(f, bg='#70B0F0', activebackground='#7FBFFF', relief=FLAT, text='Start game', command=play)\
        .grid(ipadx=3, ipady=3, padx=3, pady=3, columnspan=2)

    # brings user back to root window
    def back():
        root.deiconify()
        start.destroy()
    Button(f, bg='#F0B070', activebackground='#FFBF7F', relief=FLAT, text='Back to menu', command=back)\
        .grid(ipadx=3, ipady=3, padx=3, pady=3, columnspan=2)

    start.focus_force()


if __name__ == '__main__':
    board = []  # makes board global

    mode = False  # true is multiplayer

    root = Tk()
    root.config(bg='#808080')
    root.title('Noughts and Crosses')
    root.grid_columnconfigure(0, weight=1)
    root.minsize(root.winfo_screenwidth()//4, root.winfo_screenheight()//4)

    Label(root, bg='#F8F8F8', text='Tic Tac Toe').grid(ipadx=1, ipady=1, padx=5, pady=5, sticky=EW)

    turn = IntVar(root)

    # sets the mode and starts the next window
    def begin(m):
        global mode
        mode = m
        openStart()
    Button(root, bg='#70B0F0', activebackground='#7FBFFF', relief=FLAT, text='Single player', command=lambda: begin(True))\
        .grid(ipadx=3, ipady=3, padx=3, pady=3)
    Button(root, bg='#70B0F0', activebackground='#7FBFFF', relief=FLAT, text='Multiplayer', command=lambda: begin(False))\
        .grid(ipadx=3, ipady=3, padx=3, pady=3)

    Button(root, bg='#F0B070', activebackground='#FFBF7F', relief=FLAT, text='Exit', command=root.destroy)\
        .grid(ipadx=3, ipady=3, padx=3, pady=3)

    root.mainloop()
