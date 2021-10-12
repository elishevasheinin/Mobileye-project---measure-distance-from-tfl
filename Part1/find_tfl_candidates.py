import math

try:
    import cv2 as cv
    import numpy as np
    from scipy import signal as sg
    from PIL import Image
    from skimage.feature import peak_local_max
    from skimage import img_as_float
except ImportError:
    print("Need to fix the installation")
    raise


def find_tfl_lights(image_path, **kwargs):
    """
    Detect candidates_points for TFL lights. Use c_image, kwargs and you imagination to implement
    :param c_image: The image itself as np.uint8, shape of (H, W, 3)
    :param image_path: The image path
    :param kwargs: Whatever config you want to pass in here
    :return: 4-tuple of x_red, y_red, x_green, y_green
    """
    c_image = np.array(Image.open(image_path))
    img = cv.imread(image_path)
    layer = cv.pyrDown(img)
    layer = np.array(layer)
    layer = img_as_float(layer)
    red, green = [], []
    red_big_image = c_image[:, :, 0]
    green_big_image = c_image[:, :, 1]
    red_small_image = layer[:, :, 0]
    green_small_image = layer[:, :, 1]
    image = np.array(Image.open('../data/kernel.png').convert('L'))
    image = img_as_float(image)
    image = image[160:180, 980:1002]
    image.astype(float)
    kernel = image - image.mean()
    red_high_pass = sg.convolve(red_big_image, kernel, mode='same')
    red_coordinates = peak_local_max(red_high_pass, min_distance=30, threshold_abs=6, num_peaks=5)
    green_high_pass = sg.convolve(green_big_image, kernel, mode='same')
    green_coordinates = peak_local_max(green_high_pass, min_distance=20, threshold_abs=6, num_peaks=7)

    for i in red_coordinates:
        red.append((i[1], i[0]))
    for i in green_coordinates:
        green.append((i[1], i[0]))

    red_high_pass = sg.convolve(red_small_image, kernel, mode='same')
    red_coordinates = peak_local_max(red_high_pass, min_distance=10, threshold_abs=15)
    green_high_pass = sg.convolve(green_small_image, kernel, mode='same')
    green_coordinates = peak_local_max((green_high_pass), min_distance=20, threshold_abs=15)

    for i in red_coordinates:
        red.append((i[1] * 2, i[0] * 2))
    for i in green_coordinates:
        green.append((i[1] * 2, i[0] * 2))

    return red + green, ["red" for _ in range(len(red))] + ["green" for _ in range(len(green))]

def reduce_dup(img, positions, colors):
    for i in range(len(positions)):
        for j in range(i,len(positions)):
            if 0 < get_dis(positions[i], positions[j]) < 20:
                if colors[i] != colors[j]:
                    if img[positions[i][1], positions[i][0], 0] >= img[positions[i][1], positions[i][0], 1]:
                        ind = i if colors[i] == "green" else j
                        positions.pop(ind)
                        colors.pop(ind)
                    else:
                        ind = i if colors[i] == "red" else j
                        positions.pop(ind)
                        colors.pop(ind)
                else:
                    positions.pop(i)
    return positions, colors

def get_dis(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)‏

# def reduce_dup(img, red, green):
#     pop_red, pop_green = [], []
#     for r in red:
#         for g in green:
#             if get_dis(r, g) < 20:
#                 if img[r[1], r[0], 0] >= img[r[1], r[0], 1]:
#                     pop_green.append(g)
#         else:
#             pop_red.append(r)
#     new_red, new_green = [r for r in red if r not in pop_red], [g for g in green if g not in pop_green]
#     return [x[0] for x in new_red], [y[1] for y in new_red], [x[0] for x in new_green], [y[1] for y in new_green]
