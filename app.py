from flask import Flask, request, render_template
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Load your pre-trained deep fake analysis model
model = load_model('model_v2.h5')

@app.route('/')
def index():
    return render_template('VortexView.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    # Get the uploaded image file
    file = request.files['image']

    # Load and preprocess the image
    img_path = file.filename
    file.save(img_path)
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    # Pass the image through the model
    predictions = model.predict(img_array)[0][0]
    print(predictions)

    # Determine the result
    if predictions > 0.5:
        result = "Fake"
    else:
        result = "Real"

    # Render the results page
    return render_template('Resultpage.html', prediction=result,score=round(predictions*100,7))

if __name__ == '__main__':
    app.run(debug=True)