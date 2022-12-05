from tkinter import *
from tkinter import messagebox
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from scipy.fft import rfft, rfftfreq
from scipy.fft import irfft
import psycopg2
from psycopg2 import Error


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
    global data_n
    data_n= data + noise
    print(data_n)
    figure_data_noise = Figure(figsize=(5, 1), dpi=100)
    plot_data_noise = figure_data_noise.add_subplot(111)
    plot_data_noise.plot(t[:1000], data_n[:1000])

    frame_data_noise = Frame(window)
    frame_data_noise.grid(row=0, column=2, rowspan=2)

    canvas_data_noise = FigureCanvasTkAgg(figure_data_noise, master=frame_data_noise)
    canvas_data_noise.draw()
    canvas_data_noise.get_tk_widget().pack()
    return data_n


def get_filter_data(data_n, samplerate=44100, duration=10):
    audio_3_with_noise = np.int16((data_n / data_n.max()) * 32767)
    
    yf = rfft(audio_3_with_noise)
    xf = rfftfreq(samplerate * duration, 1 / samplerate)

    # Максимальная частота составляет половину частоты дискретизации
    points_per_freq = len(xf) / (samplerate / 2)

    # Наша целевая частота - 4000 Гц
    target_idx = int(points_per_freq * 4000)
    yf[target_idx - 1:target_idx + 1] = 0

    global data_filter
    data_filter = irfft(yf)
    
    figure_data_filter = Figure(figsize=(5, 1), dpi=100)
    plot_data_filter = figure_data_filter.add_subplot(111)
    plot_data_filter.plot(t[:1000], data_filter[:1000])

    frame_data_filter = Frame(window)
    frame_data_filter.grid(row=3, column=2, rowspan=2)

    canvas_data_filter = FigureCanvasTkAgg(figure_data_filter, master=frame_data_filter)
    canvas_data_filter.draw()
    canvas_data_filter.get_tk_widget().pack()

    return data_filter

def incode_data():
    return 'Данные зашифрованы'

def decode_data():
    return 'Данные зашифрованы'

def insert_db():
    global duration
    global samplerate
    global F_signal, A_signal, F_noise, A_noise
    try:
        connection = psycopg2.connect(user='postgres',
                                      password='postgres',
                                      host='localhost',
                                      port='5432',
                                      database = 'signals')
        cursor = connection.cursor()
        # Выполнение SQL-запроса
        insert_query = '''INSERT INTO public.signal_(id_signal, duration, sample_frequency, filtering_parametr_1, filtering_parametr_2, source_path_to_audio, resulting_audio_path)
			  VALUES (nextval('seq_signal_id'),'''+str(duration)+''', '''+str(samplerate)+''', 1, 1, '', '');'''
        cursor.execute(insert_query)
        connection.commit()
        print("запись о signal_ вставлена")

        # Получить результат
        cursor.execute("select * from signal_ order by id_signal desc")
        record = cursor.fetchone()
        id_signal = record[0]

        insert_query = '''
    INSERT INTO public.parameters_main_signal(id_signal, id_nomer, f, a)
	VALUES ('''+str(id_signal)+''', 0, '''+ str(F_signal[0])+''', '''+ str(A_signal[0])+''');
    INSERT INTO public.parameters_main_signal(id_signal, id_nomer, f, a)
	VALUES ('''+str(id_signal)+''', 1, '''+ str(F_signal[1])+''', '''+ str(A_signal[1])+''');
    INSERT INTO public.parameters_main_signal(id_signal, id_nomer, f, a)
	VALUES ('''+str(id_signal)+''', 2, '''+ str(F_signal[2])+''', '''+ str(A_signal[2])+''');
'''
        cursor.execute(insert_query)
        connection.commit()
        print("запись о параметрах главного сигнала вставлена")
        print(F_noise)
        print(A_noise)
        insert_query = '''
    INSERT INTO public.parameters_noise(id_signal, id_nomer, f, a)
	VALUES ('''+str(id_signal)+''', 0, '''+ str(F_noise[0])+''', '''+ str(A_noise[0])+''');
    INSERT INTO public.parameters_noise(id_signal, id_nomer, f, a)
	VALUES ('''+str(id_signal)+''', 1, '''+ str(F_noise[1])+''', '''+ str(A_noise[1])+''');
    INSERT INTO public.parameters_noise(id_signal, id_nomer, f, a)
	VALUES ('''+str(id_signal)+''', 2, '''+ str(F_noise[2])+''', '''+ str(A_noise[2])+''');
'''
        cursor.execute(insert_query)
        connection.commit()
        print("запись о параметрах шума вставлена")
        
        print("Результат id_signal", record[0])
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")
    #return 'Данные записаны'


def select_from_db(signal_id):
    return 'Данные из БД ' + str(signal_id)

duration = 10
samplerate = 44100

F_signal=[400, 500, 300]
A_signal=[30, 1.5, 5]

F_noise=[6300, 500, 4000]
A_noise=[0.5, 1.5, 5]

t = get_time()
data = get_data()
noise = get_noise()
data_n = []
data_filter = []
#data_n = get_data_noise(data, noise)
#data_filter = get_filter_data(data_n)


window = Tk()
window.title("ЛАБ_ПАОИС_3_4")
window.geometry('800x540')
window.title('Plotting in Tkinter')

btn_get_signal = Button(text='Получить сигнал', command = lambda: get_data_noise(data, noise))
btn_get_signal.grid(row=0, column=0)
print(data_n)

btn_filter_signal = Button(text='Фильтровать сигнал', command = lambda: get_filter_data(data_n))#
btn_filter_signal.grid(row=1, column=0)

btn_save_bd = Button(text='Записать в БД', command = insert_db)
btn_save_bd.grid(row=2, column=0)

btn_select_bd = Button(text='Получить из БД')
btn_select_bd.grid(row=3, column=0)

entry_num_signal = Entry(width=5)
entry_num_signal.grid(row=3, column=1)





window.mainloop()
