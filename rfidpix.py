from pirc522 import RFID

reader = RFID()

while True:
    reader.wait_for_tag()

    # request() gives error=True if a tag is NOT present
    error, tag_type = reader.request()
    if error:
        continue

    print("Tag detected")
    error, uid = reader.anticoll()
    if error:
        continue

    print(f"UID: {uid}")

    # as far as I can tell, if we only intend to use the UID, then
    # there are no more methods we need to call. if we DO intend
    # to read the card, we have to do some .select_tag() and
    # .card_auth() and .stop_crypto() dancing. 

# clean up GPIO
reader.cleanup()
