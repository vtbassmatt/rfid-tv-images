import math
import random
from tkinter import Tk, ttk

from PIL import Image
from PIL.ImageTk import PhotoImage

WINDOW_PADDING = 1 # very narrow
BUTTON_PADDING = -2 # whatever it takes to totally remove padding

WORK_DELAY_MS = 200 # how many milliseconds to wait to perform next work

IMAGES = [
    'assets/microscope.webp',
    'assets/orrery.jpeg',
    'assets/test_tube.webp',
]


def get_window_size(root: Tk):
    geom = root.geometry()
    # root.geometry() gives back a string like "1280x800+0+0"
    # we want to drop the bits after '+' and then split at the 'x'
    # and also we want to account for the window and button padding
    width_height, _ = geom.split('+', 1)
    width, height = [int(x) - 2*WINDOW_PADDING for x in width_height.split('x', 1)]
    return width, height


def get_image(window_width: int, window_height: int):
    filename = random.choice(IMAGES)
    im = Image.open(filename)
    im_width, im_height = im.size

    # unpacking the logic below...
    #   ratio of width = image width / available width
    #   ratio of height = image height / available height
    #   if either ratio is > 1, we are shrinking, so pick the larger one to make sure we fit
    #   if both ratios are < 1, we would need to grow, and we don't want to do that
    # use the largest number as a scale factor if it's >= 1
    scale_factor = max(im_width / window_width, im_height / window_height)
    target_width = window_width if scale_factor < 1 else math.floor(im_width / scale_factor)
    target_height = window_height if scale_factor < 1 else math.floor(im_height / scale_factor)
    im_resized = im.resize((target_width, target_height))
    return PhotoImage(im_resized)


def maybe_rotate_image(root: Tk, btn: ttk.Button):
    # one in 10 times, we choose a new image
    if random.random() > .9:
        width, height = get_window_size(root)
        tkim = get_image(width, height)
        btn.configure(image=tkim)
        # Python will garbage-collect the image immediately if we don't
        # hang onto a reference like this
        btn._keep_reference = tkim
    
    # schedule a future call to this method
    root.after(WORK_DELAY_MS, lambda: maybe_rotate_image(root, btn))


# make a full-screen window
root = Tk()
root.title("2023-24 Science Fair")
root.attributes("-fullscreen", 1)

# get the size of the window
root.update_idletasks()
width, height = get_window_size(root)

# load the first photo to use, resizing as needed
tkim = get_image(width, height)

# put a grid onto the window
frm = ttk.Frame(root, padding=WINDOW_PADDING)
frm.grid()

# put a photo button into the grid, clicking it will close the app
btn = ttk.Button(
    frm,
    text="Quit",
    image=tkim,
    padding=BUTTON_PADDING,
    command=root.destroy,
)
btn.grid(column=0, row=0)

# center the widgets
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# schedule image rotation
root.after(WORK_DELAY_MS, lambda: maybe_rotate_image(root, btn))

# run forever
root.mainloop()