import model
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pydub import AudioSegment
import numpy as np
from scipy.io import wavfile
from scipy.signal import welch

# Filesss
srcFile = None
convertedFileLocation = "convert.wav"


# Functions for Plots
def drawWaveformPlot():
    GraphHandler.drawWaveformPlot()


def drawIntensityPlot():
    GraphHandler.drawIntensityPlot()


def cycleFrequencies():
    GraphHandler.cycleRT60Graphs()


def combineRT60Graphs():
    GraphHandler.drawRT60Plot(None)


# File selection
def browseFiles():
    global srcFile
    srcFile = filedialog.askopenfilename(
        initialdir="/",
        title="Select a File",
        filetypes=(("Audio files", "*.wav *.mp3"), ("All Files", "*.*"))
    )
    if srcFile:
        fileLabel.configure(text=f"File name: {srcFile}")
    else:
        fileLabel.configure(text="No file selected")


# File analyzing
def analyzeFile():
    global srcFile
    if not srcFile or not srcFile.lower().endswith(('.wav', '.mp3')):
        print("Please select a valid .wav or .mp3 file.")
        return

    try:
        # Convert file to mono .wav if necessary
        audio = AudioSegment.from_file(srcFile)
        audio = audio.set_channels(1)
        audio.export(convertedFileLocation, format="wav")

        # Read the converted file
        sample_rate, data = wavfile.read(convertedFileLocation)

        # File information
        duration = len(data) / sample_rate
        lengthLabel.configure(text=f"File Length: {duration:.2f}s")

        # Resonant Frequency
        frequencies, power = welch(data, sample_rate, nperseg=4096)
        dominant_frequency = frequencies[np.argmax(power)]
        frequencyLabel.configure(text=f"Resonant Frequency: {round(dominant_frequency)} Hz")

        # RT60 Difference
        difference = GraphHandler.drawRT60Plot("mid")
        differenceLabel.configure(text=f"Difference: {difference}s")

        # Generate Waveform Plot
        GraphHandler.drawWaveformPlot()

    except Exception as e:
        print(f"Error processing file: {e}")
        fileLabel.configure(text="Error: Unable to analyze file")


# Tkinter UI
window = tk.Tk()
window.title("Interactive Data Acoustic Modeling")
window.geometry("625x640")

# UI
fileSelectButton = tk.Button(window, text="Open a File", width=18, command=browseFiles)
fileAnalyzeButton = tk.Button(window, text="Analyze File", width=18, command=analyzeFile)
fileLabel = tk.Label(window, text="No file selected")
lengthLabel = tk.Label(window, text="File Length: 0s")
frequencyLabel = tk.Label(window, text="Resonant Frequency: __ Hz")
differenceLabel = tk.Label(window, text="Difference: _._s")

fig = plt.figure(1)
canvas = FigureCanvasTkAgg(fig, master=window)

IntensityGraphButton = tk.Button(window, text="Intensity Graph", width=17, command=drawIntensityPlot)
WaveformGraphButton = tk.Button(window, text="Waveform Graph", width=17, command=drawWaveformPlot)
CycleRT60Button = tk.Button(window, text="Cycle RT60 Graphs", width=17, command=cycleFrequencies)
CombineRT60Button = tk.Button(window, text="Combine RT60 Graphs", width=17, command=combineRT60Graphs)

# UI
fileSelectButton.grid(row=0, column=0, padx=5, pady=10)
fileAnalyzeButton.grid(row=1, column=0, padx=5, pady=0)
fileLabel.grid(row=0, column=1, columnspan=3, padx=0, pady=10, sticky=tk.W)
lengthLabel.grid(row=1, column=1, padx=0, pady=0, sticky=tk.W)
frequencyLabel.grid(row=1, column=2, padx=0, pady=0, sticky=tk.W)
differenceLabel.grid(row=1, column=3, padx=0, pady=0, sticky=tk.W)
canvas.get_tk_widget().grid(row=3, column=0, columnspan=4, pady=20)
IntensityGraphButton.grid(row=4, column=0)
WaveformGraphButton.grid(row=4, column=1)
CycleRT60Button.grid(row=4, column=2)
CombineRT60Button.grid(row=4, column=3)

# Graph Handler
GraphHandler = model.GraphHandler(canvas)

# Start
window.mainloop()
