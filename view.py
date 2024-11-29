import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from fontTools.misc.textTools import tostr
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pydub
import subprocess

selectedFile = None
convertedFile = "convert.wav"

# File selection
def browseFiles():
    global selectedFile
    selectedFile = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("Audio files", ".wav .mp3"), ("All Files","*.*")))

    # Change label contents
    fileLabel.configure(text="File name: "+selectedFile)

# File analyze
def analyzeFile():
    # Undefined selection check
    if selectedFile is None or len(selectedFile) == 0:
        print("File undefined")
        return

    # Convert from mp3 to wav (THIS DOESN'T WORK?)
    sound = pydub.AudioSegment.from_mp3(selectedFile)
    sound.export(convertedFile, format="wav")

    #Check and handle meta/2chan

    # Display Duration
    lengthLabel.configure(text=f"File Length = {sound.duration_seconds:.2f}s")

    # Generate Plots
    ## Waveform
    ## RT60 Low, Medium, High

# Main window
window = tk.Tk()
window.title("Interactive Data Acoustic Modeling")
window.geometry("750x750")

# File select button
fileSelectButton = tk.Button(window, text="Open a File", width=25, command=browseFiles)
fileSelectButton.pack()

# File name
fileLabel = tk.Label(window, text="File name: ")
fileLabel.pack()

# File analyze button
fileAnalyzeButton = tk.Button(window, text="Analyze File", width=25, command=analyzeFile)
fileAnalyzeButton.pack()

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