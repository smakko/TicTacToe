from tkinter import *
import time
import random

class Board(Frame):
	def __init__(self,master,mode,*args,**kwargs):
		Frame.__init__(self,master,bg='black',height=300)
		self.master=master
		self.mode=mode

		self.current_player=True
		# current_player is used only in multi mode
		
		master.option_add('*Button.Font',('Lucida Sans',20,'bold'))
		
		self.widgets()

	def widgets(self):
		self.buttons=[]
		gx=0
		gy=0
		for i in range(9):
			#Create buttons
			button='button'+str(i)
			self.buttons.append(button)
			self.buttons[i]=Button(self,width=6,height=3,bg='white',command=lambda i=i: self.rules(self.mode,i))#,command=lambda i=i: self.master.disp.out(str(i)))
		for button in self.buttons:
			#Button placement
			if gx==3:
				gy+=1
				gx=0
			button.grid(row=gy,column=gx)
			gx+=1

		#Create list of active buttons
		self.free_buttons=[button for button in range(0,9)]
		# print('Free buttons:',self.free_buttons)

	def rules(self,mode,*args):
		def scan():
			#ROWS
			for i in range(0,9,3):
				if self.buttons[i]['text']==self.buttons[i+1]['text']==self.buttons[i+2]['text']=='X':
					return 'player1'
				if self.buttons[i]['text']==self.buttons[i+1]['text']==self.buttons[i+2]['text']=='O':
					return 'player2'
			#COLUMNS
			for i in range(0,3):
				if self.buttons[i]['text']==self.buttons[i+3]['text']==self.buttons[i+6]['text']=='X':
					return 'player1'
				if self.buttons[i]['text']==self.buttons[i+3]['text']==self.buttons[i+6]['text']=='O':
					return 'player2'
			#DIAGONALS
			if self.buttons[0]['text']==self.buttons[4]['text']==self.buttons[8]['text']:
				if self.buttons[0]['text']=='X':
					return 'player1'
				elif self.buttons[0]['text']=='O':
					return 'player2'
			if self.buttons[2]['text']==self.buttons[4]['text']==self.buttons[6]['text']:
				if self.buttons[2]['text']=='X':
					return 'player1'
				elif self.buttons[2]['text']=='O':
					return 'player2'
			return None
		if mode=='solo':
			#Defining pressed button
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
					self.master.after(1500,lambda:self.master.reset('solo'))

			if scan()=='player1':
				self.master.player1_score+=1
				self.master.disp.out('You won!')
				self.master.after(1500,lambda:self.master.reset('solo'))
			elif scan()=='player2':
				self.master.player2_score+=1
				self.master.disp.out('You lose!')
				self.master.after(1500,lambda:self.master.reset('solo'))

			print('Free buttons:',self.free_buttons)
		elif mode=='multi':
			button_id=args[0]
			self.free_buttons.remove(button_id)
			if self.current_player==True:
				self.buttons[button_id].config(state='disabled',text='X')
			else:
				self.buttons[button_id].config(state='disabled',text='O')
			self.current_player= not self.current_player

			if scan()==None:
				if not self.free_buttons:
					print('draw')
					self.master.disp.out('Draw')
					self.master.after(1500,lambda:self.master.reset('multi'))

			if scan()=='player1':
				self.master.player1_score+=1
				self.master.disp.out('Player 1 won!')
				self.master.after(1500,lambda:self.master.reset('multi'))
			elif scan()=='player2':
				self.master.player2_score+=1
				self.master.disp.out('Player 2 won!')
				self.master.after(1500,lambda:self.master.reset('multi'))

class Display(Frame):
	def __init__(self,master,mode,*args,**kwargs):
		Frame.__init__(self,master,bg='white',height=30)
		self.master=master
		self.mode=mode
		self.widgets()

		if mode=='solo':
			self.out('You {}:{} Bot'.format(self.master.player1_score,self.master.player2_score))
		elif mode=='multi':
			self.out('Player 1 {}:{} Player 2'.format(self.master.player1_score,self.master.player2_score))

	def widgets(self):
		self.text=Label(self)
		self.text.pack()
	def out(self,*args):
		self.text['text']=args[0]

class Lobby(Frame):
	def __init__(self,master,*args,**kwargs):
		Frame.__init__(self,master,height=100,width=210)
		self.master=master

		master.option_add('*Button.Font',('Consolas',10,))


		self.widgets()
	def widgets(self):
		self.label=Label(self,text='Select mode:')
		self.label.place(x=35,y=10)

		self.solo=Button(self,text='Player vs Bot',command=lambda: self.master.select_mode('solo'),borderwidth=0)
		self.solo.place(x=50,y=40)

		self.multi=Button(self,text='Player vs Player',command=lambda: self.master.select_mode('multi'),borderwidth=0)
		self.multi.place(x=50,y=65)

class App(Frame):
	def __init__(self,master,*args,**kwargs):
		Frame.__init__(self,master)
		self.master=master

		self.player1_score=0
		self.player2_score=0

		self.properties()

		#lobby
		self.lobby=Lobby(self)
		self.lobby.pack(fill='both',expand=True)

	def select_mode(self,*args):
		mode=args[0]
		self.lobby.destroy()
		self.disp=Display(self,mode=mode)
		self.disp.pack(side='top',fill='x',expand=True)

		self.board=Board(self,mode=mode)
		self.board.pack(fill='both',expand=True)

	def reset(self,mode):
		self.disp.destroy()
		self.board.destroy()
		self.select_mode(mode)

	def properties(self):
		master=self.master
		master.title('Tic Tac Toe')
		master.option_add("*Background",'white')

		master.option_add('*Label.Font',('Lucida Sans',15,'bold'))
		# master.iconbitmap('assets/icon.ico')
		# master.geometry('300x330')
		master.resizable(False,False)


if __name__ == '__main__':
	master=Tk()
	App(master).pack(side='top',expand=True,fill='both')
	master.mainloop()

'''
	NOTE!
	The only way to change button bg color in MacOs
	is highlightbackground='color'
'''