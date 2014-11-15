import matplotlib
matplotlib.use('TkAgg')

#import tkColorChooser use to set color of graph
import tkColorChooser

#import arange from numpy to create x values (float)
from numpy import arange

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
        figure = Figure(figsize=(3,3), dpi=100)# set height and weight of Figure

        ploter = figure.add_subplot(111) 
        ploter.grid(self.grid_status) #Part for enable or disable grid of ploter

        canvas = FigureCanvasTkAgg(figure, master=frame)
        canvas.show() #
        canvas.get_tk_widget().pack(fill=Tk.BOTH, expand=1) #pack canvas to frame

        frame.pack(side = Tk.LEFT) #pack frame to root window

#Main window
class Main_win(object): #GUI class    

    def __init__(self):
        self.main_win = Tk.Tk()
        self.main_win.wm_title('Math Ploter') #Set titel of main window

#Equation box section
class Equation(object):

    def __init__(self, main_win):
        self.line_color = '#000000'
        self.main_win = main_win.main_win
        self.equation_frame()
        
        
    def colorChooser(self): #function to choose color of graph
        (rgb, hx) = tkColorChooser.askcolor()
        self.color_change.config(fg=hx)

    
    def equation_frame(self):
        frame = Tk.Frame(self.main_win,pady = 20, padx = 20)
        
        entry = Tk.Entry(frame)
        entry.pack()

        style_change = Tk.Button(frame, text = 'Style')
        style_change.pack(side = Tk.RIGHT)

        self.color_change = Tk.Button(frame, text= 'Color',command = self.colorChooser)
        self.color_change.pack(side = Tk.LEFT)

        frame.pack()

#Menu bar
class Menu(object):
    def __init__(self, main_win):
        self.main_win = main_win.main_win
        self.menu_bar()
        
        
    def menu_bar(self):
        menubar = Tk.Menu(self.main_win)
        # create a pulldown menu, and add it to the menu bar
        filemenu = Tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save")
        filemenu.add_separator()
        filemenu.add_command(label="Exit")
        menubar.add_cascade(label="File", menu=filemenu)

        # create more pulldown menus
        editmenu = Tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=editmenu)

        helpmenu = Tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About")
        menubar.add_cascade(label="Help", menu=helpmenu)

        # display the menu
        self.main_win.config(menu=menubar)

        
       

def main():
    main = Main_win()
    Menu(main)
    Ploter(main)
    for _ in xrange(3):
        Equation(main)
    Tk.Button(text='Start Plot').pack()
    
    Tk.mainloop()

main()
