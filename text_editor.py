import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog, Frame, Entry, Radiobutton, Checkbutton, Text, Listbox, Tk, Label, StringVar,Menu,IntVar,Entry, Toplevel, Canvas
import os

root = Tk()

root.wm_title("Untitled -MyPad")
root.iconbitmap("icons/logo.ico")

filename =  None
clrschms = {
'1. Default White': '#000000.#FFFFFF',
'2. Greygarious Grey': '#83406A.#D1D4D1',
'3. Lovely Lavender': '#202B4B.#E1E1FF' ,
'4. Aquamarine': '#5B8340.#D1E7E0',
'5. Bold Beige': '#4B4620.#FFF0E1',
'6. Cobalt Blue': '#ffffBB.#3333aa',
'7. Olive Green': '#D1E7E0.#5B8340',
'8. Solarised Yellow': 'gold4.gold2'
}


def open_file():
	global filename
	filename =   filedialog.askopenfilename(defaultextension=".txt",filetypes =[("All Files","*.*"),("Text Documents","*.txt")])
	if filename == "": # If no file chosen.
		filename = None # Absence of file.
	else:
		root.title(os.path.basename(filename) + "  -MyPad") # 
    #Returning the basename of 'file'
		textarea.delete(1.0,END)         
		fh = open(filename,"r")        
		textarea.insert(1.0,fh.read()) 
		fh.close()
		update_line_number()

def save():
	global filename
	try:
		f = open(filename, 'w')
		letter = textarea.get(1.0,END)
		f.write(letter)
		f.close()
	except:
		save_as()


def save_as():
	try:
		f = filedialog.asksaveasfilename(initialfile = 'untitled.txt', defaultextension=".txt", filetypes=[("All Files", "*.*",), ("Text Documents", "*.txt")])
		fh = open(f, 'w')
		textOutput = textarea.get(1.0,END)
		fh.write(textOutput)
		fh.close()
		root.title(os.path.basename(f) + "- MyPad")
	except:
		pass

def new_file():
	global filename
	if filename==None:
		# txt = textarea.get(1.0,END)
		if not textarea.compare("end-1c", "==", "1.0"):
			if messagebox.askokcancel("Save Changes?", "New file has been modified, save changes?"):
				save()

	root.title("Untitled -MyPad")
	filename = None
	textarea.delete(1.0, END)
	update_line_number()

def exit_ed(event=None):
	if textarea.compare("end-1c", "==", "1.0"):
		root.destroy()
	else:
		if messagebox.askokcancel("Quit", "Do you really want to Quit?"):
			root.destroy()

root.protocol('WM_DELETE_WINDOW', exit_ed)

def about(event=None):
	messagebox.showinfo("About", "Tkinter GUI Application\n Text Editor\nDeveloped By:- Harshita Aggarwal")

def helpbox(event=None):
	messagebox.showinfo("Help", "For help visit: mypad/info/x.com")

def temp():
	pass

def cut():
	textarea.event_generate("<<Cut>>")
	update_line_number()

def copy():
	textarea.event_generate("<<Copy>>")
	update_line_number()

def paste():
	textarea.event_generate("<<Paste>>")
	update_line_number()

def undo():
	textarea.event_generate("<<Undo>>")
	update_line_number()

def redo():
	textarea.event_generate("<<Redo>>")
	update_line_number()

def select_all():
	textarea.tag_add('sel',1.0,END)

def on_find():
	t2 = Toplevel(root)
	t2.title("Find")
	t2.iconbitmap("icons/find.ico")
	t2.geometry("262x65+200+250")
	t2.transient(root)
	Label(t2,text="Find All:").grid(row=0, column=0, sticky='e')
	v = StringVar()
	e = Entry(t2,width=25,textvariable=v)
	e.grid(row=0, column=1, padx=2, pady = 2, sticky='we')
	e.focus_set()
	c= IntVar()
	Checkbutton(t2, text="Ignore Case", variable=c).grid(row=1, column=1, padx=2, pady=2, sticky='e')
	Button(t2, text="Find All", command= lambda: search_for(v.get(), c.get(), textarea, t2, e)).grid(row=0, column=2, sticky='e'+'w', padx=2, pady=2)
	def close_search():
		textarea.tag_remove('match',1.0,END)
		t2.destroy()
	t2.protocol('WM_DELETE_WINDOW',close_search)

