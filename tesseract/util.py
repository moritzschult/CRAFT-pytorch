import cv2


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


def bounding_box_not_exceeding_image(img, tx, ty, bx, by):
    return 0 < tx < img.shape[1] \
           and 0 < ty < img.shape[0] \
           and 0 < bx < img.shape[1] \
           and 0 < by < img.shape[0]


def crop_image(img, tx, ty, bx, by):
    cropped = img[ty:by, tx:bx]
    th, dst = cv2.threshold(cropped, 100, 255, cv2.THRESH_BINARY)
    return th, dst
