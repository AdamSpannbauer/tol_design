"""Gen 'random' design

# Getting started:
1. Install python3 & pip (some dude prolly wrote a good tutorial of how to do that)
2. Navigate to this folder via command line
3. Run `pip install -r requirements.txt`
4. Run `python3 tol_gui.py`
4. See Usage below for making changes to the output

# Usage:
python tol_gui.py --input 'path_to_image.png' --output 'path/to/output/folder' --width 100

## Arguments:
  --input    Path to png image to use.
  --output   Directory name to save output images to.
  --width    Width of output image in pixels (doesn't affect display size).

## Other options
You can make color modifications by editing BG_PALETTE and FG_PALETTE constants below.
"""

import datetime
import os
import cv2
import numpy as np
import imutils
import rand_tol as tol

# Set these to None if you just want use the png's
# transparency as background indicator
BG_COLOR_LO = (75, 75, 75)
BG_COLOR_HI = (255, 255, 255)

BG_COLOR = (51, 255, 51)

# Change these to be whatever RGB values you want.
# If you want a color to appear more than the others
# then add it multiple times.
BG_PALETTE = [
    (0, 0, 0),
]
FG_PALETTE = [
    (0, 0, 0),
]

# Leave these alone
WINDOW_LABEL = "Press: r to regenerate; s to save; ESC to quit"
DISPLAY_DIM = 500

PARAMS = dict(
    bg_sparsity={'value': 70, 'label': 'Background Sparsity %'},
    fg_sparsity={'value': 10, 'label': 'Logo Sparsity %'},
    resolution={'value': 50, 'label': "'Resolution'", 'max_val': 500},
    v_pad={'value': 4, 'label': 'Vertical Padding Row Count'},
    h_pad={'value': 16, 'label': 'Horizontal Padding Column Count'},
)


def noop(_):
    pass


def gen_design(path, output_dir, output_width=750):
    im = tol.read_logo(path, BG_COLOR, BG_COLOR_LO, BG_COLOR_HI)

    cv2.namedWindow(WINDOW_LABEL)
    for param in PARAMS.values():
        min_val = 0 if 'min_val' not in param.keys() else param['min_val']
        max_val = 100 if 'max_val' not in param.keys() else param['max_val']

        cv2.createTrackbar(param['label'], WINDOW_LABEL, min_val, max_val, noop)
        cv2.setTrackbarPos(param['label'], WINDOW_LABEL, param['value'])

    og_im = np.copy(im)
    gen_new = True
    while True:
        if gen_new:
            im = np.copy(og_im)
            gen_new = False

            for param in PARAMS.values():
                param['value'] = cv2.getTrackbarPos(param['label'], WINDOW_LABEL)

            im = tol.pixelate(im, n_col=PARAMS['resolution']['value'], pixel_size=1)
            im = tol.add_border(im,
                                vertical=PARAMS['v_pad']['value'],
                                horizontal=PARAMS['h_pad']['value'],
                                bg_color=BG_COLOR)
            im = tol.add_noise(im,
                               fg_palette=FG_PALETTE,
                               bg_palette=BG_PALETTE,
                               bg_color=BG_COLOR,
                               fg_sparsity=PARAMS['fg_sparsity']['value'] / 100,
                               bg_sparsity=PARAMS['bg_sparsity']['value'] / 100)

            im = imutils.resize(im, width=DISPLAY_DIM)
            if im.shape[0] > DISPLAY_DIM:
                im = imutils.resize(im, height=DISPLAY_DIM)

        cv2.imshow(WINDOW_LABEL, im)

        key = cv2.waitKey(0)

        if key == ord('r'):
            gen_new = True
        elif key == ord('s'):
            timestamp = datetime.datetime.utcnow().strftime('%Y_%m_%d__%H_%M_%S')
            output_path = os.path.join(output_dir, f'design_{timestamp}.png')
            save_im = imutils.resize(im, width=output_width)
            tol.write_logo(save_im, output_path, bg_color=BG_COLOR)
        elif key == 27:
            break


if __name__ == '__main__':
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--input', default='untero_logomockup.png',
                    help='Path to png image to use.')
    ap.add_argument('-o', '--output', default='output',
                    help='Name of directory to save output images to.')
    ap.add_argument('-w', '--width', default=1000, type=int,
                    help="Width of saved image output in pixels (doesn't affect display size).")
    args = vars(ap.parse_args())

    gen_design(path=args['input'],
               output_dir=args['output'],
               output_width=args['width'])
