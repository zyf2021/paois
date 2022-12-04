from tkinter import *
from tkinter import messagebox
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from scipy.fft import rfft, rfftfreq
from scipy.fft import irfft

def get_time(samplerate=44100,
             duration=10):
    t = np.linspace(0, duration, samplerate * duration, False)
    return t


def get_noise(samplerate=44100,
              duration=10,
              F_noise=[6300, 500, 4000],
              A_noise=[0.5, 1.5, 5]):
    # вектор времени
    t = np.linspace(0, duration, samplerate * duration, False)
    # Генерация шума
    noise = A_noise[0] * np.sin(2 * np.pi * F_noise[0] * t) + A_noise[1] * np.sin(2 * np.pi * F_noise[1] * t) + A_noise[
        2] * np.sin(2 * np.pi * F_noise[2] * t)
    return noise


def get_data(samplerate=44100,
             duration=10,
             F_signal=[400, 500, 300],
             A_signal=[30, 1.5, 5]):
    t = np.linspace(0, duration, samplerate * duration, False)
    # Генерация исходного аудио
    data = A_signal[0] * np.sin(2 * np.pi * F_signal[0] * t) + A_signal[1] * np.sin(2 * np.pi * F_signal[1] * t)
    return data


def get_data_noise(data, noise):
    data_n = data + noise
    print(data_n)
    return data_n


def get_filter_data(data_n, samplerate=44100, duration=10):
    audio_3_with_noise = np.int16((data_n / data_n.max()) * 32767)
    yf = rfft(audio_3_with_noise)
    xf = rfftfreq(samplerate * duration, 1 / samplerate)
    #plt.plot(xf, np.abs(yf))
    #plt.show()
    # Максимальная частота составляет половину частоты дискретизации
    points_per_freq = len(xf) / (samplerate / 2)
    print(points_per_freq)
    # Наша целевая частота - 4000 Гц
    target_idx = int(points_per_freq * 4000)
    print(target_idx)
    yf[target_idx - 1:target_idx + 1] = 0
    #plt.plot(xf, np.abs(yf))
    #plt.show()
    data_filter = irfft(yf)
    return data_filter

def code_data():
    return 'Данные зашифрованы'


def insert_db():
    return 'Данные записаны'


def select_from_db(signal_id):
    return 'Данные из БД ' + str(signal_id)


t = get_time()
data = get_data()
noise = get_noise()
data_n = get_data_noise(data, noise)
data_filter = get_filter_data(data_n)


window = Tk()
window.title("ЛАБ_ПАОИС_3_4")
window.geometry('800x540')
window.title('Plotting in Tkinter')

btn_get_signal = Button(text='Получить сигнал', command=get_data_noise(data, noise))
btn_get_signal.grid(row=0, column=0)

btn_filter_signal = Button(text='Фильтровать сигнал', command = get_filter_data(data_n))
btn_filter_signal.grid(row=1, column=0)

btn_save_bd = Button(text='Записать в БД')
btn_save_bd.grid(row=2, column=0)

btn_select_bd = Button(text='Получить из БД')
btn_select_bd.grid(row=3, column=0)

entry_num_signal = Entry(width=5)
entry_num_signal.grid(row=3, column=1)

figure_data_noise = Figure(figsize=(5, 1), dpi=100)
plot_data_noise = figure_data_noise.add_subplot(111)
plot_data_noise.plot(t[:1000], data_n[:1000])

frame_data_noise = Frame(window)
frame_data_noise.grid(row=0, column=2, rowspan=2)

canvas_data_noise = FigureCanvasTkAgg(figure_data_noise, master=frame_data_noise)
canvas_data_noise.draw()
canvas_data_noise.get_tk_widget().pack()

figure_data_filter = Figure(figsize=(5, 1), dpi=100)
plot_data_filter = figure_data_filter.add_subplot(111)
plot_data_filter.plot(t[:1000], data_filter[:1000])

frame_data_filter = Frame(window)
frame_data_filter.grid(row=3, column=2, rowspan=2)

canvas_data_filter = FigureCanvasTkAgg(figure_data_filter, master=frame_data_filter)
canvas_data_filter.draw()
canvas_data_filter.get_tk_widget().pack()

window.mainloop()
