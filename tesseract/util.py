import os

import cv2


def generate_file_paths(base_path, image_path):
    file_paths = {"txt": [],
                  "jpg": [],
                  "boxes": []}
    for file in os.listdir(base_path):
        if file.endswith(".txt"):
            file_paths["txt"].append(base_path + file)
            file_paths["jpg"].append(image_path + file.replace(".txt", ".jpg").replace("res_", ""))
    return file_paths


def add_bounding_boxes(file_paths):
    for file_path in file_paths["txt"]:
        with open(file_path, 'rb') as f:
            lines = f.readlines()
            file_paths["boxes"].append(lines)
    return file_paths


def decode_boxes(input_string):
    full_coordinates = input_string.decode("utf-8").split(",")
    selected_coordinates = [full_coordinates[0]] + [full_coordinates[1]] + [full_coordinates[4]] + [
        full_coordinates[5]]

    selected_coordinates = [int(coordinate) for coordinate in selected_coordinates]
    full_coordinates = [int(coordinate) for coordinate in full_coordinates]
    return selected_coordinates, full_coordinates


def show_window(image):
    cv2.imshow('cropped', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def show_crop(img, coordinate_one, coordinate_two, coordinate_three, coordinate_four):
    cropped = img[coordinate_one:coordinate_two, coordinate_three:coordinate_four]
    show_window(cropped)
