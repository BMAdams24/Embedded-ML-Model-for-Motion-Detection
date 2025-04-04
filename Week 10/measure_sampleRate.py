from sense_hat import SenseHat
import time

# The goal of this script is to determine how quickly the RPi can sample
# from the gyroscope and accelerometer. It will start the timer, collect
# 1000 samples, and then stop the time. Sample rate is determined as
# number of samples / elapsed time. (3-2025, MEL)

# Initialize SenseHat
sense = SenseHat()

# Function to get gyro and accel data
def get_gyro_accel_data():
    gyro = sense.get_gyroscope_raw()
    accel = sense.get_accelerometer_raw()
    return gyro, accel

# Function to measure sampling rate
def measure_sampling_rate(num_samples):
    start_time = time.time()  # Record start time
    for _ in range(num_samples):
        get_gyro_accel_data()
    end_time = time.time()  # Record end time

    elapsed_time = end_time - start_time
    sampling_rate = num_samples / elapsed_time

    print(f"Collected {num_samples} samples in {elapsed_time:.2f} seconds.")
    print(f"Sampling rate: {sampling_rate:.2f} samples per second.")

# Measure sampling rate for 1000 samples
measure_sampling_rate(1000)
