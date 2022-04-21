from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from random import random
from datetime import datetime


from Shcedulers import *

# Main Window

window = Tk()
window.title("Process Scheduler")
window.minsize(600, 350)

# Saving Figure


def savefig():
    global figure
    figure.savefig(f"Process Scheduler {datetime.now()}.png")


def about():
    messagebox.showinfo("About", "Github: 0ssamaak0")


# Menu
menubar = Menu(window)

filemenu = Menu(menubar, tearoff=0)
aboutmenu = Menu(menubar, tearoff=0)

filemenu.add_command(label="Save", command=savefig)

filemenu.add_separator()

filemenu.add_command(label="Exit", command=window.quit)

aboutmenu.add_command(label="About", command=about)

menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="About", menu=aboutmenu)
window.config(menu=menubar)

# Inputs Frame
frame = Frame(window)
frame.grid(column=2, rowspan=10, columnspan=10)

# plot_frame Frame
plot_frame = Frame(window)
plot_frame.grid(row=30, columnspan=10)

# Processes empty list (will be list of dictionaries)
processes = []

# Round Robin Time slice
time_slice_flag = False

# Random value canot be chosen by the user
time_slice = 932031.412345124

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

    # Removing input entries when changing the Sheduler of number of processes
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

        # If priority set priority
        if(int(type.get()) == 3 or int(type.get()) == 4):
            Label(frame, text="Priority").grid(row=i, column=8)
            processes[i]["priority"] = Entry(
                frame, width=5)
            processes[i]["priority"].grid(row=i, column=9)
        else:
            # random value can't be set by the user
            processes[i]["priority"] = 932031.412345124

    # If RoundRobin set time_slice
    global time_slice_flag
    if(int(type.get()) == 5):
        time_slice_flag = True
        Label(frame, text="Time Slice").grid(row=0, column=10)
        global time_slice_entry
        time_slice_entry = Entry(frame, width=5)
        time_slice_entry.grid(row=1, column=10)
    else:
        time_slice_flag = False

        # Schedule Button
    Schedule = Button(frame, command=scheduler, height=5,
                      text="Shecdule").grid(row=2, column=10, rowspan=4, padx=10, pady=10)


def scheduler():
    # Removing the Previous plot_frame
    for widget in plot_frame.winfo_children():
        widget.destroy()

    # Global Variables
    global processes
    global time_slice

    for process in processes:
        process["burst_time_val"] = float(process["burst_time"].get())
        process["arrival_time_val"] = float(process["arrival_time"].get())
        if(process["priority"] != 932031.412345124):
            process["priority_val"] = float(process["priority"].get())

    for process in processes:
        if (process["burst_time_val"] < 0 or process["arrival_time_val"] < 0 or process["priority"] < 0):
            Label(
                plot_frame, text="Times cannot be negative! enter valid values", fg="red").grid()
            return

    if time_slice_flag:
        time_slice = float(time_slice_entry.get())

        if(time_slice <= 0):
            Label(plot_frame, text="Time slice cannot be negative or equal zero! enter valid values",
                  fg="red").grid()
            return

    # if the first arrival time > 0, start from this time
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

    # setting random color for each process
    colors = [(random(), random(), random())
              for process in range(len(gnatt))]

    # Preparing the figure and the ax
    figure = plt.Figure(figsize=(10, 5), dpi=100)
    ax = figure.add_subplot(111)

    # Adding the plot_frame
    canvas = FigureCanvasTkAgg(figure, plot_frame)
    canvas.get_tk_widget().grid(columnspan=10)

    # Plotting the Gnatt Chart
    for process in gnatt:
        ax.broken_barh([(process["start"], [process["end"] - process["start"]])], (0.5, 10),
                       label=f"P{process['processs_no'],}", color=colors[process["processs_no"] - 1])
        ax.text(x=((process["end"] + process["start"]) / 2.1),
                y=4.75, s=f"P{process['processs_no']}")
        ax.set_ylim(0, 20)
        ax.set_yticks([])
        ax.set_xlim(- (gnatt[-1]["end"] / 15), gnatt[-1]
                    ["end"] + (gnatt[-1]["end"] / 15))
        ax.text(x=gnatt[-1]["end"] / 4, y=15,
                s=f"average waiting time = {round(avg_wait, 2)}ms")

    xticks = [process["start"] for process in gnatt]
    xticks.append(gnatt[-1]["end"])
    ax.set_xticks(xticks)


# Submit Type and num Button
Select = Button(window, command=processes_filling, text="Select",
                height=5, width=10).grid(rowspan=4, columnspan=1, row=2, column=1)

window.mainloop()
