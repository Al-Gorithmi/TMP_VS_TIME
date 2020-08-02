import serial
from datetime import datetime
import time
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import Text, StringVar
import csv


tmp  = []
timez = []

ArduinoData = serial.Serial('com3', 9600)

def getTmp():
    x = ArduinoData.readline()
    String = x.strip()
    Temperature = String.decode()
    return Temperature

def svdecode(strvar,argz):
    strvar.set(argz.get('1.0', 'end -1c'))
    return strvar.get()

def graph(time_limit, yaxis):
    tmp.clear()
    timez.clear()
    time_limit = float(time_limit)
    start = time.time()
    end = time.time()
    while (end-start) < time_limit:
        timez.append(round((end - start), 6))
        tmp.append(float(getTmp()))
        end = time.time()

    file = open('data.csv', 'w')
    for timer, valz in zip(timez, tmp):
        writer = csv.writer(file)
        writer.writerow((valz, timer))

    plt.title(f'{yaxis} VS Time')
    plt.xlabel('Time / s')
    plt.ylabel(yaxis)
    plt.plot(timez,tmp)
    plt.show()


def Integral():
    global integralz

    delta_t = 0
    t_int = 0
    for t_final in timez:
        delta_t += t_final - t_int
        t_int = t_final
    delta_t = delta_t/len(timez)

    min_sum = 0
    for fx in tmp[:-1]:
        min_sum += fx * delta_t
    max_sum = 0
    for fx in tmp[1:]:
        max_sum += fx * delta_t
    integral = (max_sum + min_sum)/2
    integral = round(integral, 4)
    integralz.set(integral)


root = tk.Tk()
root.title('Arduino Grapher')
root.resizable(height = False, width = False)

time_limit = StringVar()
y_axis = StringVar()
integralz = StringVar()

canvas = tk.Canvas(root, height = 150, width = 500, bg = 'White')
canvas.pack()

Frame = tk.Frame(root)
Frame.place(relwidth = 1.0, relheight = 1.0)

Time_label = tk.Label(Frame, text = 'Time Span (in seconds):', font = 50)
Time_label.grid(row = 1, column = 0)

Time_txt = tk.Text(Frame, height = 1, width = 20, font = 50,relief = 'solid')
Time_txt.grid(row = 1, column = 1)


yaxis_label = tk.Label(Frame, text='Y axis label: ', font=50)
yaxis_label.grid(row=2, column=0)

yaxis_txt = tk.Text(Frame, height=1, width=20, font=50, relief='solid')
yaxis_txt.grid(row=2, column=1)


graph_button = tk.Button(Frame, text='Graph', padx=5,
                         pady=10, command=lambda: graph(svdecode(time_limit, Time_txt), svdecode(y_axis, yaxis_txt)))
graph_button.grid(row = 3, column = 1)


Integral_label = tk.Label(Frame, text='Integral: ', font=50)
Integral_label.grid(row=4, column=0)

Integral_label = tk.Label(Frame, textvariable = integralz, font=50)
Integral_label.grid(row=4, column=1)

integral_button = tk.Button(Frame, text='Integral', padx=5,
                            pady=10, command=Integral)
integral_button.grid(row=4, column=2)

root.mainloop()
