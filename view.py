import tkinter as tk
import matplotlib.pyplot as plt
#from matplotlib.backends.backend_gtk4 import FigureCanvasGTK4
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Main window
window = tk.Tk()
window.title("Interactive Data Acoustic Modeling")
window.geometry("750x700")

# File select button
fileButton = tk.Button(window, text="Open a File", width=25, command=window.destroy)
fileButton.pack()

# File name
fileLabel = tk.Label(window, text="File name: ")

# Plots
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master = window)
canvas.get_tk_widget().pack()

# File data
lengthLabel = tk.Label(window, text="File Length = 0s")
frequencyLabel = tk.Label(window, text="Resonant Frequency: __ Hz")
differenceLabel = tk.Label(window, text="Difference: _._s")
lengthLabel.pack()
frequencyLabel.pack()
differenceLabel.pack()

#Graph Types
IntensityGraphButton = tk.Button(window, text="Intensity Graph", width=25, command=window.destroy)
WaveformGraphButton = tk.Button(window, text="Waveform Graph", width=25, command=window.destroy)
CycleRT60Button = tk.Button(window, text="Cycle RT60 Graphs", width=25, command=window.destroy)
CombineRT60Button = tk.Button(window, text="Combine RT60 Graphs", width=25, command=window.destroy)
IntensityGraphButton.pack()
WaveformGraphButton.pack()
CycleRT60Button.pack()
CombineRT60Button.pack()

#Grid layout (UNUSED ATM)
#IntensityGraphButton.grid(row=0, column=0)
#WaveformGraphButton.grid(row=0, column=1)
#CycleRT60Button.grid(row=1, column=0, columnspan=2)
#CombineRT60Button.grid(row=1, column=0, columnspan=2)

window.mainloop()