from flask import Flask, request, render_template, redirect, url_for, flash, session
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.models import load_model
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flash messages and sessions

# Load your pre-trained deep fake analysis model
model = load_model('model_v2.h5')

# Simple user storage (replace with database in production)
users = {}

@app.route('/')
def index():
    return render_template('VortexView.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    if email in users and users[email]['password'] == password:
        session['user'] = email
        flash('Successfully logged in!', 'success')
        return redirect(url_for('index'))
    
    flash('Invalid credentials!', 'error')
    return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    
    if email in users:
        flash('Email already registered!', 'error')
        return redirect(url_for('index'))
    
    if password != confirm_password:
        flash('Passwords do not match!', 'error')
        return redirect(url_for('index'))
    
    users[email] = {
        'name': name,
        'password': password
    }
    
    flash('Registration successful! Please login.', 'success')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Successfully logged out!', 'success')
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'user' not in session:
        flash('Please login to analyze images!', 'error')
        return redirect(url_for('index'))
        
    if 'image' not in request.files:
        flash('No image uploaded!', 'error')
        return redirect(url_for('index'))
        
    file = request.files['image']
    
    if file.filename == '':
        flash('No selected file!', 'error')
        return redirect(url_for('index'))
        
    if file:
        # Create uploads directory if it doesn't exist
        uploads_dir = os.path.join(app.static_folder, 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        
        # Save and process the image
        img_path = os.path.join(uploads_dir, file.filename)
        file.save(img_path)
        
        # Process image
        img = image.load_img(img_path, target_size=(128, 128))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0

        # Get prediction
        predictions = model.predict(img_array)[0][0]
        result = "Fake" if predictions > 0.5 else "Real"
        
        return render_template('Resultpage.html', 
                             prediction=result,
                             score=round(predictions*100, 7),
                             image_path=os.path.join('uploads', file.filename))

if __name__ == '__main__':
    app.run(debug=True)