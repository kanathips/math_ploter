import matplotlib
matplotlib.use('TkAgg')

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

grid_status = False #status of grid for ploter

root = Tk.Tk()
root.wm_title("Embedding in TK") #Set titel of main window
frame = Tk.Frame(root, width=500, height=500, bd=1) #frame for ploter
figure = Figure(figsize=(3,3), dpi=100)# set height and weight of Figure

ploter = figure.add_subplot(111) 
ploter.grid(grid_status) #Part for enable or disable grid of ploter
    

canvas = FigureCanvasTkAgg(figure, master=frame)
canvas.show() #
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1) #pack canvas to frame
frame.pack() #pack frame to root window

Tk.mainloop()

