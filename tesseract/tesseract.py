import traceback

import cv2
from pytesseract import pytesseract

from tesseract.util import bounding_box_not_exceeding_image, crop_image

margin = 10


def tesseract_decode(dst, print_text=False):
    # Apply OCR on the cropped image
    text = pytesseract.image_to_string(dst)
    if print_text:
        print(text)


def convert_image_to_text(coordinates, img_path, debug_mode=False):
    tx, ty, bx, by = coordinates[0], coordinates[1], coordinates[2], coordinates[3]

    # reads image 'opencv-logo.png' as grayscale
    img = cv2.imread(img_path, 2)

    if img is None:
        return

    # Drawing a rectangle on copied image
    if debug_mode:
        try:
            cv2.rectangle(img, (tx, ty), (bx, by), (0, 255, 0))
        except TypeError:
            traceback.print_exc()
            return

    # Add bounding box if possible
    if bounding_box_not_exceeding_image(img, tx - margin, ty - margin, bx - margin, by - margin, ):
        tx -= margin
        ty -= margin
        bx += margin
        by += margin

    _, dst = crop_image(img, tx, ty, bx, by)
    tesseract_decode(dst, True)
