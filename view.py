import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pydub
import wave
import numpy as np

# Files
srcFile = None
convertedFileLocation = "convert.wav"
# Plots
#f = plt.figure(1)

# Plots
def drawWaveformPlot():
    # Clear canvas
    plt.clf()

    # Plot and axis titles
    plt.title("Waveform Graph")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")

    # Plot data and display on canvas
    fig = plt.figure(1)
    spf = wave.open(convertedFileLocation, "r")
    fs = spf.getframerate()
    signal = np.fromstring(spf.readframes(-1), np.int16)
    plt.plot(np.linspace(0, len(signal) / fs, num=len(signal)), signal)
    fig.set_canvas(canvas)
    canvas.draw()

# File selection
def browseFiles():
    global srcFile
    srcFile = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("Audio files", ".wav .mp3"), ("All Files","*.*")))

    # Change label contents
    fileLabel.configure(text="File name: "+srcFile)

# File analyze
def analyzeFile():
    # Undefined selection check
    if srcFile is None or len(srcFile) == 0:
        print("File undefined")
        return

    # Convert from mp3 to wav, handle 2chan
    raw_audio = pydub.AudioSegment.from_mp3(srcFile)
    mono_audio = raw_audio.set_channels(1)
    mono_audio.export(convertedFileLocation, format="wav")

    currentSound = pydub.AudioSegment.from_mp3(convertedFileLocation)
    #Check and handle meta

    # Display Duration
    lengthLabel.configure(text=f"File Length = {currentSound.duration_seconds:.2f}s")

    # Generate Plots
    ## Waveform
    drawWaveformPlot()

    ## RT60 Low, Medium, High

# Tkinter UI
## Main window
window = tk.Tk()
window.title("Interactive Data Acoustic Modeling")
window.geometry("625x640")

## File select button
fileSelectButton = tk.Button(window, text="Open a File", width=18, command=browseFiles)

## File name
fileLabel = tk.Label(window, text="File name: ")

## File analyze button
fileAnalyzeButton = tk.Button(window, text="Analyze File", width=18, command=analyzeFile)

## Plots
global fig
fig = plt.figure(1)
canvas = FigureCanvasTkAgg(fig, master = window)

## File data
lengthLabel = tk.Label(window, text="File Length = 0s")
frequencyLabel = tk.Label(window, text="Resonant Frequency: __ Hz")
differenceLabel = tk.Label(window, text="Difference: _._s")

## Graph Types
IntensityGraphButton = tk.Button(window, text="Intensity Graph", width=17, command=window.destroy)
WaveformGraphButton = tk.Button(window, text="Waveform Graph", width=17, command=drawWaveformPlot)
CycleRT60Button = tk.Button(window, text="Cycle RT60 Graphs", width=17, command=window.destroy)
CombineRT60Button = tk.Button(window, text="Combine RT60 Graphs", width=17, command=window.destroy)

# Grid Layout
## File buttons
fileSelectButton.grid(row=0, column=0, padx=5, pady=10)
fileAnalyzeButton.grid(row=1, column=0, padx=5, pady=0)
## Info labels
fileLabel.grid(row=0, column=1, columnspan = 3, padx=0, pady=10, sticky=tk.W)
lengthLabel.grid(row=1, column=1, padx=0, pady=0, sticky=tk.W)
frequencyLabel.grid(row=1, column=2, padx=0, pady=0, sticky=tk.W)
differenceLabel.grid(row=1, column=3, padx=0, pady=0, sticky=tk.W)
## Graph
canvas.get_tk_widget().grid(row=3, column=0, columnspan=6, pady = 20)
## Graph buttons
IntensityGraphButton.grid(row=4, column=0)
WaveformGraphButton.grid(row=4, column=1)
CycleRT60Button.grid(row=4, column=2)
CombineRT60Button.grid(row=4, column=3)

window.mainloop()