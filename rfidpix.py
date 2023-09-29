import os
import shutil
import subprocess
from time import process_time
import atexit

from RPi import GPIO
from mfrc522 import SimpleMFRC522


# get the directory this file lives in
BASE_DIR = os.path.dirname(__file__)
# find student work directory
STUDENT_WORK_DIR = f'{BASE_DIR}/students/'
# make a dictionary which has just the base file name as the key
# and the full file path as the value. files should be named for
# the RFID tag ID they correspond to.
# for example:
# {
#   332664828692: '/my/directory/students/332664828692.jpg',
#   334561047487: '/my/directory/students/334561047487.png',
# }
# os.path.splitext splits a filename into "file" and ".ext",
# and we take the first half of that (the non-extension part).
# then we convert that to an int to make our lives slightly
# easier later on.
#
# NOTE! you can break things subtly here if you have two files with
# the same RFID tag base name but different extensions (think like
# "1.png" and "1.jpg"). don't do that!
IMAGES = {
    int(os.path.splitext(filename)[0]): f"{STUDENT_WORK_DIR}{filename}"
    for filename in os.listdir(STUDENT_WORK_DIR)
}

# find "feh" which is our image viewer
FEH_CMD = shutil.which("feh")
if FEH_CMD is None:
    raise SystemExit("could not find 'feh' image viewer; did you run `sudo apt install feh` yet?")


# use this to read from the RFID 522 device
reader = SimpleMFRC522()

# clean up GPIO when the program exits
atexit.register(lambda: GPIO.cleanup())

# store the last RFID tag ID we saw (we haven't seen one yet!)
last_id = None
# same for the last instance of the "feh" program
feh = None

# clean up feh when the program exits
atexit.register(lambda: feh.terminate() if feh else None)

# we wrap this in a "try" so we can capture the keyboard event
# later when we press Ctrl-C to exit
try:
    print("Awaiting tag...")
    # record the time we started this
    last_time = process_time()

    # loop forever (well, until Ctrl-C) waiting on a tag
    while True:
        # read the ID of the tag, but ignore the contents of the tag
        uid, _ = reader.read()

        # if we see the same tag again in under 3 seconds, skip it
        # this is called "debouncing" if you want to learn more
        if uid == last_id and process_time() - last_time < 3:
            continue

        # store the new last ID
        last_id = uid

        print(f"Tag detected: {uid=}")

        # if there's a running instance of feh, kill it
        if feh:
            feh.terminate()
            feh = None

        # if the tag ID matches an image we know about, show it
        if uid in IMAGES.keys():
            # arguments to feh are:
            # -F -- fullscreen
            # -Y -- hide cursor
            feh = subprocess.Popen([FEH_CMD, '-F', '-Y', IMAGES[uid]])
        else:
            print("  (no image with that tag ID)")

        print("Awaiting tag...")
        last_time = process_time()

# waaaay down here is where we jump when Ctrl-C is detected
except KeyboardInterrupt:
    # cleanly exit Python, which will exit this infinite loop
    raise SystemExit()
