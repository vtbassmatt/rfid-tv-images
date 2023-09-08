# rfid-tv-images

A Raspberry Pi program for scanning RFID tags and displaying a corresponding image on screen.

# Requirements

Will only function on a Raspberry Pi. That Raspberry Pi also needs:
- Python 3.9+
- TKinter package for Python3
- The packages called out in `requirements.txt`, preferably in a venv
- Compiler tools to make `spidev` happy

The following should do it on a Debian-based system:

```ShellSession
sudo apt install python3 python3-tk python3-venv
sudo apt install python3-dev gcc libc6
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```