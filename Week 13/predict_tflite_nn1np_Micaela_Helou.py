import numpy as np
from sense_hat import SenseHat
import tflite_runtime.interpreter as tflite

# Initialize SenseHat
sense = SenseHat()

# Load the TensorFlow Lite model
interpreter = tflite.Interpreter(model_path="nn_model_raw_1np.tflite")
interpreter.allocate_tensors()

# Get input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Function to get gyro/accel data from SenseHat
def get_gyro_accel_data():
    accel = sense.get_accelerometer_raw()
    gyro = sense.get_gyroscope_raw()
    data = np.array([accel['x'], accel['y'], accel['z'], gyro['x'], gyro['y'], gyro['z']])
    return data

# Function to make a prediction based on gyro/accel data
def predict(data):
    # Preprocess the data to match the input shape of the model
    data = data.reshape((1,6)).astype(np.float32)
    
    # Set the tensor to point to the input data to be inferred
    interpreter.set_tensor(input_details[0]['index'], data)
    
    # Run inference
    interpreter.invoke()
    
    # Get the prediction results
    output_data = interpreter.get_tensor(output_details[0]['index'])
    prediction = np.argmax(output_data)
    
    return prediction

# Function to update LED matrix based on prediction
def update_led_matrix(prediction):
    if prediction == 0:
        color = (0, 0, 255)  # Blue for sitting
        print("Sitting")
    elif prediction == 1:
        color = (255, 255, 0)  # Yellow for standing
        print("Standing")
    elif prediction == 2:
        color = (0, 255, 0)  # Green for walking
        print("Walking")
    elif prediction == 3:
        color = (255, 0, 0)  # Red for falling
        print("Falling")
    
    # Update LED matrix with the color
    sense.clear(color)

# Main loop to continuously get data, make predictions, and update LED matrix
window_size = 1
data_window = []

while True:
    data = get_gyro_accel_data()
    prediction = predict(data)
    update_led_matrix(prediction)
