import traceback

import cv2
from pytesseract import pytesseract

from tesseract.util import bounding_box_not_exceeding_image, crop_image, show_crop, decode_boxes, show_window


def process_images(file_paths, margin, debug=False):
    """
    Iterate over file paths and run image to text conversion, for every detected box in the image.
    """
    for idx, jpg_path in enumerate(file_paths["jpg"]):
        for box in file_paths["boxes"][idx]:
            selected_coordinates, full_coordinates = decode_boxes(box)

            img = cv2.imread(jpg_path)

            if debug:
                show_crop(img, full_coordinates[1], full_coordinates[5], full_coordinates[0], full_coordinates[4])

            convert_image_to_text(selected_coordinates, jpg_path, margin)


def tesseract_decode(dst, print_text=False):
    """
    Apply OCR on the cropped image
    """
    text = pytesseract.image_to_string(dst)
    if print_text:
        print(text)


def convert_image_to_text(coordinates, img_path, margin, debug_mode=False):
    tx, ty, bx, by = coordinates[0], coordinates[1], coordinates[2], coordinates[3]

    # reads image as grayscale
    img = cv2.imread(img_path, 2)

    if img is None:
        return

    # Drawing a rectangle on copied image
    if debug_mode:
        rect = cv2.rectangle(img, (tx, ty), (bx, by), (0, 255, 0))
        show_window(rect, 'With rect')

    # Add bounding box if possible
    if bounding_box_not_exceeding_image(img, tx - margin, ty - margin, bx - margin, by - margin, ):
        tx -= margin
        ty -= margin
        bx += margin
        by += margin

    _, dst = crop_image(img, tx, ty, bx, by)
    tesseract_decode(dst, True)
