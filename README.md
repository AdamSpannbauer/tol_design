# Gen 'random' design for ToL

### Getting started:
1. Install python3 & pip (some dude prolly wrote a good tutorial of how to do that)
2. Navigate to this folder via command line
3. Run `pip install -r requirements.txt`
4. Run `python3 tol_gui.py`
4. See Usage below for more

### Usage:
#### With defaults
`python3 tol_gui.py`

##### With options
`python3 tol_gui.py --input 'path_to_image.png' --output 'path/to/output/folder' --width 100`

#### Arguments:

```
  --input    Path to png image to use.
  --output   Directory name to save output images to.
  --width    Width of output image in pixels (doesn't affect display size).
```

#### Other options
You can make color modifications by editing `BG_PALETTE` and `FG_PALETTE` constants in `tol_gui.py`.
