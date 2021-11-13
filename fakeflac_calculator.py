#!/usr/bin/python
# -*- coding: utf-8 -*-

# uncomment for debugging:
import matplotlib.pyplot as plt
import numpy
from scipy.fftpack import rfft
from scipy.io.wavfile import read
from scipy.signal import hann
import sys
import warnings

def moving_average(a, w):
    # calculate moving average
    window = numpy.ones(int(w)) / float(w)
    r = numpy.convolve(a, window, 'valid')
    # len(a) = len(r) + w
    a = numpy.empty((int(w / 2)))
    a.fill(numpy.nan)
    b = numpy.empty((int(w - len(a))))
    b.fill(numpy.nan)
    # add nan arrays to equal input and output length
    return numpy.concatenate((a, r, b))

def find_cutoff(a, dx, diff, limit):
    for i in range(1, int(a.shape[0] - dx)):
        if a[-i] / a[-1] > limit:
            break
        if a[int(-i - dx)] - a[-i] > diff:
            return a.shape[0] - i - dx
    return a.shape[0]

def CalculateFakeFlacValue(fileToProcess):
    # print usage if no argument given
    print(fileToProcess)
    if fileToProcess == '':
        return -1

    # read audio samples and ignore warnings, print errors
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            input_data = fileToProcess
    except IOError as e:
        print(e[1])
        return -1

    # process data
    freq = input_data[0]
    audio = input_data[1]
    channel = 0
    samples = len(audio[:, 0])
    seconds = int(samples / freq)
    seconds = min(seconds, 30)
    spectrum = [0] * freq

    # run over the seconds (max 30)
    for t in range(0, seconds - 1):
        # apply hanning window
        window = hann(freq)
        audio_second = audio[t * freq:(t + 1) * freq, channel] * window
        # do fft to add second to frequency spectrum
        spectrum += abs(rfft(audio_second))

    # calculate average of the spectrum
    spectrum /= seconds
    # normalize frequency spectrum
    spectrum = numpy.lib.scimath.log10(spectrum)
    # smoothen frequency spectrum with window w
    spectrum = moving_average(spectrum, freq / 100)
    # find cutoff in frequency spectrum
    cutoff = find_cutoff(spectrum, freq / 50, 1.25, 1.1)
    # print percentage of frequency spectrum before cutoff
    out = (int((cutoff * 100) / freq))
    print(out)
    return out

'''
if out == 100:
  sys.exit(0)
else:
  sys.exit(1)

# debugging only:
if 'plt' in globals():
  # plot
  plt.plot(spectrum)
  # label the axes
  plt.ylabel('Magnitude')
  plt.xlabel('Frequency')
  # set the title
  plt.title('Spectrum')
  plt.axis((0, 45000, 0, 10))
  plt.show()
'''

