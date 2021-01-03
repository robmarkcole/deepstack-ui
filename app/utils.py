import io
from collections import namedtuple
from PIL import Image, ImageDraw
from typing import Tuple


def pil_image_to_byte_array(image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, "PNG")
    return imgByteArr.getvalue()


Box = namedtuple("Box", "y_min x_min y_max x_max")
Point = namedtuple("Point", "y x")


def point_in_box(box: Box, point: Point) -> bool:
    """Return true if point lies in box"""
    if (box.x_min <= point.x <= box.x_max) and (box.y_min <= point.y <= box.y_max):
        return True
    return False


def object_in_roi(roi: dict, centroid: dict) -> bool:
    """Convenience to convert dicts to the Point and Box."""
    target_center_point = Point(centroid["y"], centroid["x"])
    roi_box = Box(roi["y_min"], roi["x_min"], roi["y_max"], roi["x_max"])
    return point_in_box(roi_box, target_center_point)


def get_objects(predictions: list, img_width: int, img_height: int):
    """Return objects with formatting and extra info."""
    objects = []
    decimal_places = 3
    for pred in predictions:
        box_width = pred["x_max"] - pred["x_min"]
        box_height = pred["y_max"] - pred["y_min"]
        box = {
            "height": round(box_height / img_height, decimal_places),
            "width": round(box_width / img_width, decimal_places),
            "y_min": round(pred["y_min"] / img_height, decimal_places),
            "x_min": round(pred["x_min"] / img_width, decimal_places),
            "y_max": round(pred["y_max"] / img_height, decimal_places),
            "x_max": round(pred["x_max"] / img_width, decimal_places),
        }
        box_area = round(box["height"] * box["width"], decimal_places)
        centroid = {
            "x": round(box["x_min"] + (box["width"] / 2), decimal_places),
            "y": round(box["y_min"] + (box["height"] / 2), decimal_places),
        }
        name = pred["label"]
        confidence = pred["confidence"]

        objects.append(
            {
                "bounding_box": box,
                "box_area": box_area,
                "centroid": centroid,
                "name": name,
                "confidence": confidence,
            }
        )
    return objects


def get_faces(predictions: list):
    """Return faces info."""
    faces = []
    for pred in predictions:
        name = pred["userid"]
        confidence = pred["confidence"]

        faces.append(
            {"name": name, "confidence": confidence,}
        )
    return faces


def draw_box(
    draw: ImageDraw,
    box: Tuple[float, float, float, float],
    img_width: int,
    img_height: int,
    text: str = "",
    color: Tuple[int, int, int] = (255, 255, 0),
) -> None:
    """
    Draw a bounding box on and image.
    The bounding box is defined by the tuple (y_min, x_min, y_max, x_max)
    where the coordinates are floats in the range [0.0, 1.0] and
    relative to the width and height of the image.
    For example, if an image is 100 x 200 pixels (height x width) and the bounding
    box is `(0.1, 0.2, 0.5, 0.9)`, the upper-left and bottom-right coordinates of
    the bounding box will be `(40, 10)` to `(180, 50)` (in (x,y) coordinates).
    """

    line_width = 3
    font_height = 8
    y_min, x_min, y_max, x_max = box
    (left, right, top, bottom) = (
        x_min * img_width,
        x_max * img_width,
        y_min * img_height,
        y_max * img_height,
    )
    draw.line(
        [(left, top), (left, bottom), (right, bottom), (right, top), (left, top)],
        width=line_width,
        fill=color,
    )
    if text:
        draw.text(
            (left + line_width, abs(top - line_width - font_height)), text, fill=color
        )
