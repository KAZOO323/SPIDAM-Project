import tkinter as tk
from itertools import cycle
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pydub
import wave
import numpy as np
from scipy.io import wavfile
from scipy.signal import welch


# Files
srcFile = None
convertedFileLocation = "convert.wav"

# Plots
## Waveform
def drawWaveformPlot():
    # Clear canvas
    plt.clf()

    # Plot and axis titles
    plt.title("Waveform Graph")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")

    # Plot data and display on canvas
    spf = wave.open(convertedFileLocation, "r")
    fs = spf.getframerate()
    signal = np.fromstring(spf.readframes(-1), np.int16)
    plt.plot(np.linspace(0, len(signal) / fs, num=len(signal)), signal)
    canvas.draw()
    # Reset RT60 graph cycle
    global currentFreq
    currentFreq = "high"

## Low RT60
def drawLowFreq():
    # Clear canvas
    plt.clf()

    # Axis titles
    plt.title("Low RT60 Graph")
    plt.xlabel("Time (s)")
    plt.ylabel("Power (DB)")

    # Get frequency data
    sr, data = wavfile.read(convertedFileLocation)
    n = len(data)
    fft_result = np.fft.fft(data)
    freqs = np.fft.fftfreq(n, d=1 / sr)
    indices = np.where((freqs >= 0) & (freqs < 15))

    # Plot frequency data and display
    plt.plot(freqs[indices], data[indices])
    canvas.draw()

## Mid RT60
def drawMidFreq():
    # Clear canvas
    plt.clf()

    # Axis titles
    plt.title("Mid RT60 Graph")
    plt.xlabel("Time (s)")
    plt.ylabel("Power (DB)")

    # Get frequency data
    sr, data = wavfile.read(convertedFileLocation)
    n = len(data)
    fft_result = np.fft.fft(data)
    freqs = np.fft.fftfreq(n, d=1 / sr)
    indices = np.where((freqs >= 15) & (freqs < 1500))

    # Plot frequency data and display
    plt.plot(freqs[indices], data[indices])
    canvas.draw()

## High RT60
def drawHighFreq():
    # Clear canvas
    plt.clf()

    # Axis titles
    plt.title("High RT60 Graph")
    plt.xlabel("Time (s)")
    plt.ylabel("Power (DB)")

    # Get frequency data
    sr, data = wavfile.read(convertedFileLocation)
    n = len(data)
    fft_result = np.fft.fft(data)
    freqs = np.fft.fftfreq(n, d=1 / sr)
    indices = np.where((freqs >= 1500) & (freqs < 15000))

    # Plot frequency data and display
    plt.plot(freqs[indices], data[indices])
    canvas.draw()

currentFreq = "high"
## Cycles between RT60 graphs
def cycleFrequencies():
    global currentFreq
    if currentFreq == "low":
        currentFreq = "mid"
        drawMidFreq()
    elif currentFreq == "mid":
        currentFreq = "high"
        drawHighFreq()
    elif currentFreq == "high":
        currentFreq = "low"
        drawLowFreq()

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

    # Generate waveform plot
    drawWaveformPlot()
    # Define and display Resonant Frequency
    sample_rate, data = wavfile.read(convertedFileLocation)
    frequencies, power = welch(data, sample_rate, nperseg=4096)
    dominant_frequency = frequencies[np.argmax(power)]
    frequencyLabel.configure(text=f"Resonant Frequency: {round(dominant_frequency)} Hz")

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
CycleRT60Button = tk.Button(window, text="Cycle RT60 Graphs", width=17, command=cycleFrequencies)
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