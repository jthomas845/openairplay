from hashlib import md5


def hashes(method, uri, user, realm, pwd, nonce):
    payload = (
        'Digest username="{0}", realm="{1}", nonce="{2}", uri="{3}", response="{4}"'
    )

    ha1 = md5(f"{user}:{realm}:{pwd}".encode("utf-8")).hexdigest()
    ha2 = md5(f"{method}:{uri}".encode("utf-8")).hexdigest()
    print("DIGEST INFORMATION -------------")
    print (f"ha1 = {ha1}")
    print (f"nonce = {nonce}")
    print (f"ha2 = {ha2}")
    input_string = f"{ha1}:{nonce}:{ha2}"
    print(f"Input string: '{input_string}'")
    # Convert the input string to bytes and then to hex
    hex_dump = input_string.encode('utf-8').hex()

    # Split the hex dump into groups of 2 characters (1 byte each)
    grouped_hex = ' '.join([hex_dump[i:i+2] for i in range(0, len(hex_dump), 2)])

    print(f"Hex Dump of Input Bytes: {grouped_hex}")

    print("hashed: ", md5(input_string.encode("utf-8")).hexdigest())
    print(f"Raw Input String (repr): {repr(input_string)}")
    print(f"Nonce Used: '{nonce}' (length: {len(nonce)})")
    for i, c in enumerate(nonce.encode('utf-8')):
        print(f"Byte {i}: {c:02X} ({chr(c) if 32 <= c <= 126 else '?'})")
    if any(c in '\n\t\r ' for c in nonce):
        print(f"Warning: Nonce has extra spaces or newlines! '{repr(nonce)}'")

    print(f"Hex Dump of Nonce: {nonce.encode('utf-8').hex()} (Length: {len(nonce)})")

    di_response = md5(f"{ha1}:{nonce}:{ha2}".encode("utf-8")).hexdigest()
    print (payload.format(user, realm, nonce, uri, di_response))

hashes("SETUP", "/auth-setup", "admin", "airplay", "", "nonce1236")