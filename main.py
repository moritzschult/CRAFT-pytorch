from file_processing_utils import generate_file_paths
from tesseract.tesseract import process_images

# Margin of the bounding box, which is applied to the crop of the detected text in the image
bounding_box_margin = 10

# Location of the txt files containing the tesseract detections
result_path = "result/"
# Location of the images on which the detection shall be applied
image_path = "data/jbl/"

file_paths = generate_file_paths(result_path, image_path)
process_images(file_paths, bounding_box_margin)
