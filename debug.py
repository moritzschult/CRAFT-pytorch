import traceback

import cv2
from pytesseract import pytesseract
import os

margin = 10

cv2.bootstrap()


def tesseract_decode(tx, ty, bx, by, img, img_path):
    if img is None:
        return
    # try:
    #     cropped = img[ty:by, tx:bx]
    #     cv2.imwrite(f'cropped/out_{img_path.split("/")[-1]}', cropped)
    # except TypeError:
    #     traceback.print_exc()

    cropped = img[ty:by, tx:bx]
    th, dst = cv2.threshold(cropped, 100, 255, cv2.THRESH_BINARY)

    # Apply OCR on the cropped image
    text = pytesseract.image_to_string(dst)

    print(text)
    # if "Turmzimmer" in text:

    cv2.imshow('cropped', dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def extract(coordinates, img_path, debug_mode=False):
    # tx, ty, bx, by = 637, 443, 766, 495
    tx, ty, bx, by = coordinates[0], coordinates[1], coordinates[2], coordinates[3]

    # reads image 'opencv-logo.png' as grayscale
    img = cv2.imread(img_path, 2)

    # Drawing a rectangle on copied image
    if debug_mode:
        try:
            rect = cv2.rectangle(img, (tx, ty), (bx, by), (0, 255, 0))
        except TypeError:
            traceback.print_exc()
            return

    try:
        tx -= margin
        ty -= margin
        bx += margin
        by += margin
        tesseract_decode(tx, ty, bx, by, img, img_path)
        # cropped = img[ty:by, tx:bx]
    except SystemError:
        # Reset margin increase, if image is to big after increase
        tx += margin
        ty += margin
        bx -= margin
        by -= margin
        tesseract_decode(tx, ty, bx, by, img, img_path)
    #     cropped = img[ty:by, tx:bx]
    #
    # # Apply OCR on the cropped image
    # text = pytesseract.image_to_string(cropped)
    #
    # print(text)
    #
    # cv2.imshow('cropped', cropped)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


result_path = "result/"
source_path = "data/jbl/"
file_paths = {"txt": [],
              "jpg": [],
              "boxes": []}

for file in os.listdir(result_path):
    if file.endswith(".txt"):
        file_paths["txt"].append(result_path + file)
        file_paths["jpg"].append(source_path + file.replace(".txt", ".jpg").replace("res_", ""))

for file_path in file_paths["txt"]:
    with open(file_path, 'rb') as f:
        lines = f.readlines()
        file_paths["boxes"].append(lines)

for idx, jpg_path in enumerate(file_paths["jpg"]):
    for box in file_paths["boxes"][idx]:
        full_coordinates = box.decode("utf-8").split(",")
        selected_coordinates = [full_coordinates[0]] + [full_coordinates[1]] + [full_coordinates[4]] + [
            full_coordinates[5]]

        selected_coordinates = [int(coordinate) for coordinate in selected_coordinates]
        full_coordinates = [int(coordinate) for coordinate in full_coordinates]
        # file_paths['boxes'][0][0].decode("utf-8").split(",")

        img = cv2.imread(jpg_path)
        rect = cv2.rectangle(img, (full_coordinates[0], full_coordinates[1]), (full_coordinates[4], full_coordinates[5]), (0, 255, 0))

        cropped = img[full_coordinates[1]:full_coordinates[5], full_coordinates[0]:full_coordinates[4]]
        cv2.imshow('cropped', cropped)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        extract(selected_coordinates, jpg_path)
debug = 0
