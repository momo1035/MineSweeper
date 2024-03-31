import random
from tkinter import *
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog

root = Tk()
root.withdraw()
class Cell:
    def __init__(self,row,colmun,typee="#",visibility=False,flaggad=False):
        self.row=row
        self.colmun=colmun
        self.typee=typee
        self.visibility=visibility
        self.flaggad=flaggad
    def show_cell(self):
        self.visibility=True
    def put_flag(self):
        self.flaggad=True
    def remove_flag(self):
        self.flaggad=False
class Board:
    def __init__(self,size,num):
        self.all_mines=num
        self.control=True
        self.size=size
        khaneha=[]
        for i in range(self.size):
            for j in range(self.size):
                khaneha.append((i,j))
        lst_min=[]
        for i in range(num):
            new_pos = random.choice(khaneha)
            khaneha.remove(new_pos)
            (row, col) = new_pos
            lst_min.append((row,col))
        self.board=[[None]*size]*size
        main_lst=[]
        for i in range(size):
            lst=[]
            for j in range(size):
                if (i,j) in lst_min:
                    cell=Cell(i,j,"@")
                    lst.append(cell)
                else:
                    cell=Cell(i,j)
                    lst.append(cell)
            main_lst.append(lst)
        self.board=main_lst

    def show_cell(self,row,colmun):
        if not self.board[row][colmun].visibility:
            self.board[row][colmun].show_cell()

            if self.board[row][colmun].typee=="@" and not self.board[row][colmun].flaggad:
                self.control=False


    def put_flag(self,row,colmun):
        if not self.board[row][colmun].visibility:
            self.board[row][colmun].put_flag()
            self.all_mines -=1
    def remove_flag(self,row,colmun):
        if not self.board[row][colmun].visibility and self.flaggad:
            self.board[row][colmun].remove_flag()
            self.all_mines +=1
    def counter(self,row,colmun):
        count=0
        for i in range(row-1,row+2):
            for j in range(colmun-1,colmun+2):
                if  0<= i < self.size and 0<= j <self.size:
                    if self.board[i][j].typee=="@":
                        count += 1
        return count
    def won(self):
        for row in range(self.size):
            for colmun in range(self.size):
                if self.board[row][colmun].typee=="#":
                        if  not (self.board[row][colmun].visibility):
                            return False
        return True
    # init board size and mines count

global flag,flag1
flag=True
flag1=False

def show_final(board,root):

    if board.won():
        for i in range(board.size):
            for j in range(board.size):
                if board.board[i][j].typee=="@":
                    cells[i][j]["bg"]="red"
                    cells[i][j]["state"]=DISABLED
                else:
                    cells[i][j]["bg"]="green"
                    cells[i][j]["state"]=DISABLED
    if not board.control:
        for i in range(board.size):
            for j in range(board.size):
                if board.board[i][j].typee=="@":
                    cells[i][j]["bg"]="red"
                cells[i][j]["state"]=DISABLED
    root.grab_set()
flag=True
global time
time=0

def click_cell(row, col,board,master):

    ''' Handle clicking on a cell.
        If it is a mine, finish the game; player will loose.
        If it has a flag, do nothing.
        Otherwise, show the number of mines around the cell.
    '''
    global flag
    if flag:
        def time_counter():
            global time
            time_label['text'] = time
            if not board.control:
                return
            if board.won():
                return
            time = time +  1
            time_label.after(1000, time_counter)
            time_label['text'] = time
        time_counter()
        flag=False
    if board.won() or not board.control:
        return
    board.show_cell(row,col)
    if  not board.board[row][col].flaggad and board.board[row][col].typee=="@" :
        cells[row][col]["state"]=DISABLED
        cells[row][col]["text"]=" @ "
    else:
       if board.board[row][col].visibility:
        cells[row][col]["state"]=DISABLED
        if board.counter(row,col)==0:
             cells[row][col]["text"]="   "
             cells[row][col]["bg"]="lightgreen"
        else:
            cells[row][col]["text"]=board.counter(row,col)
            cells[row][col]["bg"]="lightgreen"
    if board.won():
        messagebox.showinfo("You win!", "You win!")
        show_final(board,root)
    if not board.control:
        messagebox.showinfo("You lose!", "You lose!")
        show_final(board,root)
    if board.counter(row,col) ==0 :
               for i in range(row-1,row+2):
                    for j in range(col-1,col+2):
                        if  0<= i < board.size and 0<= j <board.size and  not board.board[i][j].visibility:
                                click_cell(i,j,board,master)
    flag=False


def toggle_flag(row, col,board,master):
    if board.won() or not board.control:
        return False
    if not board.board[row][col].visibility and not board.board[row][col].flaggad:
            board.board[row][col].put_flag()
            board.all_mines -=1
            cells[row][col]["text"]="p"
            mines_label['text'] = board.all_mines
    elif not board.board[row][col].visibility and board.board[row][col].flaggad:
            board.board[row][col].remove_flag()
            board.all_mines +=1
            cells[row][col]["text"]="   "
            mines_label['text'] = board.all_mines

cells=[]
global size
def init_gui(master,size,board):
    ''' Initialize the graphical user interface '''
    global mines_label, mines_count, time_label
    global time

    master.title('Minesweeper')
    master.minsize(size * 30 + 40, size * 30 + 70)

    frame = Frame(master)
    frame.grid(padx = 30, pady = 30)

    for i in range(size):
        cells.append([])

    for i in range(size):
        for j in range(size):
            cell = Button(frame, text = '     ', bg = '#DDDDDD',height=1,width=3)
            cell.config(anchor = CENTER)
            cell.grid(row = i, column = j, sticky = 'nswe')
            cells[i].append(cell)

            def left_click_handler(event, row = i, col = j):
                click_cell(row, col,board,master)

            def right_click_handler(event, row = i, col = j):
                toggle_flag(row, col,board,master)

            cell.bind('<Button-3>', right_click_handler)
            cell.bind('<Button-1>', left_click_handler)

    remainings = Label(frame, text = 'Mines: ')
    remainings.grid(row = size + 1, column = 1, columnspan = 2, pady = 10)

    mines_label = Label(frame, text = board.all_mines)
    mines_label.grid(row = size + 1, column = 3, pady = 0)

    timer = Label(frame, text = 'Time :')
    timer.grid(row = size + 2, column = 1, columnspan = 2, pady = 0)

    time_label = Label(frame, text = '0')
    time_label.grid(row = size + 2, column = 3, pady = 0)

    master.deiconify()

def main():
    ''' The main entry of the game '''
    board_size = simpledialog.askinteger('Minesweeper', 'Please Enter board size', parent = root)
    mines_count = simpledialog.askinteger('Minesweeper', 'Please Enter mines number', parent = root)
    board=Board(board_size,mines_count)

    init_gui(root,board_size,board)
    root.mainloop()


# Entry Point
main()



