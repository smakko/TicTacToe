from tkinter import *
import time
import random

class Board(Frame):
	def __init__(self,master,*args,**kwargs):
		Frame.__init__(self,master,bg='black',height=300)
		self.master=master
		self.widgets()

	def widgets(self):
		self.buttons=[]
		gx=0
		gy=0
		for i in range(9):
			#Create buttons
			button='button'+str(i)
			self.buttons.append(button)
			self.buttons[i]=Button(self,width=6,height=3,bg='white',command=lambda i=i: self.rules(i))#,command=lambda i=i: self.master.disp.out(str(i)))
		for button in self.buttons:
			#Button placement
			if gx==3:
				gy+=1
				gx=0
			button.grid(row=gy,column=gx)
			gx+=1

		#Create list of active buttons
		self.free_buttons=[button for button in range(0,9)]
		print('Free buttons:',self.free_buttons)

	def rules(self,*args):
		def scan():
			#ROWS
			for i in range(0,9,3):
				if self.buttons[i]['text']==self.buttons[i+1]['text']==self.buttons[i+2]['text']=='X':
					return 'usr'
				if self.buttons[i]['text']==self.buttons[i+1]['text']==self.buttons[i+2]['text']=='O':
					return 'bot'
			#COLUMNS
			for i in range(0,3):
				if self.buttons[i]['text']==self.buttons[i+3]['text']==self.buttons[i+6]['text']=='X':
					return 'usr'
				if self.buttons[i]['text']==self.buttons[i+3]['text']==self.buttons[i+6]['text']=='O':
					return 'bot'
			#DIAGONALS
			if self.buttons[0]['text']==self.buttons[4]['text']==self.buttons[8]['text']=='X':
				return 'usr'
			if self.buttons[2]['text']==self.buttons[4]['text']==self.buttons[6]['text']=='O':
				return 'bot'
			return None

		button_id=args[0]
		self.free_buttons.remove(button_id)
		self.buttons[button_id].config(state='disabled',text='X')
		print('You\'ve pressed',button_id)

		if scan()==None:
			if self.free_buttons:
				while True:
					bot=random.randint(0,8)
					if bot in self.free_buttons:
						print('Bot pressed',bot)
						self.free_buttons.remove(bot)
						self.buttons[bot].config(state='disabled',text='O')
						break
			else:
				print('draw')
				self.master.disp.out('Draw')
				self.master.after(1500,self.master.reset)

		elif scan()=='usr':
			self.master.usr_score+=1
			self.master.disp.out('You won!')
			self.master.after(1500,self.master.reset)
		elif scan()=='bot':
			self.master.bot_score+=1
			self.master.disp.out('Game over!')
			self.master.after(1500,self.master.reset)

		print('Free buttons:',self.free_buttons)

class Display(Frame):
	def __init__(self,master,*args,**kwargs):
		Frame.__init__(self,master,bg='white',height=30)
		self.master=master
		self.widgets()
		self.out('You {}:{} Bot'.format(self.master.usr_score,self.master.bot_score))
	def widgets(self):
		self.text=Label(self)
		self.text.pack()
	def out(self,*args):
		self.text['text']=args[0]


class App(Frame):
	def __init__(self,master,*args,**kwargs):
		Frame.__init__(self,master)
		self.master=master

		self.usr_score=0
		self.bot_score=0

		self.properties()
		self.elements()

	def elements(self):
		self.disp=Display(self)
		self.disp.pack(side='top',fill='x',expand=True)

		self.board=Board(self)
		self.board.pack(fill='both',expand=True)

	def reset(self):
		self.disp.destroy()
		self.board.destroy()
		self.elements()

	def properties(self):
		root=self.master
		root.title('Tic Tac Toe')
		root.option_add("*Background",'white')
		root.option_add('*Label.Font',('Lucida Sans',10,'bold'))
		root.option_add('*Button.Font',('Lucida Sans',20,'bold'))
		root.iconbitmap('assets/icon.ico')
		#root.geometry('300x330')
		root.resizable(False,False)


if __name__ == '__main__':
	root=Tk()
	App(root).pack(side='top',expand=True,fill='both')
	root.mainloop()
