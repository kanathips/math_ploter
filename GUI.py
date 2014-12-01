''''Math Ploter'''
import matplotlib
matplotlib.use('TkAgg')

#import tkColorChooser use to set color of graph
import tkColorChooser

#import tkFileDialog to save graph
import tkFileDialog
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
    '''Class to create Ploter section'''
    def __init__(self, main_win):
        '''Main variable of this class'''
        self.main_win = main_win.main_win
        self.grid_status = True #status of grid for ploter
        self.ploter_frame()

    def ploter_frame(self):
        '''function to create ploter section'''
        #frame for ploter
        frame = Tk.Frame(self.main_win, width = 500, height = 500) 

        # set height and weight of Figure
        self.figure = Figure(figsize = (5, 5), dpi = 100)

        self.ploter = self.figure.add_subplot(111) 
        #Part for enable or disable grid of ploter
        self.ploter.grid(self.grid_status) 

        self.canvas = FigureCanvasTkAgg(self.figure, master = frame)
        self.canvas.show() 
         #pack canvas to frame
        
        self.canvas.get_tk_widget().pack(fill = Tk.BOTH, expand = 1)
        #pack frame to root window
        frame.grid(row = 0, column = 0, rowspan = 3, sticky = Tk.W) 

#Main window
class Main_win(object): #GUI class    
    '''Class to create main window '''
    def __init__(self):
        '''Main variable of this class'''
        self.main_win = Tk.Tk()
        self.main_win.resizable(0, 0) #config to fix size of main window
        self.main_win.wm_title('Math Ploter') #Set titel of main window

#Equation box section
class Equation(object):
    '''Class to create equation section'''
    def __init__(self, main_win, ploter, rounds):
        '''Main variable of this class'''
        self.fig = ploter.figure
        self.ploter_frame = ploter.ploter_frame
        self.rounds = rounds
        self.line_color = '#000000'
        self.main_win = main_win.main_win
        self.equation_frame()
        
    #color dialog for graph 
    def color_chooser(self): #function to choose color of graph
        '''function to create color chooser window'''
        (rgb, self.line_color) = tkColorChooser.askcolor()
        self.color_change.config(fg = self.line_color)

    def equation_frame(self):
        '''function to create equation box colorChooser botton and stylechooser botton'''
        frame = Tk.Frame(self.main_win, padx = 20, pady = 20)
        
        entry = Tk.Entry(frame)
        entry.grid(row = 0, column = 0, columnspan = 2)

        style_change = Tk.Button(frame, text = 'Style', command = self.style_chooser)
        style_change.grid(row = 1, column = 1)

        self.color_change = Tk.Button(frame, text= 'Color', command = self.color_chooser)
        self.color_change.grid(row = 1, column = 0)

        frame.grid(column = 1, row = self.rounds, sticky=Tk.NE)

    def style_chooser(self):
        '''function to create Style chooser window'''
        window = Tk.Toplevel()
        window.resizable(0, 0)
        window.title('Style Chooser')

        figure = Figure(figsize=(3, 3), dpi=100)# set height and weight of Figure

        ploter = figure.add_subplot(111) 
        
        canvas = FigureCanvasTkAgg(figure, master=window)
        canvas.show() #
        
        canvas.get_tk_widget().grid(columnspan = 3) #pack canvas to frame
        ploter.plot([0, 0], [0, 1], '-', color = self.line_color)
        ploter.plot([1, 1], [0, 1], '--', color = self.line_color)
        ploter.plot([2, 2, 2], [0, 0.5, 1], 'ro', color = self.line_color)
        ploter.axis([-1, 3, -0.5, 1.5])
        ploter.axes.get_xaxis().set_ticks([])
        ploter.axes.get_yaxis().set_ticks([])
        for i in range(1, 4):
            Tk.Button(window, text = 'Style %d' % i).grid(column = i - 1, row = 1)

