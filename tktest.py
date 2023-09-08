import math

from tkinter import Tk, ttk

from PIL import Image
from PIL.ImageTk import PhotoImage

WINDOW_PADDING = 1 # very narrow
BUTTON_PADDING = -2 # whatever it takes to totally remove padding

# make a full-screen window
root = Tk()
root.title("2023-24 Science Fair")
root.attributes("-fullscreen", 1)

# get the size of the window
root.update_idletasks()
geom = root.geometry()
# root.geometry() gives back a string like "1280x800+0+0"
# we want to drop the bits after '+' and then split at the 'x'
# and also we want to account for the window and button padding
width_height, _ = geom.split('+', 1)
width, height = [int(x) - 2*WINDOW_PADDING for x in width_height.split('x', 1)]

# load a photo to use, resizing as needed
im = Image.open('assets/microscope.webp')
im_width, im_height = im.size

# unpacking the logic below...
#   ratio of width = image width / available width
#   ratio of height = image height / available height
#   if either ratio is > 1, we are shrinking, so pick the larger one to make sure we fit
#   if both ratios are < 1, we would need to grow, and we don't want to do that
# use the largest number as a scale factor if it's >= 1
scale_factor = max(im_width / width, im_height / height)
target_width = width if scale_factor < 1 else math.floor(im_width / scale_factor)
target_height = height if scale_factor < 1 else math.floor(im_height / scale_factor)
im_resized = im.resize((target_width, target_height))

# put a grid onto the window
frm = ttk.Frame(root, padding=WINDOW_PADDING)
frm.grid()

# put a photo button into the grid, clicking it will close the app
tkim = PhotoImage(im_resized)
ttk.Button(
    frm, image=tkim, padding=BUTTON_PADDING,
    command=root.destroy
).grid(column=0, row=0)

# center the widgets
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# run forever
root.mainloop()