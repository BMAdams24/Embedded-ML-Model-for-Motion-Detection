from sense_hat import SenseHat
import time
import csv

# This scripts repeatedly samples (1000) from the SenseHat gyroscope 
# and acceleromter. It is set up so that it can be intuitively labeled DURING
# acquisition as indicated by the color on the LED matrix on the SenseHat.
# For example, for data acquisition during a Sitting posture, the LED matrix
# should show the color blue. Data collected during this time, will be labeled
# accordingly and saved in a CSV file on the RPi. (3-2025, MEL)


# Initialize SenseHat
sense = SenseHat()

# Function to get gyro and accel data
def get_gyro_accel_data():
    gyro = sense.get_gyroscope_raw()
    accel = sense.get_accelerometer_raw()
    return gyro, accel

# Function to write data to a file
def write_data_to_file(filename, data):
    with open(filename, 'w') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(['Index', 'Gyro_X', 'Gyro_Y', 'Gyro_Z', 'Accel_X', 'Accel_Y', 'Accel_Z', 'Label'])
        # Write data
        for row in data:
            writer.writerow(row)

# Main function to record data for each activity
def record_data(activity, color, label):
    total_measurements = 1000
    filename = f'gyro_accel_data_{activity}.csv'
    data = []

    print(f"Beginning measurement for {activity}")
    sense.clear(color)  # Turn LED panel to the activity color
    time.sleep(2)  # Delay before acquisition

    for i in range(total_measurements):
        index = i + 1
        print(index)
        gyro, accel = get_gyro_accel_data()
        data.append([
            index,
            gyro['x'], gyro['y'], gyro['z'],
            accel['x'], accel['y'], accel['z'],
            label
        ])
        time.sleep(0.1)  # Delay between measurements

    sense.clear()  

    write_data_to_file(filename, data)
    print(f"Data recording complete for {activity}. Data saved to {filename}")

# Run the main function for each activity
record_data('Sitting', (0, 0, 255), 0)   # Blue for Sitting
record_data('Standing', (255, 255, 0), 1) # Yellow for Standing
record_data('Walking', (0, 255, 0), 2)   # Green for Walking
record_data('Falling', (255, 0, 0), 3)   # Red for Falling
