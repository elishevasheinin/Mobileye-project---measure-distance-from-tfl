try:
    from PIL import Image
    from tensorflow.keras.models import load_model
    import numpy as np
except ImportError:
    print("Need to fix the installation")
    raise


class Filter:
    def __init__(self):
        self.__loaded_model = load_model("../data/model/model.h5")

    def crop_image(self, image_path, points_list):
        image = Image.open(image_path)
        right, left, top, bottom = 41, 41, 41, 41
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

    def filter_points(self, curr_image, candidates_points, candidates_colors):
        crop_images = self.crop_image(curr_image, candidates_points)
        l_predictions = self.__loaded_model.predict(np.array(crop_images))
        l_predicted_label = np.argmax(l_predictions, axis=-1)
        tfl_images = [point for pred, point in zip(l_predicted_label, candidates_points) if pred == 1]
        tfl_colors=[color for pred, color in zip(l_predicted_label, candidates_colors) if pred == 1]
        return tfl_images, tfl_colors
