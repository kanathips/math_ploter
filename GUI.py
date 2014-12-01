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
    

#Main window
class Main_win(object): #GUI class    
    '''Class to create main window '''
    def __init__(self):
        '''Main variable of this class'''
        self.main_win = Tk.Tk()
        self.main_win.resizable(0, 0) #config to fix size of main window
        self.main_win.wm_title('Math Ploter') #Set titel of main window
        self.grid_status = True
        Tk.Frame(self.main_win, width = 30, height = 300).grid(column = 3, row = 0, rowspan = 4) #separator between ploter and eqution frame
        
        self.ploter_frame()
        self.equation_frame()
        

    def ploter_frame(self):
        '''function to create ploter section'''
        #frame for ploter
        frame = Tk.Frame(self.main_win, width = 500, height = 500) 

        # set height and weight of Figure
        self.figure = Figure(figsize = (5, 5), dpi = 100)
        self.ploter = self.figure.add_subplot(111) 
        
        #Part for enable or disable grid of ploter
        self.ploter.grid() 

        self.canvas = FigureCanvasTkAgg(self.figure, master = frame)
        self.canvas.show() 
        
        #pack canvas to frame
        self.canvas.get_tk_widget().pack(fill = Tk.BOTH, expand = 1)
        
        #pack frame to root window
        frame.grid(row = 0, column = 0, rowspan = 5, columnspan = 3, sticky = Tk.W) 

    def equation_frame(self):
        frame = Tk.Frame(self.main_win, width = 200, height  = 200, padx = 20, pady = 20)
        frame.grid(row = 0, column = 4, rowspan = 4)

        equation_1 = Tk.Entry(frame)
        Tk.Label(frame, text = 'Equation 1').grid()
        equation_1.grid(row = 0, column = 1)

        equation_2 = Tk.Entry(frame)
        Tk.Label(frame, text = 'Equation 2').grid(row = 1, column = 0)
        equation_2.grid(row = 1, column = 1)
        
        equation_3 = Tk.Entry(frame)
        Tk.Label(frame, text = 'Equation 3').grid(row = 2, column = 0)
        equation_3.grid(row = 2, column = 1)

        calc = Tk.Button(frame, text = 'Calculate').grid(row = 3, column = 0, columnspan = 2)

