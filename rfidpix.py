from time import process_time
import atexit

from RPi import GPIO
from mfrc522 import SimpleMFRC522

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
        print("uid=%s text=%s" % (uid, text))

        print("Awaiting tag...")
        last_time = process_time()

except KeyboardInterrupt:
    raise SystemExit()
