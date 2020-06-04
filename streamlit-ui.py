from pathlib import Path
import sys
import io
import streamlit as st
from PIL import Image
import numpy as np
import os
import deepstack.core as ds

## Depstack setup
DEEPSTACK_IP_ADDRESS = "localhost"
DEEPSTACK_PORT = "5000"
DEEPSTACK_API_KEY = ""
DEEPSTACK_TIMEOUT = 20  # Default is 10

DEFAULT_CONFIDENCE_THRESHOLD = 0.5
TEST_IMAGE = "street.jpg"

detections = ""


def pil_image_to_byte_array(image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, "PNG")
    return imgByteArr.getvalue()


@st.cache
def process_image(pil_image, dsobject):
    try:
        image_bytes = pil_image_to_byte_array(pil_image)
        dsobject.detect(image_bytes)
        return dsobject.predictions
    except Exception as exc:
        return exc


st.title("Object detection with Deepstack")
img_file_buffer = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
confidence_threshold = st.slider(
    "Confidence threshold", 0.0, 1.0, DEFAULT_CONFIDENCE_THRESHOLD, 0.05
)

if img_file_buffer is not None:
    pil_image = Image.open(img_file_buffer)

else:
    pil_image = Image.open(TEST_IMAGE)

dsobject = ds.DeepstackObject(
    DEEPSTACK_IP_ADDRESS, DEEPSTACK_PORT, DEEPSTACK_API_KEY, DEEPSTACK_TIMEOUT
)
detections = process_image(pil_image, dsobject)

st.image(
    np.array(pil_image), caption=f"Processed image", use_column_width=True,
)

st.write(detections)