def search_for(pat,ignc,textarea,t2,e):
	textarea.tag_remove('match',1.0,END)
	count=0
	if pat:
		pos='1.0'
		while True:
			pos = textarea.search(pat,pos,nocase=ignc,stopindex=END)
			if not pos:
				break
			lastpos = '%s+%dc' %(pos,len(pat))
			textarea.tag_add('match',pos,lastpos)
			count+=1
			pos = lastpos
		textarea.tag_config('match',foreground='red',background='yellow')
		e.focus_set()
		t2.title('%d matches found' %count)


def update_line_number(event=None):
	txt=''
	if showln.get():
		endline, endcolumn = textarea.index('end-1c').split('.')
		txt = '\n'.join(map(str, range(1, int(endline))))
	lnlabel.config(text=txt, anchor="nw")
	currline,currcolumn = textarea.index('insert').split('.')
	infobar.config(text='Line: %s |Column: %s' %(currline,currcolumn))

def show_infobar():
	val = showinfo.get()
	if val:
		infobar.pack(expand=NO, fill=None, side=RIGHT, anchor='se')
	else:
		infobar.pack_forget()


def highlight_line(interval=100):
	textarea.tag_remove("active_line",1.0,END)
	textarea.tag_add("active_line","insert linestart","insert lineend+1c")
	textarea.after(interval,toggle_highlight)

def undo_highlight():
	textarea.tag_remove("active_line",1.0,END)

def toggle_highlight(event=None):
	val = hltln.get()
	if not val:
		undo_highlight()
	else:
		highlight_line()

def themeset():
	global fgc,bgc
	val = themech.get()
	clrs = clrschms.get(val)
	fgc,bgc = clrs.split('.')
	textarea.config(bg=bgc, fg=fgc)

def popup(event):
	cmenu.tk_popup(event.x_root, event.y_root, 0)


menubar = Menu(root)

