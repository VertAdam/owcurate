# ======================================== IMPORTS ========================================
from Sensor.Accelerometer import *
from Sensor.Thermometer import *
from Sensor.Light import *
from Sensor.Button import *
from scipy.signal import butter, filtfilt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import statistics


# Sensor class adds a layer of modularity between sensor and person
# This class hopes to solve multi-sensor but uni-device problems such as nonwear
class Sensor:
    def __init__(self):
        self.metadata = {}
        self.accelerometer = None
        self.thermometer = None
        self.ecg = None
        self.light = None
        self.button = None
        self.non_wear_starts = []
        self.non_wear_ends = []

    def init_accelerometer(self):
        self.accelerometer = Accelerometer()

    def init_thermometer(self):
        self.thermometer = Thermometer()

    def init_light(self):
        self.light = Light()

    def init_button(self):
        self.button = Button()

    def generate_times(self, frequency, length):
        start_time = self.metadata["start_time"]
        return np.array([start_time + datetime.timedelta(seconds=i/frequency) for i in range(length)])


    def plot_accelerometer(self):
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    def VanHeesNonWear(self, window_len=5, mins=5):
        """
        This method calculates non-wear for any given GENEActiv device.
        Non-wear is characterized by extended periods of inactivity in accelerometer signal, paired by
            a rapid drop in overall temperature
        Args:
            min_duration:

        Returns:

        """

        # Checking for uninitialized values
        if self.accelerometer is None:
            raise Exception("Accelerometer has not been initialized")

        if self.thermometer is None:
            raise Exception("Thermometer has not been initialized")

        # ==================== Variable declaration and initialization
        epoch_len = self.accelerometer.frequency * window_len
        angles = []
        angles_diff = []
        start_indices = []
        end_indices = []
        x = []
        y = []
        z = []
        curr_stat = False

        # ==================== Main
        # Finding angle of accelerometer, using the "Novel way to determine sleep" method
        # Preliminary accelerometer-based checking

        # Gets median values for each period in the rolling window
        for i in range(0, len(self.accelerometer.x) - epoch_len, epoch_len):
            x.append(statistics.median(self.accelerometer.x[i:i + epoch_len]))
            y.append(statistics.median(self.accelerometer.y[i:i + epoch_len]))
            z.append(statistics.median(self.accelerometer.z[i:i + epoch_len]))

        # Gets angles for each period in the rolling window
        for i in range(len(x)):
            angles.append(math.atan(z[i] / math.sqrt(math.pow(x[i], 2) + math.pow(y[i], 2))) * 180 / math.pi)

        # Differentiates angles with respect to next sample
        angles_diff = np.diff(angles)
        angles_diff = np.append(angles_diff, 0)

        i = 0
        while i < len(angles_diff) - 1:
            if angles_diff[i] < 5:
                j = i
                while angles_diff[j] < 5 and j < len(angles_diff) - 1:
                    j += 1

                if j-i > (mins * 60 * 75 // epoch_len):
                    start_indices.append(i * epoch_len)
                    end_indices.append(j * epoch_len)
                i = j

            i += 1

        self.start_indices = start_indices
        self.end_indices = end_indices



    def Check_Temperature(self, window_len=5):
        # Temperature based checking
        self.non_wear_starts = []
        self.non_wear_ends = []
        for i in range(len(self.start_indices)):
            start_index = self.start_indices[i] // 300
            end_index = start_index + ((self.accelerometer.frequency * window_len * 60) // 300)
            indices = np.array([j for j in range(start_index, end_index)])
            curr_temps = np.array(self.thermometer.temperatures[start_index:end_index])
            m = (statistics.mean(curr_temps) * statistics.mean(indices) - statistics.mean(curr_temps * indices))

            if m > 10:
                self.non_wear_starts.append(self.start_indices[i])
                self.non_wear_ends.append(self.end_indices[i])

    def NonWear(self):
        """
        this method calculates non-wear times based on SVM calculations
        Args:
            min1:
            min2:

        Returns:

        """

        # Checking for uninitialized values
        if self.accelerometer is None:
            raise Exception("Accelerometer has not been initialized")

        if self.thermometer is None:
            raise Exception("Thermometer has not been initialized")

        # Find Variance per second
        f = []
        for i in range(0, len(self.accelerometer.svms), self.accelerometer.frequency):
            f.append(statistics.variance(self.accelerometer.svms[i:i+self.accelerometer.frequency]))

        # Filter
        filtered = lowpass_filter(abs(bandpass_filter(f, 15, 25, self.accelerometer.frequency, 3)), 3,
                                  self.accelerometer.frequency, 3)

        starts = []
        ends = []
        i = 0

        while i < len(filtered) - 1:
            if filtered[i] < 0.0005:
                j = i
                while filtered[j] < 0.0005 and j < len(filtered) - 1:
                    j += 1
                if j - i > 300:
                    starts.append(self.accelerometer.frequency * i)
                    ends.append(self.accelerometer.frequency * j)
                i = j
            i += 1


        # GAP COLLAPSING
        i = 0
        j = 0
        while i < (len(starts) - 1 - j):
            if starts[i + 1] - ends[i] < 300 * self.accelerometer.frequency:
                starts.remove(starts[i + 1])
                ends.remove(ends[i])
                j += 1
                i -= 1
            i += 1

        self.start_indices = starts
        self.end_indices = ends



# ======================================== HELPFUL FUNCTIONS ========================================
def bandpass_filter(dataset, lowcut, highcut, frequency, filter_order):
    # Filter characteristics
    nyquist_freq = 0.5 * frequency
    low = lowcut / nyquist_freq
    high = highcut / nyquist_freq
    b, a = butter(filter_order, [low, high], btype="band")
    y = filtfilt(b, a, dataset)
    return y


def lowpass_filter(dataset, lowcut, signal_freq, filter_order):
    """Method that creates bandpass filter to ECG data."""
    # Filter characteristics
    nyquist_freq = 0.5 * signal_freq
    low = lowcut / nyquist_freq
    b, a = butter(filter_order, low, btype="low")
    y = filtfilt(b, a, dataset)
    return y


def highpass_filter(dataset, highcut, signal_freq, filter_order):
    """Method that creates bandpass filter to ECG data."""
    # Filter characteristics
    nyquist_freq = 0.5 * signal_freq
    high = highcut / nyquist_freq
    b, a = butter(filter_order, high, btype="high")
    y = filtfilt(b, a, dataset)
    return y