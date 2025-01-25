# import tkinter as tk
from tkinter import * 
import tkinter as tk
from tkinter.ttk import *
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functools import partial
import csv
import time


range_flux = [5e+6, 12e+6]
range_temp = [0, 850]
range_pressure = [2, 6]

max_flux, min_flux = range_flux[1], range_flux[0]
max_temp, min_temp = range_temp[1], range_temp[0]
max_pressure, min_pressure = range_pressure[1], range_pressure[0]

setpoint_flux = 11e+6
setpoint_temp = 740
setpoint_pres = 4.4

# list_reading_pressure = [2, 2,2]
# list_reading_flux = [5e+6, 5e+6,5e+6]
# list_reading_temp = [0, 0,0]
# list_reading_pressure = [3, 4.5, 5]
# list_reading_flux = [6e+6, 7e+6, 10e+6]
# list_reading_temp = [500, 800, 740.1]

def update_reading(canvas, 
                       height, 
                       channel1, channel2, channel3,
                       list_reading):
    """Simulate the water level rising and falling."""
    reading1 = list_reading[0]
    reading2 = list_reading[1]
    reading3 = list_reading[2]
    
    global water_level
    if water_level >= height:  # Water reached the top
        direction[0] = -1
    elif water_level <= 0:  # Water reached the bottom
        direction[0] = 1
    
    # Adjust water level
    water_level += direction[0] * 5  # Change this value to adjust speed
    
    # Update the water rectangle
    canvas.coords(channel1, x1, reading1, x2, y2) # the third parameter visualizes the level
    canvas.coords(channel2, x1+space, reading2, x2+space, y2)
    canvas.coords(channel3, x1+(space*2), reading3, x2+(space*2), y2)

    # Schedule the next update
    root.after(100, update_reading, 
               canvas, 
               height, channel1, channel2, channel3, list_reading)

# Initialize tkinter
root = Tk()
root.title("RPS simulation")
root.geometry("1500x700")

space = 50
y1, y2 = 35, 175
height = y2-y1

bar_width = 10
x1 = 70  # Top-left corner of the tank
x2= x1+bar_width # Bottom-right corner of the tank
canvas_width = x2 + 150
canvas_height = 200

water_level = 0
direction = [1]  # Direction for water level change (1 = up, -1 = down)

# Tank dimensions for water rectangle
def logic_processing(setpoint, list_reading):

    list_logic = []
    for i in range(0,len(list_reading)):
        if list_reading[i] > setpoint:
            list_logic.append(1)
        else:
            list_logic.append(0)
        
        if list_logic.count(1) >= 2:
            status = "TRUE"
        elif list_logic.count(0) >= 2:
            status = "FALSE"
    return status

# ----- ALARM WIDGET ------
def alarm_button_command():
    print("Alarm activated")

def alarm_button_widget(button, activated):
    if button == "temp":
        column = 1
        button_text = f"Helium Temperature (°C)"
    elif button == "pressure":
        column = 2
        button_text = f"Primary Coolant Pressure (MPa)"
    elif button == "flux":
        column = 0
        button_text = "Neutron Flux (cm^-2 s^-1)"

    if activated == "TRUE":
        background = "red"
    elif activated == "FALSE":
        background = "white"

    button1 = tk.Button(root, 
                text=button_text, 
                command=alarm_button_command,
                activebackground="blue", 
                activeforeground="white",
                anchor="center",
                bd=3,
                bg=background,
                # cursor="hand2",
                # disabledforeground="gray",
                fg="black",
                font=("Arial", 10),
                height=3,
                highlightbackground="black",
                highlightcolor="green",
                highlightthickness=2,
                justify="center",
                overrelief="raised",
                padx=10,
                pady=5,
                width=25,
                wraplength=100)
    
    button1.grid(row=0, column=column, padx=1, pady=1)

