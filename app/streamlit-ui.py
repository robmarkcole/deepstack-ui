from pathlib import Path
import sys
import io
import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import os
import deepstack.core as ds
import utils
import const

## Depstack setup
DEEPSTACK_IP = os.getenv("DEEPSTACK_IP", "localhost")
DEEPSTACK_PORT = os.getenv("DEEPSTACK_PORT", 5000)
DEEPSTACK_API_KEY = os.getenv("DEEPSTACK_API_KEY", "")
DEEPSTACK_TIMEOUT = int(os.getenv("DEEPSTACK_TIMEOUT", 10))

DEFAULT_CONFIDENCE_THRESHOLD = 0
TEST_IMAGE = "street.jpg"

DEFAULT_ROI_Y_MIN = 0.0
DEFAULT_ROI_Y_MAX = 1.0
DEFAULT_ROI_X_MIN = 0.0
DEFAULT_ROI_X_MAX = 1.0
DEFAULT_ROI = (
    DEFAULT_ROI_Y_MIN,
    DEFAULT_ROI_X_MIN,
    DEFAULT_ROI_Y_MAX,
    DEFAULT_ROI_X_MAX,
)

predictions = None


@st.cache
def process_image(pil_image, dsobject):
    image_bytes = utils.pil_image_to_byte_array(pil_image)
    dsobject.detect(image_bytes)
    predictions = dsobject.predictions
    return predictions


## Setup sidebar
st.title("Deepstack Object detection")
img_file_buffer = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

st.sidebar.title("Parameters")
CONFIDENCE_THRESHOLD = st.sidebar.slider(
    "Confidence threshold", 0, 100, DEFAULT_CONFIDENCE_THRESHOLD, 1
)

CLASSES_TO_INCLUDE = st.sidebar.multiselect(
    "Select object classes to include",
    options=const.CLASSES,
    default=const.DEFAULT_CLASSES,
)

# Get ROI info
st.sidebar.title("ROI")
ROI_X_MIN = st.sidebar.slider("x_min", 0.0, 1.0, DEFAULT_ROI_X_MIN)
ROI_Y_MIN = st.sidebar.slider("y_min", 0.0, 1.0, DEFAULT_ROI_Y_MIN)
ROI_X_MAX = st.sidebar.slider("x_max", 0.0, 1.0, DEFAULT_ROI_X_MAX)
ROI_Y_MAX = st.sidebar.slider("y_max", 0.0, 1.0, DEFAULT_ROI_Y_MAX)
ROI_TUPLE = (
    ROI_Y_MIN,
    ROI_X_MIN,
    ROI_Y_MAX,
    ROI_X_MAX,
)
ROI_DICT = {
    "x_min": ROI_X_MIN,
    "y_min": ROI_Y_MIN,
    "x_max": ROI_X_MAX,
    "y_max": ROI_Y_MAX,
}

## Process image
if img_file_buffer is not None:
    pil_image = Image.open(img_file_buffer)

else:
    pil_image = Image.open(TEST_IMAGE)

dsobject = ds.DeepstackObject(
    DEEPSTACK_IP, DEEPSTACK_PORT, DEEPSTACK_API_KEY, DEEPSTACK_TIMEOUT
)

predictions = process_image(pil_image, dsobject)
objects = utils.get_objects(predictions, pil_image.width, pil_image.height)
all_objects_names = set([obj["name"] for obj in objects])

# Filter objects for display
objects = [obj for obj in objects if obj["confidence"] > CONFIDENCE_THRESHOLD]
objects = [obj for obj in objects if obj["name"] in CLASSES_TO_INCLUDE]
objects = [obj for obj in objects if utils.object_in_roi(ROI_DICT, obj["centroid"])]

# Draw object boxes
draw = ImageDraw.Draw(pil_image)
for obj in objects:
    name = obj["name"]
    confidence = obj["confidence"]
    box = obj["bounding_box"]
    box_label = f"{name}: {confidence:.1f}%"

    utils.draw_box(
        draw,
        (box["y_min"], box["x_min"], box["y_max"], box["x_max"]),
        pil_image.width,
        pil_image.height,
        text=box_label,
        color=const.YELLOW,
    )

# Draw ROI box
if ROI_TUPLE != DEFAULT_ROI:
    utils.draw_box(
        draw,
        ROI_TUPLE,
        pil_image.width,
        pil_image.height,
        text="ROI",
        color=const.GREEN,
    )

# Display image and results
st.image(
    np.array(pil_image), caption=f"Processed image", use_column_width=True,
)
st.subheader("All discovered objects")
st.write(all_objects_names)

st.subheader("Filtered object count")
obj_types = list(set([obj["name"] for obj in objects]))
for obj_type in obj_types:
    obj_type_count = len([obj for obj in objects if obj["name"] == obj_type])
    st.write(f"{obj_type} : {obj_type_count}")

st.subheader("All filtered objects")
st.write(objects)

st.subheader("Deepstack raw response")
st.write(predictions)
