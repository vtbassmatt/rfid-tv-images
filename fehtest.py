import subprocess
import time

print("pre-feh")

proc = subprocess.Popen(
    ["/usr/bin/feh", "-F", "-Y", "/home/pi/rfid-tv-images/assets/orrery.jpeg"],
)
pid = proc.pid

print(f"{pid=}")

time.sleep(5)

proc.terminate()

print("post-feh")
