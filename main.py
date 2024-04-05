import csv
import scipy.fftpack
import matplotlib.pyplot as plt
import math
import numpy as np

voltage = []
time = []

base_freq = 440
freqs = [i * base_freq for i in range(10, 0, -1)]

with open('dump0/a0_1.csv') as file:
    data = csv.reader(file)
    for i, row in enumerate(data):
        if i < 3:
            continue 

        if i % 1_000 == 0:
            fields = str(row[0]).split(';')
            time.append(fields[0])
            voltage.append(fields[1])

freq = 1e3 / float(time[1])

fft = scipy.fftpack.fft(voltage)
x = np.linspace(0, freq * 2, len(fft))
fft_calculated = []
for chunck in fft:
     fft_calculated.append(20 * math.log10(abs(chunck)))


x_limit = []
y_limit = []

for i in range(1, len(x)):
    if x[i - 1] < freqs[-1] and x[i] > freqs[-1]:
        if len(freqs) == 1:
            break
        freqs.pop()
        x_limit.append(x[i])
        y_limit.append(fft_calculated[i])

plt.plot(x_limit, y_limit)
plt.show()
