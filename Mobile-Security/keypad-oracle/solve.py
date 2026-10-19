import itertools
import json
import sys

# Usage: python3 solve.py [path_to_KeypadConfig.json]
config_file = sys.argv[1] if len(sys.argv) > 1 else "KeypadConfig.json"

with open(config_file, encoding="utf-8") as f:
    config = json.load(f)["digits"]

seeds = {int(digit): bytes.fromhex(value) for digit, value in config.items()}

# 28-byte salt recovered from the app's binary.
SALT = bytes.fromhex(
    "3a91442fd0186bc3720ea95d11be8027"
    "f466399a05cc701b8842e153"
)
OUTPUT_LENGTH = 27


def rotate_left_8(value, count):
    count %= 8
    if count == 0:
        return value
    return ((value << count) | (value >> (8 - count))) & 0xff


def derive(seed, digit, position):
    result = bytearray()
    for i in range(OUTPUT_LENGTH):
        value = seed[i % len(seed)]
        value ^= ((position + 1) * 33) & 0xff
        value ^= (digit * 19) & 0xff
        value ^= (i * 7) & 0xff
        shift = (digit + position + i) % 8
        value = rotate_left_8(value, shift)
        value ^= (i + digit + 11 * position) & 0xff
        result.append(value)
    return result


def encode_pin(pin):
    combined = bytearray(OUTPUT_LENGTH)
    for position, digit in enumerate(pin):
        stream = derive(seeds[digit], digit, position)
        for i in range(OUTPUT_LENGTH):
            combined[i] ^= stream[i]
    for i in range(OUTPUT_LENGTH):
        combined[i] ^= SALT[i]
    return bytes(combined)


for pin in itertools.permutations(range(10), 4):
    result = encode_pin(pin)
    if result.startswith(b"deadface{"):
        print("PIN:", "".join(map(str, pin)))
        print("Message:", result.decode("ascii"))
        print("Hex:", result.hex())

