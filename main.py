import cv2

from tesseract.tesseract import extract
from tesseract.util import generate_file_paths, add_bounding_boxes, decode_boxes, show_crop
from craft import test
margin = 10

result_path = "result/"
source_path = "data/jbl/"


def process_images(file_paths, debug=False):
    for idx, jpg_path in enumerate(file_paths["jpg"]):
        for box in file_paths["boxes"][idx]:
            selected_coordinates, full_coordinates = decode_boxes(box)

            img = cv2.imread(jpg_path)

            if debug:
                show_crop(img, full_coordinates[1], full_coordinates[5], full_coordinates[0], full_coordinates[4])

            extract(selected_coordinates, jpg_path)

def apply_tesseract_to_images():
    test.main()



file_paths = generate_file_paths(result_path, source_path)
file_paths = add_bounding_boxes(file_paths)
process_images(file_paths)
