import random
import cv2
from imutils import resize
import numpy as np

random.seed(42)

LOGO_PATH = 'untero_logomockup.png'
BG_COLOR = (255, 255, 255)
PALETTE = [
    (65, 135, 245), (5, 55, 135), (245, 215, 190),
    (230, 145, 70), (230, 95, 55),
]


def set_bg(image, bgr_range_lo, bgr_range_hi, bg_color=None):
    if bg_color is None:
        bg_color = bgr_range_hi

    mask = cv2.inRange(image, bgr_range_lo, bgr_range_hi)
    negative_space = np.where(mask == 255)
    image[negative_space] = bg_color

    return image


def read_logo(path, bg_color=(255, 255, 255), bgr_range_lo=None, bgr_range_hi=None):
    image = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    if image.shape[2] == 4:
        image[np.where(image[:, :, 3] == 0)] = list(bg_color) + [255]
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    if bgr_range_lo is not None and bgr_range_hi is not None:
        set_bg(image, bgr_range_lo, bgr_range_hi, bg_color)

    return image


def write_logo(image, path, bg_color):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    bg_y, bg_x, bg_z = np.where(image[:, :, :3] == bg_color)
    image[bg_y, bg_x] = list(bg_color) + [0]
    cv2.imwrite(path, image)


def pixelate(image, n_col=50, pixel_size=1):
    shrunken = resize(image, width=n_col)
    return resize(shrunken, width=n_col * pixel_size)


def rand_colors(k, palette, bg_color, bg_weight):
    non_bg_weights = [(1 - bg_weight) / len(palette) for _ in palette]
    palette = [bg_color] + palette
    weights = [bg_weight] + non_bg_weights
    return random.choices(palette, weights=weights, k=k)


def add_border(image, vertical=4, horizontal=16, bg_color=(255, 255, 255)):
    return cv2.copyMakeBorder(image,
                              top=vertical, bottom=vertical,
                              left=horizontal, right=horizontal,
                              borderType=cv2.BORDER_CONSTANT, value=bg_color)


def add_noise(image, fg_palette=None, bg_palette=None, bg_color=(255, 255, 255),
              fg_sparsity=0.1, bg_sparsity=0.7):
    if fg_palette is None:
        fg_palette = PALETTE

    if bg_palette is None:
        bg_palette = PALETTE

    bg_y, bg_x, bg_z = np.where(image == bg_color)
    fg_y, fg_x, fg_z = np.where(image != bg_color)

    if len(bg_x):
        new_bg_pixels = rand_colors(len(bg_x), bg_palette, bg_color, bg_sparsity)
        image[bg_y, bg_x] = new_bg_pixels

    if len(fg_x):
        new_fg_pixels = rand_colors(len(fg_x), fg_palette, bg_color, fg_sparsity)
        image[fg_y, fg_x] = new_fg_pixels

    return image


if __name__ == '__main__':
    import cv2

    logo = read_logo(LOGO_PATH)

    logo = pixelate(logo)
    logo = add_border(logo)
    logo = add_noise(logo, fg_sparsity=0.1, bg_sparsity=0.7)

    logo = resize(logo, width=1000)

    cv2.imshow('ToL', logo)
    cv2.waitKey(0)
