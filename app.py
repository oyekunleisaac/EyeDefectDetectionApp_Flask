from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from PIL import Image
import os
from werkzeug.utils import secure_filename
import tensorflow as tf
import numpy as np




app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
model = tf.keras.models.load_model('model.h5')

def process_image(image):
    # Preprocess the image as needed
    # Example: Resize the image to the required input shape
    image = image.resize((299, 299))
    image = np.array(image)
    image = image / 255.0  # Normalize pixel values to the range [0, 1]
    image = np.expand_dims(image, axis=0)  # Add a batch dimension
    return image

def detect_eye_defect(image):
    # Perform eye defect detection using the loaded model
    # Example: Make predictions on the image using the model
    predictions = model.predict(image)
    # Process the predictions and return the results
    return predictions

def determine_eye_defect(predictions, threshold=0.5):
    max_prediction = np.max(predictions)
    if max_prediction >= threshold:
        return "Eye defect is present, seek medical help."
    else:
        return "Congratulations! No eye defect detected"


def get_defect_label(index):
    # Map the defect index to the corresponding label
    labels = ["Defect A", "Defect B", "Defect C", "Defect D"]
    return labels[index]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('image')
        if file:
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)
            image = Image.open(image_path)
            processed_image = process_image(image)
            predictions = detect_eye_defect(processed_image)
            conclusion = determine_eye_defect(predictions)
            return render_template('result.html', conclusion=conclusion)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

