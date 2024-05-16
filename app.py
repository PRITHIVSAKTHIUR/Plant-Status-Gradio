import os
import gradio as gr
import tensorflow as tf
import numpy as np

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


model = tf.keras.models.load_model('plant_disease_classifier.h5')

def predict(input_image):
    try:
        
        input_image = tf.image.resize(input_image, [256, 256])
        input_image = tf.expand_dims(input_image, 0) / 255.0

        predictions = model.predict(input_image)
        labels = ['Healthy', 'Powdery', 'Rust']

        class_idx = np.argmax(predictions)
        class_label = labels[class_idx]
        confidence = np.round(predictions[0][class_idx] * 100, 3)

        return f"Predicted Class: {class_label}.  Confidence Score: {confidence}%"

    except Exception as e:
        return f"An error occurred: {e}"

examples = ["1.png", "2.png", "3.png"]

iface = gr.Interface(
    fn=predict,
    inputs=gr.Image(type="numpy", image_mode="RGB"),
    outputs="text",
    title="<div style='text-align: center;'>🍂PLANT STATUS🍂</div>",
    description='🍃Upload a photo of a plant to see how the model classifies its status!🍃',
    examples=examples
)

iface.launch(share=True)
