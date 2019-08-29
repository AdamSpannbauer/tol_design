import cv2
import numpy as np
import rand_tol as tol

# Range to deem as background
# White-ish range
BG_COLOR_LO = (100, 100, 100)
BG_COLOR_HI = (255, 255, 255)

# Black-ish range
# BG_COLOR_LO = (0, 0, 0)
# BG_COLOR_HI = (60, 60, 60)

# Value to be used as background color
BG_COLOR = (255, 255, 255)

# Change these to be whatever RGB values you want.
# If you want a color to appear more than the others
# then add it multiple times.
BG_PALETTE = [
    (0, 0, 0), (255, 255, 255),
    # (65, 135, 245), (5, 55, 135), (245, 215, 190),
    # (230, 145, 70), (230, 95, 55),
]
FG_PALETTE = [
    (0, 0, 0), (255, 255, 255)
    # (65, 135, 245), (5, 55, 135), (245, 215, 190),
    # (230, 145, 70), (230, 95, 55),
]

WINDOW_LABEL = "Press: r to regenerate; s to save; ESC to quit"


def read_frame(video_capture):
    status, frame = video_capture.read()

    if not status:
        return None

    mask = cv2.inRange(frame, BG_COLOR_LO, BG_COLOR_HI)
    negative_space = np.where(mask == 255)
    frame[negative_space] = BG_COLOR_HI

    return frame


def str_int(x):
    try:
        return int(x)
    except ValueError:
        return x


if __name__ == '__main__':
    import os.path
    import argparse
    import imutils

    MAX_DISPLAY_HEIGHT = 500

    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--input', default='~/Desktop/shane_goes.mp4', type=str_int,
                    help='Video to add effect to')
    ap.add_argument('-o', '--output', default='output_video.avi',
                    help='Path to output video')
    args = vars(ap.parse_args())

    vidcap = cv2.VideoCapture(os.path.expanduser(args['input']))
    fps = vidcap.get(cv2.CAP_PROP_FPS)

    def init_writer(shape):
        return cv2.VideoWriter(args['output'],
                               cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                               fps, shape, True)

    writer = None
    while True:
        im = read_frame(vidcap)
        if im is None:
            break

        if writer is None:
            writer = init_writer(shape=im.shape[:2])

        im = tol.pixelate(im, n_col=300, pixel_size=1)
        im = tol.add_noise(im,
                           fg_palette=FG_PALETTE,
                           bg_palette=BG_PALETTE,
                           bg_color=BG_COLOR_HI,
                           fg_sparsity=0.01,
                           bg_sparsity=0.99)

        im[np.where(im == BG_COLOR_HI)[:2]] = BG_COLOR

        im = imutils.resize(im, width=1000)
        h, w = im.shape[:2]

        if h > MAX_DISPLAY_HEIGHT:
            im = imutils.resize(im, height=MAX_DISPLAY_HEIGHT)

        writer.write(im)
        cv2.imshow('Frame', im)
        key = cv2.waitKey(30)

        if key == 27:
            break

    if writer is not None:
        writer.release()
