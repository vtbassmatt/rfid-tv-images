# rfid-tv-images

A Raspberry Pi program for scanning RFID tags and displaying a corresponding image on screen.

# Requirements

Will only function on a Raspberry Pi. That Raspberry Pi also needs:
- Python 3.9+
- `feh` package
- The packages called out in `requirements.txt`, preferably in a venv
- Compiler tools to make `spidev` happy

The following should do it on a Debian-based system:

```ShellSession
sudo apt install python3 python3-venv feh
sudo apt install python3-dev gcc libc6
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

# Setup

I followed https://pimylifeup.com/raspberry-pi-rfid-rc522/ to get things wired and set up.
Pins were:
- SDA to pin 24
- SCK to pin 23
- MOSI to pin 19
- MISO to pin 21
- GND to pin 6
- RST to pin 22
- 3.3v to pin 1

In `raspi-config` (launch with `sudo`), under **3 Interfacing Options**, go to **I4 SPI**, enable it, and reboot.

Also you probably want your Raspberry Pi not to shut off the screen after 10 minutes.
Open `/etc/lightdm/lightdm.conf`, find the "SeatsDefault" or "Seats:*" section, and add:

```ini
xserver-command=X -s 0 -dpms
```

Then reboot.
