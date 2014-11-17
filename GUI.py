import matplotlib
matplotlib.use('TkAgg')

#import tkColorChooser use to set color of graph
import tkColorChooser

#import tkFileDialog to save graph
import tkFileDialog

#import arange from numpy to create x values (float)
from numpy import arange

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

#import Figure from matplotlib to be space for ploter 
from matplotlib.figure import Figure

# import sys to chcek version of python
# becaues Tkinter in python 3+ and 3-  have differance name
import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

#Ploter section
class Ploter(object):
    def __init__(self, main_win):
        self.main_win = main_win.main_win
        self.grid_status = False #status of grid for ploter
        self.ploter_frame()
    def ploter_frame(self):
   
        frame = Tk.Frame(self.main_win, width=500, height=500) #frame for ploter
        self.figure = Figure(figsize=(5, 5), dpi=100)# set height and weight of Figure

        ploter = self.figure.add_subplot(111) 
        ploter.grid(self.grid_status) #Part for enable or disable grid of ploter

        self.canvas = FigureCanvasTkAgg(self.figure, master=frame)
        self.canvas.show() #
        self.canvas.get_tk_widget().pack(fill=Tk.BOTH, expand=1) #pack canvas to frame

        frame.grid(row = 0 , column = 0,rowspan = 3, sticky=Tk.W) #pack frame to root window

#Main window
class Main_win(object): #GUI class    

    def __init__(self):
        self.main_win = Tk.Tk()
        self.main_win.wm_title('Math Ploter') #Set titel of main window
        self.main_win.columnconfigure(1, weight=300)
        
#Equation box section
class Equation(object):

    def __init__(self, main_win, ploter, rounds):
        self.fig = ploter.figure
        self.rounds = rounds
        self.line_color = '#000000'
        self.main_win = main_win.main_win
        self.equation_frame()
        
    #color dialog for graph 
    def colorChooser(self): #function to choose color of graph
        (rgb, hx) = tkColorChooser.askcolor()
        self.color_change.config(fg=hx)

    
    def equation_frame(self):
        frame = Tk.Frame(self.main_win,padx = 20 , pady = 20)
        
        entry = Tk.Entry(frame)
        entry.grid(row = 0 , column = 0,columnspan=2)

        style_change = Tk.Button(frame, text = 'Style', command = self.styleChooser)
        style_change.grid(row = 1, column = 1)

        self.color_change = Tk.Button(frame, text= 'Color',command = self.colorChooser)
        self.color_change.grid(row = 1, column = 0)

        frame.grid(column = 1,row = self.rounds, sticky=Tk.NE)

    def styleChooser(self):
        window = Tk.Toplevel()
        window.title('Style Chooser')

        figure = Figure(figsize=(3, 3), dpi=100)# set height and weight of Figure

        ploter = figure.add_subplot(111) 
        ploter.grid(True) #Part for enable or disable grid of ploter

        canvas = FigureCanvasTkAgg(figure, master=window)
        canvas.show() #
        
        canvas.get_tk_widget().pack(fill=Tk.BOTH, expand=1) #pack canvas to frame

#Menu bar
class Menu(object):
    def __init__(self, main_win, ploter):
        self.main_win = main_win.main_win
        self.fig = ploter.figure
        
        self.menu_bar()

    def main_exit(self):
        self.main_win.quit()
        self.main_win.destroy()
    
    def menu_bar(self):
        menubar = Tk.Menu(self.main_win)
        # create a pulldown menu, and add it to the menu bar
        filemenu = Tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save", command = self.file_save)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command = self.main_exit)
        menubar.add_cascade(label="File", menu=filemenu)

        # create more pulldown menus
        editmenu = Tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=editmenu)

        helpmenu = Tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About")
        menubar.add_cascade(label="Help", menu=helpmenu)

        # display the menu
        self.main_win.config(menu=menubar)

    def file_save(self):
        f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".png")
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        self.fig.savefig(f.name)
        f.close()

def main():
    main = Main_win()
    ploter = Ploter(main)
    Menu(main, ploter)
    for i in xrange(3):
        Equation(main, ploter, i)  
    Tk.Button(text='Start Plot').grid(column = 1,row = 4)
    Tk.mainloop()

main()