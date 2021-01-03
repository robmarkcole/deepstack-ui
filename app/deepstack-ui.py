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

DEFAULT_CONFIDENCE_THRESHOLD = 0.45
MIN_CONFIDENCE_THRESHOLD = 0.1
MAX_CONFIDENCE_THRESHOLD = 1.0
OBJECT_TEST_IMAGE = "street.jpg"
FACE_TEST_IMAGE = "faces.jpg"
FACE = "Face"
OBJECT = "Object"

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

## Depstack setup
DEEPSTACK_IP = os.getenv("DEEPSTACK_IP", "localhost")
DEEPSTACK_PORT = os.getenv("DEEPSTACK_PORT", 80)
DEEPSTACK_API_KEY = os.getenv("DEEPSTACK_API_KEY", "")
DEEPSTACK_TIMEOUT = int(os.getenv("DEEPSTACK_TIMEOUT", 20))
DEEPSTACK_CUSTOM_MODEL = os.getenv("DEEPSTACK_CUSTOM_MODEL", None)

predictions = None


@st.cache
def process_image_object(pil_image, dsobject):
    image_bytes = utils.pil_image_to_byte_array(pil_image)
    predictions = dsobject.detect(image_bytes)
    return predictions


@st.cache
def process_image_face(pil_image, dsface):
    image_bytes = utils.pil_image_to_byte_array(pil_image)
    predictions = dsface.recognize(image_bytes)
    return predictions


deepstack_mode = st.selectbox("Select Deepstack mode:", [OBJECT, FACE])

if deepstack_mode == FACE:
    st.title("Deepstack Face recogntion")

    img_file_buffer = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    ## Process image
    if img_file_buffer is not None:
        pil_image = Image.open(img_file_buffer)

    else:
        pil_image = Image.open(FACE_TEST_IMAGE)

    dsface = ds.DeepstackFace(
        ip=DEEPSTACK_IP,
        port=DEEPSTACK_PORT,
        api_key=DEEPSTACK_API_KEY,
        timeout=DEEPSTACK_TIMEOUT,
        min_confidence=MIN_CONFIDENCE_THRESHOLD,
    )
    predictions = process_image_face(pil_image, dsface)
    faces = utils.get_faces(predictions, pil_image.width, pil_image.height)

    # Draw object boxes
    draw = ImageDraw.Draw(pil_image)
    for face in faces:
        name = face["name"]
        confidence = face["confidence"]
        box = face["bounding_box"]
        box_label = f"{name}"

        utils.draw_box(
            draw,
            (box["y_min"], box["x_min"], box["y_max"], box["x_max"]),
            pil_image.width,
            pil_image.height,
            text=box_label,
            color=const.YELLOW,
        )
    st.image(
        np.array(pil_image), caption=f"Processed image", use_column_width=True,
    )
    st.subheader("All faces")
    st.write(faces)


elif deepstack_mode == OBJECT:
    ## Setup main
    st.title("Deepstack Object detection")
    if not DEEPSTACK_CUSTOM_MODEL:
        st.text("Using default model")
    else:
        st.text(f"Using custom model named {DEEPSTACK_CUSTOM_MODEL}")

    ## Setup sidebar
    st.sidebar.title("Parameters")
    st.text("Adjust parameters to select what is displayed")
    CONFIDENCE_THRESHOLD = st.sidebar.slider(
        "Confidence threshold",
        MIN_CONFIDENCE_THRESHOLD,
        MAX_CONFIDENCE_THRESHOLD,
        DEFAULT_CONFIDENCE_THRESHOLD,
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

    img_file_buffer = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if not DEEPSTACK_CUSTOM_MODEL:
        CLASSES_TO_INCLUDE = st.sidebar.multiselect(
            "Select object classes to include",
            options=const.CLASSES,
            default=const.CLASSES,
        )

    ## Process image
    if img_file_buffer is not None:
        pil_image = Image.open(img_file_buffer)

    else:
        pil_image = Image.open(OBJECT_TEST_IMAGE)

    if not DEEPSTACK_CUSTOM_MODEL:
        dsobject = ds.DeepstackObject(
            ip=DEEPSTACK_IP,
            port=DEEPSTACK_PORT,
            api_key=DEEPSTACK_API_KEY,
            timeout=DEEPSTACK_TIMEOUT,
            min_confidence=MIN_CONFIDENCE_THRESHOLD,
        )
    else:
        dsobject = ds.DeepstackObject(
            ip=DEEPSTACK_IP,
            port=DEEPSTACK_PORT,
            api_key=DEEPSTACK_API_KEY,
            timeout=DEEPSTACK_TIMEOUT,
            min_confidence=MIN_CONFIDENCE_THRESHOLD,
            custom_model=DEEPSTACK_CUSTOM_MODEL,
        )

    predictions = process_image_object(pil_image, dsobject)
    objects = utils.get_objects(predictions, pil_image.width, pil_image.height)
    all_objects_names = set([obj["name"] for obj in objects])

    # Filter objects for display
    objects = [obj for obj in objects if obj["confidence"] > CONFIDENCE_THRESHOLD]
    objects = [obj for obj in objects if utils.object_in_roi(ROI_DICT, obj["centroid"])]
    if not DEEPSTACK_CUSTOM_MODEL:
        objects = [obj for obj in objects if obj["name"] in CLASSES_TO_INCLUDE]

    # Draw object boxes
    draw = ImageDraw.Draw(pil_image)
    for obj in objects:
        name = obj["name"]
        confidence = obj["confidence"]
        box = obj["bounding_box"]
        box_label = f"{name}"

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
