import os
import json
from PIL import Image
import numpy as np
import tensorflow as tf
import streamlit as st

# Custom CSS for a natural green theme and potato field background
page_bg_img = '''
<style>
html, body, .stApp {
    background-image: url("data:image/jpeg;base64,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"); 
    background-size: cover; /* Ensures the image covers the entire screen */
    background-position: center; /* Centers the image */
    background-repeat: no-repeat; /* Prevents the image from repeating */
    background-attachment: fixed; /* Keeps the image fixed while scrolling */
    color: #1B5E20;  /* Deep green for text */
    height: 100%;
    margin: 0;
    padding: 0;
}

h1 {
    color: #1B5E20;  /* Deep green */
    text-align: center;
    font-size: 2.5em;
    font-weight: bold;
    text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.7);  /* White shadow for better readability */
}

.stButton>button {
    background-color: #388E3C !important; /* Darker green */
    color: white !important;
    border-radius: 10px;
    padding: 12px 20px;
    font-size: 1em;
    font-weight: bold;
    border: none;
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);  /* Subtle shadow */
}

.stButton>button:hover {
    background-color: #2E7D32 !important; /* Slightly darker green on hover */
}

.stFileUploader {
    border: 2px solid #81C784;  /* Light green */
    background-color: rgba(255, 255, 255, 0.9);  /* Slightly opaque white */
    border-radius: 10px;
    padding: 10px;
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);  /* Subtle shadow */
}

.stMarkdown {
    color: #1B5E20;  /* Deep green for text */
}

.stSuccess {
    background-color: #C8E6C9 !important;  /* Light green for success messages */
    color: #1B5E20 !important;  /* Deep green text */
    border-radius: 10px;
    padding: 10px;
    border: 1px solid #81C784;  /* Light green border */
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Streamlit App Title
st.title('🥔🍃 **Potato Disease Classifier** 🍃🥔')

# Get the working directory
working_dir = os.path.dirname(os.path.abspath(__file__))

# Define model and class indices paths correctly
model_path = os.path.join(working_dir, "models", r"C:\Users\vasan\Downloads\final_year\models\plant_disease_model.keras")
class_indices_path = os.path.join(working_dir, r"C:\Users\vasan\Downloads\final_year\classes_indexes.json")

# Load the pre-trained model
model = tf.keras.models.load_model(model_path)

# Load the class indices
with open(class_indices_path, "r") as f:
    class_indices = json.load(f)

# Function to preprocess image
def load_and_preprocess_image(image, target_size=(224, 224)):
    img = image.resize(target_size)  # Resize image
    img_array = np.array(img)  # Convert to numpy array
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = img_array.astype('float32') / 255.  # Normalize
    return img_array

# Function to predict image class
def predict_image_class(model, image, class_indices):
    preprocessed_img = load_and_preprocess_image(image)
    predictions = model.predict(preprocessed_img)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    predicted_class_name = class_indices[str(predicted_class_index)]
    return predicted_class_name

# Upload image
uploaded_image = st.file_uploader("🌿 Upload a potato leaf image for classification...", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)  # Open image
    col1, col2 = st.columns(2)

    with col1:
        resized_img = image.resize((150, 150))
        st.image(resized_img, caption="📸 Uploaded Image", use_column_width=True)

    with col2:
        if st.button('🌱 Classify'):
            prediction = predict_image_class(model, image, class_indices)
            st.success(f'🍃 **Prediction:** {prediction}')