class Option(object):
    def __init__(self, ploter):
        '''set all valuse in graph'''
        self.press = None
        self.cur_x_limit = None
        self.cur_y_limit = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None
        self.ploter = ploter.ploter

        self.zoom_option()
        self.pan_option()

    def zoom_option(self, base_scale = 1.1):
        def zoom(event):
            '''set veluse of size of graph''' 
            cur_x_limit = self.ploter.get_xlim()
            cur_y_limit = self.ploter.get_ylim()

            xdata = event.xdata # get event x location
            ydata = event.ydata # get event y location

            if event.button == 'up':
                # deal with zoom in
                scale_factor = 1 / base_scale
            elif event.button == 'down':
                # deal with zoom out
                scale_factor = base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1
                print event.button

            new_width = (cur_x_limit[1] - cur_x_limit[0]) * scale_factor
            new_height = (cur_y_limit[1] - cur_y_limit[0]) * scale_factor

            relx = (cur_x_limit[1] - xdata) / (cur_x_limit[1] - cur_x_limit[0])
            rely = (cur_y_limit[1] - ydata) / (cur_y_limit[1] - cur_y_limit[0])

            self.ploter.set_xlim([xdata - new_width * \
                (1 - relx), xdata + new_width * (relx)])
            self.ploter.set_ylim([ydata - new_height * \
                (1 - rely), ydata + new_height * (rely)])
            self.ploter.figure.canvas.draw()

        fig = self.ploter.get_figure() # get the figure of interest
        fig.canvas.mpl_connect('scroll_event', zoom)

        return zoom

    def pan_option(self):
        def press(event):
            if event.inaxes == self.ploter:
                self.cur_x_limit = self.ploter.get_xlim()
                self.cur_y_limit = self.ploter.get_ylim()
                self.press = self.x0, self.y0, event.xdata, event.ydata
                self.x0, self.y0, self.xpress, self.ypress = self.press

        def release(event):
            self.press = None
            self.ploter.figure.canvas.draw()

        def move(event):
            if event.inaxes == self.ploter and not (self.press is None):
                dx = event.xdata - self.xpress
                dy = event.ydata - self.ypress
                self.cur_x_limit -= dx
                self.cur_y_limit -= dy
                self.ploter.set_xlim(self.cur_x_limit)
                self.ploter.set_ylim(self.cur_y_limit)
    
            self.ploter.figure.canvas.draw()

        fig = self.ploter.get_figure() # get the figure of interest

        # attach the call back
        fig.canvas.mpl_connect('button_press_event', press)
        fig.canvas.mpl_connect('button_release_event', release)
        fig.canvas.mpl_connect('motion_notify_event', move)

        #return the function
        return move

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
        '''create menu bar
        1.buttom "Save" -> this buttom wil save picture of graph
        2.buttom "Exit" -> thi buttom will exit this program
        3.buttom "Flie" -> 
        '''menubar = Tk.Menu(self.main_win)
        # create a pulldown menu, and add it to the menu bar
        filemenu = Tk.Menu(menubar, tearoff = 0)
        filemenu.add_command(label = "Save", command = self.file_save)
        filemenu.add_separator()
        filemenu.add_command(label = "Exit", command = self.main_exit)
        menubar.add_cascade(label = "File", menu = filemenu)

        # create more pulldown menus
        editmenu = Tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label = "Edit", menu = editmenu)

        helpmenu = Tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label = "About")
        menubar.add_cascade(label = "Help", menu=helpmenu)

        # display the menu
        self.main_win.config(menu = menubar)

    def file_save(self):
        save = tkFileDialog.asksaveasfile(mode = 'w', defaultextension = ".png")
        if save is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        self.fig.savefig(save.name)
        save.close()

def main():
    import numpy as np
    main = Main_win()
    ploter = Ploter(main)
    Option(ploter)
    Menu(main, ploter)
    for i in xrange(3):
        Equation(main, ploter, i)  
    Tk.Button(text =' Start Plot').grid(column = 1 ,row = 4)
    t = np.arange(0., 20., 1)
    x = t ** 2
    ploter.ploter.plot(t, x, 'ro')
    Tk.mainloop()

main()
