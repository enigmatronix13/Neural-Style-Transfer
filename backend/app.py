import os
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load TensorFlow Hub model
hub_module = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

def load_image(image_path, max_dim=512):
    """Loads an image and converts it to a float32 numpy array."""
    img = Image.open(image_path).convert('RGB')
    img = np.array(img)
    img = tf.image.resize(img, (max_dim, max_dim)).numpy()
    img = img.astype(np.float32)[np.newaxis, ...] / 255.0
    return img

@app.route('/style-transfer', methods=['POST'])
def style_transfer():
    if 'content_image' not in request.files or 'style_image' not in request.files:
        return jsonify({'error': 'Please upload both content and style images'}), 400

    content_file = request.files['content_image']
    style_file = request.files['style_image']

    # Save uploaded files
    content_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(content_file.filename))
    style_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(style_file.filename))
    content_file.save(content_path)
    style_file.save(style_path)

    # Process images
    content_image = load_image(content_path)
    style_image = load_image(style_path, max_dim=256) 

    # Perform style transfer
    outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
    stylized_image = outputs[0].numpy()

    # Save the result
    result_path = os.path.join(app.config['UPLOAD_FOLDER'], 'stylized_image.png')
    stylized_image = (stylized_image * 255).astype(np.uint8)
    result_image = Image.fromarray(stylized_image[0])
    result_image.save(result_path)

    return send_file(result_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
