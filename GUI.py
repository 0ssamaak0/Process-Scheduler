from tkinter import *
from Shcedulers import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from random import random

# Main Window
window = Tk()
window.title("Process Scheduler")
window.minsize(600, 350)

frame = Frame(window)
frame.grid(column=2, rowspan=10, columnspan=10)

plot = Frame(window)
plot.grid(row=30, columnspan=10)


processes = []

time_slice_flag = False
time_slice = 0

# Number of Processes
nprocess_label = Label(window, text="Number of Processes")
nprocess_label.grid(row=0, column=0)
nprocess_entry = Entry(window, bd=5)
nprocess_entry.grid(row=0, column=1)


# Type of Scheduler
type = IntVar()

type_radio_0 = Radiobutton(
    window, text="FCFS", variable=type, value=0)
type_radio_0.grid(row=1, column=0)

type_radio_1 = Radiobutton(
    window, text="SJF (Preemptive)", variable=type, value=1)
type_radio_1.grid(row=2, column=0)

type_radio_2 = Radiobutton(
    window, text="SJF (Non Preemptive)", variable=type, value=2)
type_radio_2.grid(row=3, column=0)

type_radio_3 = Radiobutton(
    window, text="Priority (Preemptive)", variable=type, value=3)
type_radio_3.grid(row=4, column=0)

type_radio_4 = Radiobutton(
    window, text="Priority (Non Preemptive)", variable=type, value=4)
type_radio_4.grid(row=5, column=0)

type_radio_5 = Radiobutton(window, text="Round Robin",
                           variable=type, value=5)
type_radio_5.grid(row=6, column=0)


# processes_filling function


def processes_filling():

    for widget in frame.winfo_children():
        widget.destroy()
    global processes
    processes = []

    try:
        nprocess_entry_int = int(nprocess_entry.get())
    except Exception:
        Errorlabel = Label(frame, text="Enter a valid value", fg="red")
        Errorlabel.grid(row=6, column=1)
    else:
        Errorlabel = Label(
            window, text="Correct value", fg="green")
        Errorlabel.grid(row=6, column=1)

    for i in range(nprocess_entry_int):
        processes.append({})

        processes[i]["processs_no"] = i + 1
        Label(frame, text=f"P{processes[i]['processs_no']}", padx=3, pady=3).grid(
            row=i, column=3)

        # Burst Time
        Label(frame, text="Burst Time").grid(row=i, column=4)
        processes[i]["burst_time"] = Entry(
            frame, width=5)
        processes[i]["burst_time"].grid(row=i, column=5)

        # Arrival Time
        Label(frame, text="Arrival Time").grid(row=i, column=6)
        processes[i]["arrival_time"] = Entry(
            frame, width=5)
        processes[i]["arrival_time"].grid(row=i, column=7)

        # If priority
        if(int(type.get()) == 3 or int(type.get()) == 4):
            Label(frame, text="Priority").grid(row=i, column=8)
            processes[i]["priority"] = Entry(
                frame, width=5)
            processes[i]["priority"].grid(row=i, column=9)
        else:
            processes[i]["priority"] = -1

    # If RR set time_slice
    if(int(type.get()) == 5):
        global time_slice_flag
        time_slice_flag = True
        Label(frame, text="Time Slice").grid(row=0, column=10)
        global time_slice_entry
        time_slice_entry = Entry(frame, width=5)
        time_slice_entry.grid(row=1, column=10)

    # Schedule Button
    Schedule = Button(frame, command=scheduler, height=5,
                      text="Shecdule").grid(row=2, column=10, rowspan=4, padx=10, pady=10)


def scheduler():
    for widget in plot.winfo_children():
        widget.destroy()
    global processes
    for process in processes:
        process["burst_time_val"] = int(process["burst_time"].get())
        process["arrival_time_val"] = int(process["arrival_time"].get())
        if(process["priority"] != -1):
            process["priority_val"] = int(process["priority"].get())

    global time_slice

    if time_slice_flag:
        time_slice = int(time_slice_entry.get())
        print(time_slice)

    time_normalizer(processes)
    if(int(type.get()) == 0):
        (gnatt, avg_wait) = FCFS(processes)
    elif (int(type.get()) == 1):
        (gnatt, avg_wait) = SJFP(processes)
    elif (int(type.get()) == 2):
        (gnatt, avg_wait) = SJFNP(processes)
    elif (int(type.get()) == 3):
        (gnatt, avg_wait) = priorityP(processes)
    elif (int(type.get()) == 4):
        (gnatt, avg_wait) = priorityNP(processes)
    elif (int(type.get()) == 5):
        (gnatt, avg_wait) = RoundRobin(processes, time_slice)

    colors = [(random(), random(), random())
              for process in range(len(gnatt))]

    figure = plt.Figure(figsize=(6, 5), dpi=100)
    ax = figure.add_subplot(111)

    canvas = FigureCanvasTkAgg(figure, plot)
    canvas.get_tk_widget().grid(columnspan=10)

    for process in gnatt:
        ax.broken_barh([(process["start"], [process["end"] - process["start"]])], (0.5, 10),
                       label=f"P{process['processs_no'],}", color=colors[process["processs_no"] - 1])
        ax.text(x=((process["end"] + process["start"]) / 2) -
                0.3, y=4.75, s=f"P{process['processs_no']}")
        ax.set_ylim(0, 20)
        ax.set_yticks([])
        ax.set_xlim(-2, gnatt[-1]["end"] + 2)
        ax.text(x=gnatt[-1]["end"] / 4, y=15,
                s=f"average waiting time = {round(avg_wait, 2)}ms")


# Submit Type and num Button
Select = Button(window, command=processes_filling, text="Select",
                height=5, width=10).grid(rowspan=4, columnspan=1, row=2, column=1)

window.mainloop()
