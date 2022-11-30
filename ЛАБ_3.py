from tkinter import *
from tkinter import messagebox
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

def get_time(samplerate=44100,
             duration = 10):
    t = np.linspace(0, duration, samplerate*duration, False)
    return t

def get_noise(samplerate=44100,
              duration = 10,
              F_noise = [6300, 500, 4000],
              A_noise = [0.5, 1.5, 5]):
    #вектор времени
    t = np.linspace(0, duration, samplerate*duration, False)
    #Генерация шума
    noise = A_noise[0]*np.sin(2*np.pi*F_noise[0]*t) + A_noise[1]*np.sin(2*np.pi*F_noise[1]*t) + A_noise[2]*np.sin(2*np.pi*F_noise[2]*t)
    return noise
    
def get_data(samplerate=44100,
             duration = 10,
             F_signal = [400, 500, 300],
             A_signal = [30, 1.5, 5]):
    t = np.linspace(0, duration, samplerate*duration, False)
    #Генерация исходного аудио
    data = A_signal[0]*np.sin(2*np.pi*F_signal[0]*t)+A_signal[1]*np.sin(2*np.pi*F_signal[1]*t)   
    return data
    
def get_data_noise(data, noise):
    data_n = data+noise
    return data_n

def clear_data():
    return 0
    
def plot():
    t = get_time()
    data = get_data()
    noise = get_noise()
    print(type(noise))
    print(type(data))
    data_n = get_data_noise(data, noise)

    figure = Figure(figsize=(10,5), dpi=100)

    plot_data_noise = figure.add_subplot(111)
    plot_data_noise.plot(t[:1000], data_n[:1000])
    #plot_data_noise.
    plot_data_noise.margins(0, 0.5)

    # creating the Tkinter canvas containing the Matplotlib figure
    
    canvas = FigureCanvasTkAgg(figure, master = window)  
    canvas.draw()
  
    # placing the canvas on the Tkinter window
    #canvas.get_tk_widget().pack()



    canvas.grid(row=0, column=1, sticky=NSEW)
    # creating the Matplotlib toolbar
    #toolbar = NavigationToolbar2Tk(canvas, window)
    #toolbar.update()
  
    # placing the toolbar on the Tkinter window
    #canvas.get_tk_widget().pack()    




window = Tk()
window.title("ЛАБ_ПАОИС_3_4")
window.geometry('800x540')
window.title('Plotting in Tkinter')
  
window.columnconfigure(index=0, weight=1)
window.columnconfigure(index=1, weight=3)
window.rowconfigure(index=0, weight=1)
window.rowconfigure(index=1, weight=1)
window.rowconfigure(index=2, weight=1)
  
# button that displays the plot
plot_button = Button(master = window, command = plot, height = 2, width = 10, text = "Plot")
  

#canvas = Canvas(bg="white")
#canvas.grid(row=0, column=1, sticky=NSEW)

# place the button 
# in main window
plot_button.pack()

window.mainloop()