# ---- BAR WIDGET -----    
def bar_widget(label, canvas, min, max,
               setpoint,
               column, row,
               list_reading):
    canvas.delete("all")
    reading_color = "black"
    channel_color = "red"
    setpoint_line = y2 - ((setpoint-min)/(max-min)) * height

    reading1 = list_reading[0]
    reading2 = list_reading[1]
    reading3 = list_reading[2]

    height1 = y2 - ((reading1-min)/(max-min)) * height
    height2 = y2 - ((reading2-min)/(max-min)) * height
    height3 = y2 - ((reading3-min)/(max-min)) * height

    list_reading = [height1, height2, height3]

    text1, text2, text3 = f"{reading1:.2f}", f"{reading2:.2f}", f"{reading3:.2f}"

    if label == "flux":
        text1, text2, text3 = f"{reading1:.1e}", f"{reading2:.1e}", f"{reading3:.1e}"
        
    canvas.create_text(x1+(bar_width/2),y1-10, 
                        text="CH1", fill=channel_color, 
                        anchor="center")
    canvas.create_rectangle( # border for channel 1
                            x1, y1, x2, y2,
                            outline="black") 
    tag1 = canvas.create_rectangle(
                            x1, y1, x2, y2, 
                            fill="blue", width=0)
    canvas.create_text(x1+(bar_width/2),y2+10, 
                        text=text1, fill=reading_color, 
                        anchor="center")
    
    canvas.create_text(x1+(bar_width/2) +space,y1-10, 
                        text="CH2", fill=channel_color, 
                        anchor="center")
    canvas.create_rectangle( # border for channel 2
                            x1+space, y1, x2+space, y2,
                            outline="black") 
    tag2 = canvas.create_rectangle(
                            x1+space, y1, x2+space, y2, 
                            fill="red", width=0) 
    canvas.create_text(x1+(bar_width/2) +space,y2+10, 
                        text=text2, fill=reading_color, 
                        anchor="center")

    canvas.create_text(x1+(bar_width/2) +space*2,y1-10, 
                        text="CH3", fill=channel_color, 
                        anchor="center")
    canvas.create_rectangle( # border for channel 3
                            x1+(space*2), y1, 
                            x2+(space*2), y2,
                            outline="black") 
    tag3 = canvas.create_rectangle(
                            x1+(space*2), y1, 
                            x2+(space*2), y2, 
                            fill="green", width=0)
    canvas.create_text(x1+(bar_width/2)+space*2,y2+10, 
                        text=text3, fill=reading_color, 
                        anchor="center")
    
    canvas.create_line( # setpoint line
                        x1 - 10, setpoint_line, 
                        x2 + (space*2) + 10, 
                        setpoint_line, 
                        fill="black", dash=(2, 2))
    if label == "flux":
        canvas.create_text( x1 - 30, setpoint_line, 
                       text=f"SP:\n{setpoint:.1e}", 
                       fill="red", anchor="center")
    else:
        canvas.create_text( x1 - 30, setpoint_line, 
                        text=f"SP:\n{setpoint}", 
                        fill="red", anchor="center"
        )

    canvas.grid(row=row, column=column, padx=0, pady=0)

    update_reading(canvas, height, 
                       tag1, tag2, tag3, list_reading)

# ----- GRAPH WIDGET ------
# Global variables to store the data for each sensor
time_stamps = []
flux_data = []
temperature_data = []
pressure_data = []

# Data counter for time stamps
new_time = 0
prev_time = 0

# Flags to track the updating state
updating = True  # Controls whether data is updated
running = True   # Indicates whether the app is running

# Create a Matplotlib figure
fig, axes = plt.subplots(3, 1, figsize=(8, 6))
fig.tight_layout(pad=3.0)

# Embed the Matplotlib figure in the Tkinter GUI
canvas_graph = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas_graph.get_tk_widget()
canvas_widget.grid(row=0, column= 3, rowspan=9)

def update_plot_data(new_flux, new_temperature, new_pressure):
    """
    new_flux, new_temperature, new_pressure: list of the most updated sensor data
    """
    global prev_time, updating, running
    if not updating or not running:  # Stop updating if reset or window is closed
        return

    # Generate new data
    global new_time
    new_time = prev_time + 1
    prev_time = new_time

    # new_flux, new_temperature, new_pressure = generate_random_data()

    # Append new data
    time_stamps.append(new_time)
    flux_data.append(new_flux)
    temperature_data.append(new_temperature)
    pressure_data.append(new_pressure)

    # Keep the lists to the last 20 data points
    max_points = 20
    if len(time_stamps) > max_points:
        time_stamps.pop(0)
        flux_data.pop(0)
        temperature_data.pop(0)
        pressure_data.pop(0)

    # Update plots
    update_plot(axes[0], flux_data, "Flux Sensor", r"Flux ($cm^{-2}$ $s^{-1}$)")
    update_plot(axes[1], temperature_data, "Temperature Sensor", "Temperature (°C)")
    update_plot(axes[2], pressure_data, "Pressure Sensor", "Pressure (MPa)")

    # Redraw the canvas
    canvas_graph.draw()

    # Schedule the next update
    # root.after(500, update_plot_data,
    #            new_flux, new_temperature, new_pressure)

