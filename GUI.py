''''Math Ploter'''

import matplotlib
matplotlib.use('TkAgg')

import tkMessageBox

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
class Main_win(object): 
    '''Class to create main window '''
    def __init__(self):
        '''Main variable of this class'''
        self.main_win = Tk.Tk()#create main window
        self.main_win.resizable(0, 0) #config to fix size of main window
        self.main_win.wm_title('Math Ploter') #Set titel of main window
        Tk.Frame(self.main_win, width = 30, height = 300).grid(column = 3, row = 0, rowspan = 4) #separator between ploter and eqution frame
        
        self.ploter_frame() #call create ploter_frame function
        self.equation_frame() #call create equation_frame function
        
    #Ploter_frame function
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

    #Equation_frame function
    def equation_frame(self):
        '''function to create eqution section'''
        #frame for equation
        frame = Tk.Frame(self.main_win, width = 200, height  = 200, padx = 20, pady = 20) #create and config frame
        frame.grid(row = 0, column = 4, rowspan = 4) #locate frame
        equation_1 = Tk.Entry(frame) #create entry for equation 1
        Tk.Label(frame, text = 'Equation 1').grid() #create and locate label of equation 1
        equation_1.grid(row = 0, column = 1) #locate equation 1
        equation_2 = Tk.Entry(frame) #create entry for equation 2
        Tk.Label(frame, text = 'Equation 2').grid(row = 1, column = 0) #create and locate label of equation 2
        equation_2.grid(row = 1, column = 1)#locate equation 2        
        equation_3 = Tk.Entry(frame)#create entry for equation 3
        Tk.Label(frame, text = 'Equation 3').grid(row = 2, column = 0) #create and locate label of equation 3
        equation_3.grid(row = 2, column = 1)#locate equation 3
        calc = Tk.Button(frame, text = 'Calculate').grid(row = 3, column = 0, columnspan = 2)#create and locate calculate button

