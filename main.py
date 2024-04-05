import csv
import scipy.fftpack
import matplotlib.pyplot as plt
import math
import numpy as np


class guitar_fft:
    time = []
    voltage = []
    harmonics = []
    x = []
    y = []

    def read_dataframe(self, path: str, dec: int = 1):
        # Open the expected pandas dataframe
        with open(path) as file:
            data = csv.reader(file)
            for i, row in enumerate(data):
                # Skip the first 3 rows that are used for column definition in Picoscope
                if i < 3:
                    continue 

                # Decimate the data by a factor of 1'000
                if i % dec == 0:
                    # Split the time and voltage fields and append it to their arrays
                    fields = str(row[0]).split(';')
                    self.time.append(fields[0])
                    self.voltage.append(fields[1])

    def calc_harmonics(self, base: int, num: int):
        # Caclculate the reversed harmonics of a base freq
        self.harmonics = [i * base for i in range(num, 0, -1)]

    def calc_fft(self):
        # Calculate the frequency with wich is beeing meassured
        freq = 1e3 / float(self.time[1])

        # Make the actuall fft
        fft = scipy.fftpack.fft(self.voltage)

        # Calculate the x_axis with the appropriate step in greqency
        self.x = np.linspace(0, freq * 2, len(fft))

        # Calculate the abs of the fft
        for chunck in fft:
             self.y.append(20 * math.log10(abs(chunck)))

    def extract_harmonics_from_fft(self):
        # Copy the full fft_results
        x_copy = self.x
        y_copy = self.y
        # Reset output
        self.x = []
        self.y = []

        for i in range(1, len(x_copy)):
            # If the current smallest harmonics is in range of two meassured frequencies
            if x_copy[i - 1] < self.harmonics[-1] and x_copy[i] > self.harmonics[-1]:
                # Append the frequency and amplitude to the new data
                self.x.append(x_copy[i])
                self.y.append(y_copy[i])
                # Remove harmonics from array and stop if now harmonics are left
                self.harmonics.pop()
                if len(self.harmonics) == 0:
                    break

    def plot_results(self):
        plt.plot(self.x, self.y)
        plt.title("FFT Analysys")
        plt.xlabel("Frequency [Hz]")
        plt.ylabel("Amplitude [mW]")
        plt.show()


if __name__ == '__main__':
    fft_instance = guitar_fft()
    # Replace with your csv data, the code works for the csv output from Picoscope
    fft_instance.read_dataframe('dump0/a0_1.csv')
    # Change the base frequency to your desire: here 440 Hz: a 
    fft_instance.calc_harmonics(440, 10)    
    fft_instance.calc_fft()
    fft_instance.extract_harmonics_from_fft()
    fft_instance.plot_results()