class Option(object):
    def __init__(self, main_win):
        self.press = None
        self.cur_x_limit = None
        self.cur_y_limit = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None
        self.ploter = main_win.ploter
        self.fig = main_win.figure
        self.main_win = main_win
        self.line_color_1 = '#000000'
        self.line_color_2 = '#000000'
        self.line_color_3 = '#000000'
        self.line_style_1 = '-'
        self.line_style_2 = '-'
        self.line_style_3 = '-'
        self.zoom_option()
        self.pan_option()

    def zoom_option(self, base_scale = 1.1):
        def zoom(event):
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
        fig.canvas.mpl_connect('button_press_event',press)
        fig.canvas.mpl_connect('button_release_event',release)
        fig.canvas.mpl_connect('motion_notify_event',move)

        #return the function
        return move

    def file_save(self):
        save = tkFileDialog.asksaveasfile(mode = 'w', defaultextension = ".png")
        if save is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        self.fig.savefig(save.name)
        save.close()

    def main_exit(self):
        self.main_win.main_win.quit()
        self.main_win.main_win.destroy()

    def color_chooser(self): #function to choose color of graph
        '''function to create color chooser window'''
        window = Tk.Toplevel()
        window.title('Color Chooser')
        frame_tmp = []

        def color_dialog_1():
            color_tmp = self.line_color_1
            (rgb, self.line_color_1) = tkColorChooser.askcolor()
            if self.line_color_1 == None: #Check for debug when cancle color chooser window
                self.line_color_1 = color_tmp
            color_1_frame.config(bg = self.line_color_1)

        def color_dialog_2():
            color_tmp = self.line_color_2
            (rgb, self.line_color_2) = tkColorChooser.askcolor()
            if self.line_color_2 == None: #Check for debug when cancle color chooser window
                self.line_color_2 = color_tmp
            color_2_frame.config(bg = self.line_color_2)

        def color_dialog_3():
            color_tmp = self.line_color_3
            (rgb, self.line_color_3) = tkColorChooser.askcolor()
            if self.line_color_3 == None: #Check for debug when cancle color chooser window
                self.line_color_3 = color_tmp
            color_3_frame.config(bg = self.line_color_3)

        color_1_frame = Tk.Frame(window, width = 100, height = 50, bg = self.line_color_1)
        color_1_frame.grid(row = 0, column = 0)
        Tk.Button(window, text = 'Equation 1', command = color_dialog_1).grid(row = 0, column = 1)

        color_2_frame = Tk.Frame(window, width = 100, height = 50, bg = self.line_color_2)
        color_2_frame.grid(row = 1, column = 0) 
        Tk.Button(window, text = 'Equation 2', command = color_dialog_2).grid(row = 1, column = 1)

        color_3_frame = Tk.Frame(window, width = 100, height = 50, bg = self.line_color_3)
        color_3_frame.grid(row = 2, column = 0) 
        Tk.Button(window, text = 'Equation 3', command = color_dialog_3).grid(row = 2, column = 1)
    
    def style_chooser(self):
        '''function to create Style chooser window'''
        window = Tk.Toplevel()
        window.resizable(0, 0) #Set to fig size of window
        window.title('Style Chooser')

        figure = Figure(figsize=(3, 3), dpi=100)# set height and weight of Figure

        ploter = figure.add_subplot(111) 
        
        canvas = FigureCanvasTkAgg(figure, master=window)
        canvas.show() #
        
        canvas.get_tk_widget().grid(columnspan = 3) #pack canvas to frame

        ploter.plot([0, 0], [0, 1], '-', color = 'blue')
        ploter.plot([1, 1], [0, 1], '--', color = 'blue')
        ploter.plot([2, 2, 2], [0, 0.5, 1], 'ro', color = 'blue')
        ploter.axis([-1, 3, -0.5, 1.5])
        ploter.axes.get_xaxis().set_ticks([])
        ploter.axes.get_yaxis().set_ticks([])

        Tk.Label(window, text = 'Equation 1').grid(column = 0, row = 1)
        Tk.Checkbutton(window, text = 'Style 1').grid(column = 0, row = 2)
        Tk.Checkbutton(window, text = 'Style 2').grid(column = 0, row = 3)
        Tk.Checkbutton(window, text = 'Style 3').grid(column = 0, row = 4)

        Tk.Label(window, text = 'Equation 2').grid(column = 1, row = 1)
        Tk.Checkbutton(window, text = 'Style 1').grid(column = 1, row = 2)
        Tk.Checkbutton(window, text = 'Style 2').grid(column = 1, row = 3)
        Tk.Checkbutton(window, text = 'Style 3').grid(column = 1, row = 4)

        Tk.Label(window, text = 'Equation 3').grid(column = 2, row = 1)
        Tk.Checkbutton(window, text = 'Style 1').grid(column = 2, row = 2)
        Tk.Checkbutton(window, text = 'Style 2').grid(column = 2, row = 3)
        Tk.Checkbutton(window, text = 'Style 3').grid(column = 2, row = 4)

    def xvalue(self):
        window = Tk.Toplevel()
        window.resizable(0, 0) #Set to fig size of window
        window.title('X value setting')

        Tk.Label(window, text = 'X value minimum = ').grid()
        mini = Tk.Entry(window)
        mini.grid(row = 0, column = 1)

        Tk.Label(window, text = 'X value maximum = ').grid(row = 1, column = 0)
        maxi = Tk.Entry(window)
        maxi.grid(row = 1, column = 1)

        
        Tk.Label(window, text = 'X value step = ').grid(row = 2, column = 0)
        step = Tk.Entry(window)
        step.grid(row = 2, column = 1)
    
#Menu bar
class Menu(object):
    def __init__(self, main_win, option):
        self.main_win = main_win.main_win
        self.option = option
        self.menu_bar()
    
    def menu_bar(self):
        menubar = Tk.Menu(self.main_win)
        # create a pulldown menu, and add it to the menu bar
        filemenu = Tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save", command = self.option.file_save)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command = self.option.main_exit)
        menubar.add_cascade(label="File", menu=filemenu)

        # create more pulldown menus
        editmenu = Tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Color", command = self.option.color_chooser)
        editmenu.add_command(label="Style", command = self.option.style_chooser)
        editmenu.add_command(label="X value", command = self.option.xvalue)
        menubar.add_cascade(label="Edit", menu=editmenu)

        helpmenu = Tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label = "About")
        menubar.add_cascade(label = "Help", menu=helpmenu)

        # display the menu
        self.main_win.config(menu = menubar)

def main():
    main = Main_win()
    option = Option(main)
    Menu(main, option)
    Tk.mainloop()

main()