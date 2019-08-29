import cv2
import numpy as np
import imutils
import rand_tol as tol
import tol_gui

INPUT_PATH = 'untero_logomockup.png'


im = tol.read_logo(INPUT_PATH, tol_gui.BG_COLOR, tol_gui.BG_COLOR_LO, tol_gui.BG_COLOR_HI)
im = tol.pixelate(im, n_col=100)
im = tol.add_border(im)
og_im = np.copy(im)


def get_im():
    return np.copy(og_im)


def display_im(image, winname='ToL', delay=100):
    cv2.imshow(winname, image)
    cv2.waitKey(delay)


start_pause = 30
mid_pause = 10
end_pause = 10
fade_len = 30

total_frames = sum([start_pause, mid_pause, end_pause, fade_len, fade_len])

fg_sparsity_range = np.linspace(0.8, 0.1, num=fade_len)
bg_sparsity_range = np.linspace(0.8, 0.8, num=fade_len)

for _ in range(start_pause):
    fg_sparsity = fg_sparsity_range[0]
    bg_sparsity = bg_sparsity_range[0]

    im = tol.add_noise(get_im(),
                       fg_palette=tol_gui.BG_PALETTE,
                       bg_palette=tol_gui.BG_PALETTE,
                       fg_sparsity=fg_sparsity,
                       bg_sparsity=bg_sparsity)
    im = imutils.resize(im, width=750)
    display_im(im)

for i in range(fade_len):
    fg_sparsity = fg_sparsity_range[i]
    bg_sparsity = bg_sparsity_range[i]

    im = tol.add_noise(get_im(),
                       fg_palette=tol_gui.FG_PALETTE,
                       bg_palette=tol_gui.BG_PALETTE,
                       fg_sparsity=fg_sparsity,
                       bg_sparsity=bg_sparsity)
    im = imutils.resize(im, width=750)
    display_im(im)

for _ in range(mid_pause):
    fg_sparsity = fg_sparsity_range[-1]
    bg_sparsity = bg_sparsity_range[-1]

    im = tol.add_noise(get_im(),
                       fg_palette=tol_gui.FG_PALETTE,
                       bg_palette=tol_gui.BG_PALETTE,
                       fg_sparsity=fg_sparsity,
                       bg_sparsity=bg_sparsity)
    im = imutils.resize(im, width=750)
    display_im(im)

for i in range(fade_len):
    fg_sparsity = fg_sparsity_range[-i]
    bg_sparsity = bg_sparsity_range[-i]

    im = tol.add_noise(get_im(),
                       fg_palette=tol_gui.FG_PALETTE,
                       bg_palette=tol_gui.BG_PALETTE,
                       fg_sparsity=fg_sparsity,
                       bg_sparsity=bg_sparsity)
    im = imutils.resize(im, width=750)
    display_im(im)

for _ in range(end_pause):
    fg_sparsity = fg_sparsity_range[0]
    bg_sparsity = bg_sparsity_range[0]

    im = tol.add_noise(get_im(),
                       fg_palette=tol_gui.BG_PALETTE,
                       bg_palette=tol_gui.BG_PALETTE,
                       fg_sparsity=fg_sparsity,
                       bg_sparsity=bg_sparsity)
    im = imutils.resize(im, width=750)
    display_im(im)