#Option class
class Option(object): 
    def __init__(self, main_win):
        'Defaul variable of this class'
        self.press = None #mouse click variable
        self.cur_x_limit = None #current limit of x value on ploter frame
        self.cur_y_limit = None #current limit of y value on ploter frame
        self.x0 = None #x0 position
        self.y0 = None #y0 position
        self.x1 = None #x1 position
        self.y1 = None #y1 position
        self.xpress = None #x positon when press
        self.ypress = None #y positon when press
        self.ploter = main_win.ploter #ploter frame
        self.fig = main_win.figure #ploter figure
        self.main_win = main_win #main window
        self.line_color_1 = '#000000' #color of equation 1
        self.line_color_2 = '#000000' #color of equation 2
        self.line_color_3 = '#000000' #color of equation 3
        self.line_style_1 = '-'  #style of equation 1
        self.line_style_2 = '-'  #style of equation 2
        self.line_style_3 = '-'  #style of equation 3
        self.style_var_1 = Tk.IntVar() #value of checkbutton 1 on style chooser  
        self.style_var_2 = Tk.IntVar() #value of checkbutton 2 on style chooser
        self.style_var_3 = Tk.IntVar() #value of checkbutton 3 on style chooser
        
        self.zoom_option() #use zoom option
        self.pan_option() #use pan option
        self.maxi_value = 1 #defaul minimum x value
        self.mini_value = 10 #defaul maximum x value
        self.step_value = 0.1 #defaul step

    def zoom_option(self, base_scale = 1.1):
        '''This function use to zoom ploter_frame'''
        def zoom(event):
            '''zoom'''
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
        '''This function use to pan ploter_frame'''
        def press(event):
            '''when press do'''
            if event.inaxes == self.ploter:
                self.cur_x_limit = self.ploter.get_xlim()
                self.cur_y_limit = self.ploter.get_ylim()
                self.press = self.x0, self.y0, event.xdata, event.ydata
                self.x0, self.y0, self.xpress, self.ypress = self.press

        def release(event):
            '''when release do'''
            self.press = None
            self.ploter.figure.canvas.draw()

        def move(event):
            '''when move do'''
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

    def file_save(self):
        '''This function use to save graph'''
        save = tkFileDialog.asksaveasfile(mode = 'w', defaultextension = ".png")
        if save is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        self.fig.savefig(save.name)
        save.close()

    def window_exit(self, window):
        '''this function use to exit window'''
        if 'main' in str(window) :
            window.quit()
        window.destroy()

    def color_chooser(self): #function to choose color of graph
        '''function to create color chooser window'''
        window = Tk.Toplevel()
        window.title('Color Chooser')

        def color_dialog(line, frame):
            '''open color dialog'''
            color_tmp = line
            (rgb, line) = tkColorChooser.askcolor()
            if line == None: #Check for debug when cancle color chooser window
                line = color_tmp
            frame.config(bg = line)

        color_1_frame = Tk.Frame(window, width = 100, height = 50, bg = self.line_color_1)
        color_1_frame.grid(row = 0, column = 0)
        Tk.Button(window, text = 'Equation 1', command = lambda :\
            color_dialog(self.line_color_1, color_1_frame)).grid(row = 0, column = 1)

        color_2_frame = Tk.Frame(window, width = 100, height = 50, bg = self.line_color_2)
        color_2_frame.grid(row = 1, column = 0) 
        Tk.Button(window, text = 'Equation 2', command = lambda :\
            color_dialog(self.line_color_2, color_2_frame)).grid(row = 1, column = 1)

        color_3_frame = Tk.Frame(window, width = 100, height = 50, bg = self.line_color_3)
        color_3_frame.grid(row = 2, column = 0) 
        Tk.Button(window, text = 'Equation 3', command = lambda :\
         color_dialog(self.line_color_3, color_3_frame)).grid(row = 2, column = 1)
    
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

        def style_line():
            '''save line style'''
            for i, j in [(self.line_style_1, self.style_var_1), (self.line_style_2, self.style_var_2), (self.line_style_3, self.style_var_3)]:
                i = ['-', '--', 'ro'][j.get()]
        Tk.Label(window, text = 'Equation 1').grid(column = 0, row = 1)
        Tk.Checkbutton(window, text = 'Style 1', variable = self.style_var_1, onvalue = 0).grid(column = 0, row = 2)
        Tk.Checkbutton(window, text = 'Style 2', variable = self.style_var_1, onvalue = 1).grid(column = 0, row = 3)
        Tk.Checkbutton(window, text = 'Style 3', variable = self.style_var_1, onvalue = 2).grid(column = 0, row = 4)

        Tk.Label(window, text = 'Equation 2').grid(column = 1, row = 1)
        Tk.Checkbutton(window, text = 'Style 1', variable = self.style_var_2, onvalue = 0).grid(column = 1, row = 2)
        Tk.Checkbutton(window, text = 'Style 2', variable = self.style_var_2, onvalue = 1).grid(column = 1, row = 3)
        Tk.Checkbutton(window, text = 'Style 3', variable = self.style_var_2, onvalue = 2).grid(column = 1, row = 4)

        Tk.Label(window, text = 'Equation 3').grid(column = 2, row = 1)
        Tk.Checkbutton(window, text = 'Style 1', variable = self.style_var_3, onvalue = 0).grid(column = 2, row = 2)
        Tk.Checkbutton(window, text = 'Style 2', variable = self.style_var_3, onvalue = 1).grid(column = 2, row = 3)
        Tk.Checkbutton(window, text = 'Style 3', variable = self.style_var_3, onvalue = 2).grid(column = 2, row = 4)

        Tk.Button(window, text = 'Ok' , command = style_line).grid(row = 5, column = 0)
        Tk.Button(window, text = 'cancle', command = lambda : self.window_exit(window)).grid(row = 5, column = 1)

    def xvalue(self):
        '''This function use to set x value'''
        window = Tk.Toplevel()
        window.resizable(0, 0) #Set to fig size of window
        window.title('X value setting')
        Tk.Label(window, text = 'X value minimum = ').grid(sticky = Tk.W)
        self.mini_entry = Tk.Entry(window)
        self.mini_entry.grid(row = 0, column = 1)
        Tk.Label(window, text = 'X value maximum = ').grid(row = 1, column = 0, sticky = Tk.W)
        self.maxi_entry = Tk.Entry(window)
        self.maxi_entry.grid(row = 1, column = 1) 
        Tk.Label(window, text = 'X value step            = ').grid(row = 2, column = 0, sticky = Tk.W)
        self.step_entry = Tk.Entry(window)
        self.step_entry.grid(row = 2, column = 1)

        def set_value(self):
            '''save x value'''
            if self.mini_entry.get() == '' or self.maxi_entry.get() == '' or self.step_entry.get() == '':
                tkMessageBox.showerror('Error', 'Minimum, Maximum, Step are None')
            elif self.mini_entry.get() >= self.maxi_entry.get():
                tkMessageBox.showerror('Error', 'Minimum is more than maximum')
            else:
                self.maxi_value = self.maxi_entry.get()
                self.mini_value = self.mini_entry.get()
                self.step_value = self.step_entry.get()


        Tk.Button(window, text = 'Ok' , command = set_value).grid(row = 3, column = 0)
        Tk.Button(window, text = 'cancle', command = lambda :self.window_exit(window)).grid(row = 3, column = 1)
    
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
        filemenu.add_command(label="Exit", command = lambda : self.option.window_exit(self.main_win))
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