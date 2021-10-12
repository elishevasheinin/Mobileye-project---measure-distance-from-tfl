try:
    import os
    import json
    import glob
    import numpy as np
    from PIL import Image
    from Part1.find_tfl_candidates import find_tfl_lights
except ImportError:
    print("Need to fix the installation")
    raise


def pick_not_traffic_pixel(test_png, image_path):
    return_array = []
    red_x, red_y, green_x, green_y = find_tfl_lights(image_path)
    for x, y in zip(red_x + green_x, red_y + green_y):
        if test_png[y, x] != 19:
            return_array.append((x, y))
    return return_array


def pick_pixels(test_json, test_png, image_img):
    real_traffic_pixel = pick_traffic_pixel(test_json)
    not_traffic_pixel = pick_not_traffic_pixel(test_png, image_img)
    real_traffic_pixel = real_traffic_pixel[:min(len(real_traffic_pixel), len(not_traffic_pixel))]
    not_traffic_pixel = not_traffic_pixel[:min(len(real_traffic_pixel), len(not_traffic_pixel))]
    return real_traffic_pixel, not_traffic_pixel


def pick_traffic_pixel(test_json):
    with open(test_json) as f:
        data = json.load(f)
        return_array = []
        for object in data["objects"]:
            if object["label"] == "traffic light":
                traffic_data = np.array(object["polygon"])
                max_x = max(traffic_data[:, 0])
                max_y = max(traffic_data[:, 1])
                min_x = min(traffic_data[:, 0])
                min_y = min(traffic_data[:, 1])
                x = (max_x + min_x) / 2
                y = (max_y + min_y) / 2
                return_array.append((x, y))
        return return_array


def crop_image(image_path, points_list):
    image = Image.open(image_path)
    right = 41
    left = 41
    top = 41
    bottom = 41
    width, height = image.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(image.mode, (new_width, new_height), (0, 0, 0))
    result.paste(image, (left, top))
    cropped_images = []
    for point in points_list:
        x, y = int(point[0]), int(point[1])
        cropped_images.append(np.array(image.crop((x - 41, y - 41, x + 40, y + 40))))
    return cropped_images


def save_data(crop_array, label, path):
    with open("../data/model_training/{}/labels.bin".format(path), "ab") as labels_file:
        with open("../data/model_training/{}/data.bin".format(path), "ab") as  data_file:
            for image in crop_array:
                labels_file.write(label.to_bytes(1, "big"))
                data_file.write(image.tobytes())


def create_dataset(data, ground_truth, path):
    for root, subdirectories, files in os.walk(data):
        for subdirectory in subdirectories:
            train_list = glob.glob(os.path.join(data + "/" + subdirectory, '*_leftImg8bit.png'))
            ground_truth_train = glob.glob(os.path.join(ground_truth + "/" + subdirectory, '*_labelIds.png'))
            ground_truth_json = glob.glob(os.path.join(ground_truth + "/" + subdirectory, '*_polygons.json'))
            for image, test_json, test_png in zip(train_list, ground_truth_json, ground_truth_train):
                test_img = np.array(Image.open(test_png))
                traffic_light_pixels, non_traffic_pixels = pick_pixels(test_json, test_img, image)
                crop_traffic_array = crop_image(image, traffic_light_pixels)
                crop_non_traffic_array = crop_image(image, non_traffic_pixels)
                save_data(crop_traffic_array, 1, path)
                save_data(crop_non_traffic_array, 0, path)


def main():
    train_data = '../data/leftImg8bit/train'
    train_ground_truth = '../data/gtFine/train'
    val_data = '../data/leftImg8bit/val'
    val_ground_truth = '../data/gtFine/val'
    create_dataset(train_data, train_ground_truth, "train")
    create_dataset(val_data, val_ground_truth, "val")


if __name__ == '__main__':
    main()
