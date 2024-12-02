import matplotlib.pyplot as plt
import wave
from scipy.io import wavfile
import numpy as np

convertedFileLocation = "convert.wav"

class GraphHandler:
    def __init__(self, canvas):
        self.canvas = canvas
        self.currentFreq = "high"
        self.sampleRate = None
        self.data = None
        self.freqs = None
        self.t = None

    # Draw and display waveform plot
    def drawWaveformPlot(self):
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
        self.canvas.draw()
        # Reset RT60 graph cycle
        self.currentFreq = "high"

    # Draw and display intensity plot
    def drawIntensityPlot(self):
        # Clear canvas
        plt.clf()

        # Spectrum Setup
        self.sampleRate, self.data = wavfile.read(convertedFileLocation)
        spectrum, freqs, t, im = plt.specgram(self.data, Fs=self.sampleRate, \
                                              NFFT=1024, cmap=plt.get_cmap('autumn_r'))

        # Set Plot & Axis Titles
        cbar = plt.colorbar(im)
        plt.title("Intensity Graph")
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        cbar.set_label('Intensity (dB)')
        self.canvas.draw()

        # Reset RT60 graph cycle
        self.currentFreq = "high"

    # RT60 Plots
    ## Helper Function
    def findTargetFrequency(self, type):
        if type == "low":
            for x in self.freqs:
             if x > 1000:
                    break
            return x
        elif type == "mid":
            for x in self.freqs:
             if 1000 < x > 10000:
                    break
            return x
        elif type == "high":
            for x in self.freqs:
             if 10000 < x > 100000:
                    break
            return x

    ## Helper Function
    def frequencyCheck(self, type):
        sample_rate, data = wavfile.read(convertedFileLocation)
        plt.figure(2)
        spectrum, self.freqs, self.t, im = plt.specgram(data, Fs=sample_rate, \
                                              NFFT=1024, cmap=plt.get_cmap('autumn_r'))
        plt.figure(1)

        global targetFrequency
        targetFrequency = self.findTargetFrequency(type)
        indexOfFrequency = np.where(self.freqs == targetFrequency)[0][0]
        # Find sound data for a particular frequency
        data_for_frequency = spectrum[indexOfFrequency]
        # Change a digital signal for a values in decibels
        data_in_db_fun = 10 * np.log10(data_for_frequency)
        return data_in_db_fun

    ## Find a nearest value of less 5db, Helper Function
    def find_nearest_value(self, array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    # Draw and display RT60 plot types. If type is None, draw combined plot.
    def drawRT60Plot(self, type, dontClear):
        if type is not None:
            data_in_db = self.frequencyCheck(type)
            #plt.clf()

        # Clear canvas
        if dontClear == False:
            plt.clf()
        plt.figure(1)

        # Axis Title
        if type == "low":
            plt.title("Low RT60 Graph")
        elif type == "mid":
            plt.title("Middle RT60 Graph")
        elif type == "high":
            plt.title("High RT60 Graph")
        plt.xlabel('Time (s)')
        plt.ylabel('Power (dB)')

        # Find an index of a max value
        if type is not None:
            plt.plot(self.t, data_in_db, linewidth=1, alpha=0.7)

            index_of_max = np.argmax(data_in_db)
            value_of_max = data_in_db[index_of_max]
            plt.plot(self.t[index_of_max], data_in_db[index_of_max], 'go')

            # Slice our array from a max value
            sliced_array = data_in_db[index_of_max:]
            value_of_max_less_5 = value_of_max - 5

            value_of_max_less_5 = self.find_nearest_value(sliced_array, value_of_max_less_5)
            index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)
            plt.plot(self.t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo')

            # Slice array from a max-5db
            value_of_max_less_25 = value_of_max - 25
            value_of_max_less_25 = self.find_nearest_value(sliced_array, value_of_max_less_25)
            index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)
            plt.plot(self.t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro')

            rt20 = (self.t[index_of_max_less_5] - self.t[index_of_max_less_25])[0]
            rt60 = 3 * rt20
            plt.grid()

        if type is None:
            self.drawRT60Plot("low", True)
            self.drawRT60Plot("mid", True)
            self.drawRT60Plot("high", True)

            plt.title("Combined RT60 Graph")

        self.canvas.draw()

        # Return Difference
        if type is not None:
            return round(abs(rt60), 2)