def update_plot(ax, data, title, ylabel):
    """
    Update the data for a specific plot.
    """
    ax.clear()
    ax.set_title(title)
    ax.set_xlabel("Time")
    ax.set_ylabel(ylabel)

    # Ensure uniform x-axis ticks for all graphs
    ax.set_xticks(time_stamps)
    ax.set_xlim(min(time_stamps, default=0), max(time_stamps, default=0) + 1)

    if title == "Flux Sensor":
        y = setpoint_flux
    elif title == "Temperature Sensor":
        y = setpoint_temp
    else:
        y = setpoint_pres
    ax.axhline(y = y, color = 'purple', linestyle = '--') 

    # Plot data for each channel
    channels = ["CH1", "CH2", "CH3"]
    for i, channel in enumerate(channels):
        if channel == "CH1":
            color = 'blue'
        elif channel == "CH2":
            color = 'red'
        else:
            color = 'green'

        ax.plot(time_stamps, [point[i] for point in data], label=channel, color=color)

    # Fixate the legend location (e.g., upper right)
    ax.legend(loc='lower left')

def on_closing():
    """
    Handle the window closing event to stop updates cleanly.
    """
    global running
    running = False  # Set the running flag to False
    # root.destroy()  # Destroy the window
    root.quit()

# ---- DATA LOGGER -----
def save_to_csv(file_name, time_stamps, flux_values, temp_values, pressure_values):
    """
    Saves sensor data to a CSV file.

    Args:
        file_name (str): The name of the CSV file.
        time_stamps (list): List of timestamps.
        flux_values (list of lists): Flux values for CH1, CH2, CH3.
        temp_values (list of lists): Temperature values for CH1, CH2, CH3.
        pressure_values (list of lists): Pressure values for CH1, CH2, CH3.
    """
    # Combine data into rows
    rows = []
    for i in range(len(time_stamps)):
        row = [
            time_stamps[i],
            flux_values[i][0], flux_values[i][1], flux_values[i][2],
            temp_values[i][0], temp_values[i][1], temp_values[i][2],
            pressure_values[i][0], pressure_values[i][1], pressure_values[i][2],
        ]
        rows.append(row)

    # Write to the CSV file
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(["Time", "Flux1", "Flux2", "Flux3", "Temp1", "Temp2", "Temp3", "Pressure1", "Pressure2", "Pressure3"])
        # Write the rows
        writer.writerows(rows)
    print(f"Data successfully saved to {file_name}!")
    populate_table(file_name)

# ---- TABLE WIDGET ----
# https://www.tutorialspoint.com/table-of-widgets-in-python-with-tkinter
table_frame = tk.Frame(root)
table_frame.grid(row=10, column=3, columnspan=10)

headings = ["Time", "Flux1", "Flux2", "Flux3",
           "Temp1", "Temp2", "Temp3",
           "Pressure1", "Pressure2", "Pressure3"]
for x, heading in enumerate(headings):
    heading_table = Label(table_frame, text=heading)
    heading_table.grid(row=0, column=x, padx=10, pady=10)

