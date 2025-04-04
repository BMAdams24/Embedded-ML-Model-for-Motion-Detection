import time
import numpy as np
from sense_hat import SenseHat
import tflite_runtime.interpreter as tflite

# Load the TensorFlow Lite model
interpreter = tflite.Interpreter(model_path="windowNN_model.tflite")
interpreter.allocate_tensors()

# Get input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Initialize SenseHat
sense = SenseHat()

# Function to get gyro and accel data from SenseHat
def get_sensor_data():
    gyro = sense.get_gyroscope_raw()
    accel = sense.get_accelerometer_raw()
    return [gyro['x'], gyro['y'], gyro['z'], accel['x'], accel['y'], accel['z']]

# Function to prepare data for inference
def prepare_data(window_size=100):
    data = []
    for _ in range(window_size):
        sensor_data = get_sensor_data()
        data.append(sensor_data)
        time.sleep(0.01)  # Adjust the sleep time as needed to match the sampling rate
    return np.array(data).reshape(1, window_size, 6)

# Function to perform inference
def perform_inference():
    input_data = prepare_data()
    interpreter.set_tensor(input_details[0]['index'], input_data.astype(np.float32))
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    return output_data
# Function to update SenseHat color based on prediction
def update_sensehat_color(prediction):
    # Define colors
    colors = {
        0: (0, 0, 255),    # Blue for sitting
        1: (255, 255, 0),  # Yellow for standing
        2: (0, 255, 0),    # Green for walking
        3: (255, 0, 0)     # Red for falling
    }
    # Get the predicted class
    predicted_class = np.argmax(prediction)
    # Set the SenseHat color
    sense.clear(colors[predicted_class])

# Perform inference and print the result
while True:
    result = perform_inference()
    print("Inference result:", result)
    update_sensehat_color(result)
