import os

from tesseract.util import add_bounding_boxes


def read_files(base_path, image_path):
    """
    Reads file-paths of images, located at image_path and detected bounding-boxes under base_path
    """
    file_paths = {"txt": [],
                  "jpg": [],
                  "boxes": []}
    for file in os.listdir(base_path):
        if file.endswith(".txt"):
            file_paths["txt"].append(base_path + file)
            file_paths["jpg"].append(image_path + file.replace(".txt", ".jpg").replace("res_", ""))
    return file_paths


def generate_file_paths(result_path, source_path):
    file_paths = read_files(result_path, source_path)
    return add_bounding_boxes(file_paths)