def populate_table(file_name):
    """
    Populate the table with data from the CSV file.
    """
    # Path to the CSV file
    # csv_file = "sensor_data.csv"
    row_count = 0
    # Open the CSV file and read the data
    try:
        with open(file_name, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row

            # Add each row to the table
            for i, row in enumerate(reader, start=1):
                if row_count == 5:
                    row_count = 0
                for j, cell in enumerate(row):
                    if j != 0:
                        cell = float(cell)
                        text_cell = f"{cell:.2f}"
                    else:
                        text_cell = cell
                    cell_label = Label(table_frame, text=text_cell, font=("Arial", 10))
                    # print(cell)
                    cell_label.grid(row=row_count+1, column=j, padx=5, pady=5)
                row_count += 1
                
    except FileNotFoundError:
        error_label = Label(root, text="CSV file not found!", fg="red")
        error_label.grid(row=11, column=3, columnspan=10)
# button_switch = tk.Button(
#     root,
#     text="Mode: Auto",  # Start in manual mode
#     command=input_mode,
#     bg="lightgray",  # Initial background color
#     fg="black",        # Initial foreground color for manual mode
#     font=("Arial", 10),
#     width=20,
#     height=2
# )   
# button_switch.grid(row=2, column=1, padx=1, pady=1)
def status_widget(status_list):
    # Define status_text based on the status_list
    if "TRUE" in status_list:
        status_text = "TRIP"
        bg_color = "red"  # Red for TRIP
    else:
        status_text = "NORMAL"
        bg_color = "green"  # Green for NORMAL
    status_text = "STATUS:\n"+status_text
    
    # Create or update the status_frame container (Frame)
    if hasattr(status_widget, 'status_frame'):  # Check if status_frame exists
        status_widget.status_frame.config(bg=bg_color)  # Update background color of the frame
        status_widget.status_label.config(text=status_text, bg=bg_color)  # Update text and label background color
    else:
        # Create the status_frame (Frame) and status_label (Label) inside it
        status_widget.status_frame = tk.Frame(
            root, 
            background=bg_color,  # Set the background color of the frame
            bd=1,  # Border thickness
            relief="solid",  # Border style
        )
        status_widget.status_frame.grid(row=2, column=2, padx=1, pady=1)
        
        status_widget.status_label = tk.Label(
            status_widget.status_frame,  # Place label inside the frame
            text=status_text,
            font=("Courier", 12),  # Use a monospaced font for display-like effect
            fg="white",
            bg=bg_color,  # Set the background color of the label
            width=10,  # Set a fixed width for the display effect
            padx=10,  # Horizontal padding inside the label
            pady=5   # Vertical padding inside the label
        )
        status_widget.status_label.pack(padx=10, pady=5)  # Pack the label inside the frame



# status_widget()

# ---- INPUT CONTROL ----
# Initial values for manual sensor readings
manual_values_flux = [6e+6, 6e+6, 6e+6]
manual_values_temp = [500, 500, 500]
manual_values_pressure = [3, 3, 3]

history_flux = []           # List to store history data
history_temp = []
history_pressure = []
history_time = []
history_filename = "sensor_data.csv"

def control_auto():
    global list_reading_flux, list_reading_pressure, list_reading_temp
    global canvas_pressure, canvas_temp, canvas_flux
    global manual_values_pressure, manual_values_flux, manual_values_temp
    if is_auto:    
        list_reading_flux = list(np.random.uniform(range_flux[0], range_flux[1], size=3))
        list_reading_pressure = list(np.random.uniform(range_pressure[0], range_pressure[1], size=3))
        list_reading_temp = list(np.random.uniform(range_temp[0], range_temp[1], size=3))

        list_status = [logic_processing(setpoint_flux, list_reading_flux),
                       logic_processing(setpoint_temp, list_reading_temp),
                       logic_processing(setpoint_pres, list_reading_pressure)]
        status_widget(list_status)
        history_flux.append(list_reading_flux)
        # history_flux = list_reading_flux
        history_temp.append(list_reading_temp)
        # history_temp = list_reading_temp
        history_pressure.append(list_reading_pressure)
        # history_pressure =list_reading_pressure
        history_time.append(time.strftime('%H:%M:%S'))

        update_plot_data(list_reading_flux, list_reading_temp, list_reading_pressure)
        # save_to_csv("sensor_data.csv", )
        # time_stamps.append(len(time_stamps))
        # update_graph()
        if len(time_stamps) % 1 == 0:  # Save every 10 data points
            save_to_csv(history_filename, history_time, history_flux, history_temp, history_pressure)

        bar_widget("flux", canvas_flux, min_flux, max_flux,
                setpoint_flux,
                column=0, row=1,
                list_reading=list_reading_flux)
        alarm_button_widget("flux", list_status[0])

        bar_widget("temp", canvas_temp, min_temp, max_temp,
                setpoint_temp,
                column=1, row= 1,
                list_reading=list_reading_temp)
        alarm_button_widget("temp", list_status[1])

        bar_widget("pressure", canvas_pressure, min_pressure, max_pressure,
            setpoint_pres,
            column=2, row= 1,
            list_reading=list_reading_pressure)
        alarm_button_widget("pressure", list_status[2])

        manual_values_temp = list_reading_temp
        manual_values_flux = list_reading_flux
        manual_values_pressure = list_reading_pressure


        # if list_status any "TRUE" --> "TRIP" display

        root.after(750, control_auto)  # Schedule the next call (500 ms delay)
    # return list_reading_flux, list_reading_temp, list_reading_pressure
    
    # else:

def update_manual_values(sensor, channel, plus):
    """
    Updates the manual values for the specified sensor and channel.
    sensor: 'flux', 'temp', 'pressure'
    channel: 0, 1, 2 (for CH1, CH2, CH3)
    plusmin: True to increase, False to decrease
    """
    global manual_values_flux, manual_values_temp, manual_values_pressure
    value_range = {
        "flux": range_flux,
        "temp": range_temp,
        "pressure": range_pressure
    }
    values = {
        "flux": manual_values_flux,
        "temp": manual_values_temp,
        "pressure": manual_values_pressure
    }

    step = (value_range[sensor][1] - value_range[sensor][0]) / 50  # Step size
    if plus:
        values[sensor][channel] = min(values[sensor][channel] + step, value_range[sensor][1])
    else:
        values[sensor][channel] = max(values[sensor][channel] - step, value_range[sensor][0])
    
    # Update the widget
    if sensor == "flux":
        bar_widget("flux", canvas_flux, min_flux, max_flux, 
                   setpoint_flux, column=0, row=1, 
                   list_reading=manual_values_flux)
        alarm_button_widget("flux", logic_processing(setpoint_flux, manual_values_flux))
    elif sensor == "temp":
        bar_widget("temp", canvas_temp, min_temp, max_temp, 
                   setpoint_temp, column=1, row=1, 
                   list_reading=manual_values_temp)
        alarm_button_widget("temp", logic_processing(setpoint_temp, manual_values_temp))
    elif sensor == "pressure":
        bar_widget("pressure", canvas_pressure, min_pressure, max_pressure, 
                   setpoint_pres, column=2, row=1, 
                   list_reading=manual_values_pressure)
        alarm_button_widget("pressure", logic_processing(setpoint_pres, manual_values_pressure))
    list_status = [logic_processing(setpoint_flux, list_reading_flux),
                       logic_processing(setpoint_temp, list_reading_temp),
                       logic_processing(setpoint_pres, list_reading_pressure)]
    status_widget(list_status)
    
    update_plot_data(manual_values_flux[:],
                     manual_values_temp[:],
                     manual_values_pressure[:])
    history_flux.append(list_reading_flux)
    # history_flux = list_reading_flux
    history_temp.append(list_reading_temp)
    # history_temp = list_reading_temp
    history_pressure.append(list_reading_pressure)
    # history_pressure =list_reading_pressure
    history_time.append(time.strftime('%H:%M:%S'))

    if len(time_stamps) % 1 == 0:  # Save every 10 data points
            save_to_csv(history_filename, history_time, history_flux, history_temp, history_pressure)

    # print(manual_values_flux)

def control_manual():
    """
    Creates manual control buttons for each sensor and channel.
    """
    for sensor, column in zip(["flux", "temp", "pressure"], [0, 1, 2]):
        for channel in range(3):
            frame = Frame(root)
            frame.grid(row=3 + channel, column=column, pady=5)

            # Decrease button
            Button(frame, text="-", command=lambda s=sensor, ch=channel: update_manual_values(s, ch, False)).grid(row=0, column=0)
            
            # Label for channel
            Label(frame, text=f"CH{channel + 1}").grid(row=0, column=1)
            
            # Increase button
            Button(frame, text="+", command=lambda s=sensor, ch=channel: update_manual_values(s, ch, True)).grid(row=0, column=2)

def input_mode():
    # Alt:
    # global is_auto
    # is_auto = not is_auto
    # button_switch.config(
    #     text="Mode: Automatic" if is_auto else "Mode: Manual",
    #     bg="green" if is_auto else "lightgray",
    # )
    # control_mode()
    
    global is_auto, button_switch
    if is_auto: # MANUAL
        # insert action
        button_switch.config(text="Mode: Manual", fg="black", bg="yellow")
        is_auto = False
        control_manual()
        print("Mode: Manual")
    else: #AUTO
        # action
        button_switch.config(text="Mode: Automatic", fg="white", bg="purple")
        is_auto = True
        control_auto()
        print("Mode: Auto")
    

def initial_bar(canvas, min, max,
               setpoint,
               column, row):
    # canvas.delete("all")
    channel_color = "red"
    setpoint_line = y2 - ((setpoint-min)/(max-min)) * height

    canvas.create_text(x1+(bar_width/2),y1-10, 
                        text="CH1", fill=channel_color, 
                        anchor="center")
    canvas.create_rectangle( # border for channel 1
                            x1, y1, x2, y2,
                            outline="black") 
    
    canvas.create_text(x1+(bar_width/2) +space,y1-10, 
                        text="CH2", fill=channel_color, 
                        anchor="center")
    canvas.create_rectangle( # border for channel 2
                            x1+space, y1, x2+space, y2,
                            outline="black") 

    canvas.create_text(x1+(bar_width/2) +space*2,y1-10, 
                        text="CH3", fill=channel_color, 
                        anchor="center")
    canvas.create_rectangle( # border for channel 3
                            x1+(space*2), y1, 
                            x2+(space*2), y2,
                            outline="black") 
    
    canvas.create_line( # setpoint line
                        x1 - 10, setpoint_line, 
                        x2 + (space*2) + 10, 
                        setpoint_line, 
                        fill="black", dash=(2, 2))
    canvas.create_text( x1 - 30, setpoint_line, 
                       text=f"SP:\n{setpoint}", 
                       fill="red", anchor="center"
    )

    canvas.grid(row=row, column=column, padx=0, pady=0)

# ----- SIMULATION ACTIVATION -------
# -----Canvas 1: FLUX-----
canvas_flux = Canvas(root, width=canvas_width, height=canvas_height, bg="white")
initial_bar(canvas_flux, min_flux, max_flux, setpoint_flux,
            0, 1)
alarm_button_widget("flux", "FALSE")

# ---- CANVAS 2: TEMPERATURE ----
canvas_temp = Canvas(root, width=canvas_width, height=canvas_height, bg="white")
initial_bar(canvas_temp, min_temp, max_temp, setpoint_temp,
            1,1)
alarm_button_widget("temp", "FALSE")

# ---- CANVAS 3: PRESSURE ----
canvas_pressure = Canvas(root, width=canvas_width, height=canvas_height, bg="white")
initial_bar(canvas_pressure, min_pressure, max_pressure, setpoint_pres,
            2,1)
alarm_button_widget("pressure", "FALSE")

# ---- ALARM WIDGET ----
canvas_logic = Canvas(root, width=canvas_width, height=canvas_height, bg="white")

# ---- CONTROL WIDGET ----
# canvas_switch = Canvas(root, width=canvas_width, height=canvas_height, bg="white")
# canvas_switch.create_rectangle(x1, )
is_auto = True
control_auto()
button_switch = tk.Button(
    root,
    text="Mode: Auto",  # Start in manual mode
    command=input_mode,
    bg="lightgray",  # Initial background color
    fg="black",        # Initial foreground color for manual mode
    font=("Arial", 10),
    width=20,
    height=3
)   
button_switch.grid(row=2, column=1, padx=1, pady=1)
# canvas_switch.bind("<Button-1>", lambda event: input_mode())

# ---- GRAPH WIDGET ----
# Add buttons for Reset and Start
# reset_button = tk.Button(root, text="Reset", command=reset_data)
# reset_button.grid(row=2, column=2, pady=10, padx=10)

# start_button = tk.Button(root, text="Start", command=start_updating)
# start_button.grid(row=2, column=3, pady=10, padx=10)

# Bind the window close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the dynamic updating
# update_plot_data()


# Run the tkinter event loop
root.mainloop()
