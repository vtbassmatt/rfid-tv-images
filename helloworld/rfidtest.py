from time import process_time
import atexit

from RPi import GPIO
from mfrc522 import SimpleMFRC522

KNOWN_TAGS = {
    468995568508: """ .    '                   .  "   '
            .  .  .                 '      '
    "`       .   .
                                     '     '
  .    '      _______________
          ==c(___(o(______(_()
                  \=\\
                   )=\\
                  //|\\\\
                 //|| \\\\
                // ||  \\\\
               //  ||   \\\\
              //         \\\\
""",
    334561047487: """ _____________________
|  _________________  |
| | JO           0. | |
| |_________________| |
|  ___ ___ ___   ___  |
| | 7 | 8 | 9 | | + | |
| |___|___|___| |___| |
| | 4 | 5 | 6 | | - | |
| |___|___|___| |___| |
| | 1 | 2 | 3 | | x | |
| |___|___|___| |___| |
| | . | 0 | = | | / | |
| |___|___|___| |___| |
|_____________________|""",
    332664828692: """+8-=-=-=-=-=-8+
 | ,.-'"'-., |
 |/         \|
 |\:.     .:/|
 | \:::::::/ |
 |  \:::::/  |
 |   \:::/   |
 |    ):(    |
 |   / . \   |
 |  /  .  \  |
 | /   .   \ |
 |/   .:.   \|
 |\.:::::::./|
 | '--___--' |
+8-=-=-=-=-=-8+""",
}


reader = SimpleMFRC522()

# clean up GPIO
atexit.register(lambda: GPIO.cleanup())

last_id = None

try:
    print("Awaiting tag...")
    last_time = process_time()

    while True:
        uid, text = reader.read()

        # if we see the same tag again in under 3 seconds, skip it
        if uid == last_id and process_time() - last_time < 3:
            continue
        last_id = uid

        print("Tag detected")
        # print(f"{uid=} {text=}")
        if uid in KNOWN_TAGS:
            print(KNOWN_TAGS[uid])
        else:
            print("uid=%s text=%s" % (uid, text))

        print("Awaiting tag...")
        last_time = process_time()

except KeyboardInterrupt:
    raise SystemExit()
