from pathlib import Path
import sys
from io import BytesIO
import streamlit as st
from PIL import Image
import numpy as np
import os
import deepstack.core as ds

## Depstack setup
DEEPSTACK_IP_ADDRESS = "localhost"
DEEPSTACK_PORT = "5000"
DEEPSTACK_API_KEY = "Mysecretkey"
DEEPSTACK_TIMEOUT = 20  # Default is 10

DEFAULT_CONFIDENCE_THRESHOLD = 0.5
TEST_IMAGE = "street.jpg"

st.title("Object detection with Deepstack")
img_file_buffer = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
confidence_threshold = st.slider(
    "Confidence threshold", 0.0, 1.0, DEFAULT_CONFIDENCE_THRESHOLD, 0.05
)

if img_file_buffer is not None:
    image = np.array(Image.open(img_file_buffer))

else:
    image = np.array(Image.open(TEST_IMAGE))


st.image(
    image, caption=f"Processed image", use_column_width=True,
)