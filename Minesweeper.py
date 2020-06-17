from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from random import randint


class buttons(Frame):

	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent
		self.pack
		self.make_board()

	def make_board(self):
		self.counter = Label(root,text="Bombs Left To Find:\n{}".format(bombs))
		self.counter.grid(row=0,column=boardsize)

		self.instructions1 = Label(root,text="Instructions:",font="bold")
		self.instructions1.grid(row=2,column=boardsize)

		self.instructions2 = Label(root,text="Click to sweep\nfor bombs!")
		self.instructions2.grid(row=3,column=boardsize)

		self.instructions3 = Label(root,text="Right click to mark\na square with a flag.")
		self.instructions3.grid(row=4,column=boardsize)

		self.instructions4 = Label(root,text="Flag all the\nbombs to win...")
		self.instructions4.grid(row=5,column=boardsize)

		self.instructions5 = Label(root,text="...but one click on\na bomb and it's all over!")
		self.instructions5.grid(row=6,column=boardsize)

		event=0
		for r in range(boardsize):
			buttonlist.append([])
			for c in range(boardsize):
				self.btn = Button(root, command=lambda r=r, c=c : sweep(r,c),
					borderwidth=2, height=1, width=2, font=("Courier New", "15"))
				self.btn.grid(row=r, column=c)
				self.btn.bind("<Button-3>", lambda event=event, r=r, c=c: flag(event,r,c))

				buttonlist[r].append([self.btn,False,False,0])  # button, is exploded/safe,
														# has a flag, number of close bombs
		buttonlist.append(self.counter)


def flag(event,r, c):
	if buttonlist[r][c][1] == False:
		if buttonlist[r][c][2] == False:  # no flag there
			buttonlist[r][c][0].config(bg="red")
			buttonlist[r][c][2] = True
			playerboard[r][c] = True

			if playerboard == bombboard:
				messagebox.showinfo(title="Congratulations!", message="   You won!   ")
				replay()

		elif buttonlist[r][c][2] == True:  # there is a flag, get rid of it
			buttonlist[r][c][0].config(bg=root["bg"])
			buttonlist[r][c][2] = False
			playerboard[r][c] = "Empty"

		bombsfound = sum([l.count(True) for l in playerboard])
		buttonlist[-1].config(text="Bombs Left To Find:\n{}".format(bombs-bombsfound))

	
def sweep(r,c):
	global bombboard
	mined = sum([l.count(False) for l in playerboard])
	if mined == 0:  # we want to make sure you don't hit a bomb the first time
		done = False
		while done == False:
			num_close_bombs = 0
			for j in range(max(0,r-1),min(r+2,boardsize)):
				for k in range(max(0,c-1),min(c+2,boardsize)):
					if bombboard[j][k] == True:
						num_close_bombs += 1
			if num_close_bombs > 0:
				bombboard = [[False for j in range(boardsize)] for k in range(boardsize)]

				bombcount = 0
				while bombcount < bombs:
					x = randint(0,boardsize-1)
					y = randint(0,boardsize-1)
					if bombboard[x][y] == False:
						bombboard[x][y] = True
						bombcount += 1
			else:
				done = True

		# initializing the correct bomb counts
		for rtemp in range(boardsize):
			for ctemp in range(boardsize):
				num_close_bombs = 0
				for j in range(max(0,rtemp-1),min(rtemp+2,boardsize)):
					for k in range(max(0,ctemp-1),min(ctemp+2,boardsize)):
						if j != rtemp or k != ctemp:
							if bombboard[j][k] == True:
								num_close_bombs += 1
				buttonlist[rtemp][ctemp][3] = num_close_bombs

	if buttonlist[r][c][2] == False:
		if not bombboard[r][c]:    # no bomb
			if buttonlist[r][c][3] != 0:
				buttonlist[r][c][0].config(bg="light green", text=buttonlist[r][c][3])
			else:
				buttonlist[r][c][0].config(bg="light green")
			playerboard[r][c] = False
		else:   # bomb
			buttonlist[r][c][0].config(bg="black")
			buttonlist[r][c][0].flash()

			for r in range(boardsize):
				for c in range(boardsize):
					if bombboard[r][c]:
						buttonlist[r][c][0].config(bg="black")

			messagebox.showwarning(title="A Bomb Exploded!", message="You have lost...")
			replay()

		buttonlist[r][c][1] = True

		if buttonlist[r][c][3] == 0:
			for indices in [[max(0,r-1),c],[r,max(0,c-1)],[r,min(c+1,boardsize-1)],
					[min(r+1,boardsize-1),c]]:
				j, k = indices[0], indices[1]
				if buttonlist[j][k][1] != True:
					sweep(j,k)
		if playerboard == bombboard:
			messagebox.showinfo(title="Congratulations!", message="   You won!   ")
			replay()


def replay():
	ans = messagebox.askyesno(title="Replay", message="Would you like to play again?")
	if ans == True:
		root.destroy()
		start()
		quit()
	else:
		root.destroy()
		quit()


def start():
	global root
	root = Tk()

	root.title("Minesweeper")
	frame = Frame(root)
	

	global buttonlist
	buttonlist = []

	global boardsize
	#boardsize=10
	boardsize = int(simpledialog.askfloat("Boardsize", "The board will be square. How many blocks wide do you want it to be?",
		initialvalue=10, minvalue=10, maxvalue=15))

	global bombs
	#bombs=10
	bombs = int(simpledialog.askfloat(title="Bombs Number", prompt="How many bombs do you want on the field?", initialvalue=10,
		minvalue=10, maxvalue=boardsize))

	global playerboard
	playerboard = [["Empty" for j in range(boardsize)] for k in range(boardsize)]

	global bombboard
	bombboard = [[False for j in range(boardsize)] for k in range(boardsize)]

	bombcount = 0
	while bombcount < bombs:
		x = randint(0,boardsize-1)
		y = randint(0,boardsize-1)
		if bombboard[x][y] == False:
			bombboard[x][y] = True
			bombcount += 1	

	app = buttons(parent=root)
	app.mainloop()


start()