filemenu = Menu(menubar, tearoff=0)
newim = PhotoImage(file="icons/new_file.png")
filemenu.add_command(label="New",compound = LEFT, image= newim, accelerator = "Ctrl + N", command = lambda: new_file())
openim = PhotoImage(file="icons/open_file.png")
filemenu.add_command(label="Open",compound = LEFT,image= openim, accelerator = "Ctrl + O", command = lambda: open_file())
filemenu.add_separator()
saveim = PhotoImage(file="icons/save.png")
filemenu.add_command(label="Save",compound = LEFT, image= saveim, accelerator = "Ctrl + S", command = lambda: save())
saveasim = PhotoImage(file="icons/save_as.png")
filemenu.add_command(label="Save As",compound = LEFT, image= saveasim, accelerator = "Ctrl + Shift + S", command = lambda: save_as())
filemenu.add_separator()
exitim = PhotoImage(file="icons/exit_ed.png")
filemenu.add_command(label="Exit",compound = LEFT, image= exitim, accelerator = "Ctrl + Q", command = lambda: exit_ed())
menubar.add_cascade(label="File", menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
undoim = PhotoImage(file="icons/undo.png")
editmenu.add_command(label="Undo", compound = LEFT, image=undoim, accelerator = "Ctrl + Z", command = lambda: undo())
redoim = PhotoImage(file="icons/redo.png")
editmenu.add_command(label="Redo", compound = LEFT, image = redoim, accelerator = "Ctrl + Y", command = lambda: redo())
editmenu.add_separator()
copyim = PhotoImage(file="icons/copy.png")
editmenu.add_command(label="Copy", compound = LEFT, image=copyim, accelerator = "Ctrl + C", command = lambda: copy())
cutim = PhotoImage(file="icons/cut.png")
editmenu.add_command(label="Cut", compound = LEFT, image=cutim, accelerator = "Ctrl + X", command = lambda: cut())
pasteim = PhotoImage(file="icons/paste.png")
editmenu.add_command(label="Paste", compound = LEFT, image=pasteim, accelerator = "Ctrl + V", command = lambda: paste())
editmenu.add_separator()
findim = PhotoImage(file="icons/on_find.png")
editmenu.add_command(label="Find",compound = LEFT, image=findim, accelerator = "Ctrl + F", command = lambda: on_find())
editmenu.add_separator()
editmenu.add_command(label="Select All", accelerator = "Ctrl + A", command = lambda: select_all())
menubar.add_cascade(label="Edit", menu=editmenu)

viewmenu = Menu(menubar, tearoff=0)
showln = IntVar()
showln.set(1)
viewmenu.add_checkbutton(label="Show Line Number", variable=showln)
showinfo = IntVar()
showinfo.set(1)
viewmenu.add_checkbutton(label="Show Info Bar at Bottom", variable=showinfo, command=show_infobar)
hltln = IntVar()
viewmenu.add_checkbutton(label="Highlight Current Line", variable=hltln, command=lambda: toggle_highlight())

themech = StringVar()
themech.set('1. Default White')
themesmenu = Menu(menubar,tearoff=0)
for k in sorted(clrschms): 
	themesmenu.add_radiobutton(label=k, variable=themech, command=themeset)

viewmenu.add_cascade(label="Themes", menu=themesmenu)
menubar.add_cascade(label="View", menu=viewmenu)

aboutmenu = Menu(menubar, tearoff=0)
aboutmenu.add_command(label="About", command = lambda: about())
aboutmenu.add_separator()
aboutmenu.add_command(label="Help", command = lambda: helpbox())
menubar.add_cascade(label="About", menu=aboutmenu)

root.config(menu=menubar)

# Shortcut bar with icons
shortcutbar = Frame(root, height=50, bd=1, relief=RAISED)
icons = ['new_file','open_file','save','save_as','copy','cut','paste','undo','redo','on_find','exit_ed']
for i, icon in enumerate(icons):
	tbicon = PhotoImage(file="icons/"+icon+".png")
	cmd = eval(icon)
	toolbar = tk.Button(shortcutbar,image=tbicon, command=cmd)
	toolbar.image=tbicon
	toolbar.pack(side=LEFT,fill=X)
shortcutbar.pack(expand=NO, fill=X)

# For Line Number
lnlabel = Label(root, width = 2, bg='white', relief=RAISED)
lnlabel.pack(side=LEFT, anchor='nw', fill=Y)

# Text Area
textarea = Text(root, undo=True)
textarea.pack(expand=YES, fill=BOTH)
textarea.bind("<Any-KeyPress>", update_line_number)
textarea.tag_configure("active_line",background='ivory2')

#Scroll Bar
scroll= Scrollbar(textarea)
textarea.configure(yscrollcommand=scroll.set)
scroll.config(command=textarea.yview)
scroll.pack(side=RIGHT, fill=Y)

#Info Bar: Line and Column Number
infobar = Label(textarea, text='Line: 1 |Column: 0')
infobar.pack(expand=NO, fill=None, side=RIGHT, anchor='se')


# Adding keyboard shorcuts
textarea.bind("<Control-N>",lambda e: new_file())
textarea.bind("<Control-n>",lambda e: new_file())
textarea.bind("<Control-O>",lambda e: open_file())
textarea.bind("<Control-o>",lambda e: open_file())
textarea.bind("<Control-S>",lambda e: save())
textarea.bind("<Control-s>",lambda e: save())
textarea.bind("<Control-Shift-S>",lambda e: save_as())
textarea.bind("<Control-Shift-s>",lambda e: save_as())
textarea.bind("<Control-Q>",lambda e: exit_ed())
textarea.bind("<Control-q>",lambda e: exit_ed())
textarea.bind("<Escape>",lambda e: exit_ed())
textarea.bind("<Control-A>",lambda e: select_all())
textarea.bind("<Control-a>",lambda e: select_all())
textarea.bind("<Control-F>",lambda e: on_find())
textarea.bind("<Control-f>",lambda e: on_find())


# Adding Context Menu
cmenu = Menu(textarea)
for i in ('cut','copy','paste','undo','redo'):
	cmd = eval(i)
	cmenu.add_command(label=i,command=cmd)
cmenu.add_separator()
cmenu.add_command(label='Select-All', command=select_all)

textarea.bind('<Button-3>',popup)


root.geometry("1280x720")
root.mainloop()