# DEADFACE CTF 2026 — Keypad Oracle

**Challenge:** Keypad Oracle  
**Category:** iOS app reverse engineering  
**Points:** 200

## Challenge summary

We are given an iOS Simulator app bundle named `Keypad-Oracle.app`. The app presents a keypad that accepts a four-digit PIN and displays an encoded result. The challenge asks us to recover the hidden message.

The bundle contains both the compiled app code and a JSON configuration file. By reading the configuration and understanding the code's transformation, we can try the small set of valid PINs and identify the one that produces readable text.

## 1. Inspect the app bundle

Unlike an APK, an iOS `.app` bundle is a directory. Start by listing its files:

```sh
find /path/to/Keypad-Oracle.app -maxdepth 2 -type f -print
```

This challenge's bundle includes:

- `Keypad-Oracle`: the app's main executable.
- `Keypad-Oracle.debug.dylib`: compiled app code used in the simulator build.
- `KeypadConfig.json`: keypad digit configuration.
- `Info.plist`: app metadata.
- `_CodeSignature/`: signature metadata.

The JSON configuration is immediately interesting because it contains one hex value for each digit from `0` to `9`:

```json
{
  "digits": {
    "0": "8e07513d09e6379a5b14f845137456c5f4974967c678c07e1a9025",
    "1": "d179fa8cf908d9ed599ab5967c4f8d362de70c1a791babc9b75bcc"
  }
}
```

The actual file has entries for all ten digits. Each value is 54 hexadecimal characters, which represents 27 bytes.

## 2. Look for clues in the compiled code

The executable code is Mach-O (the format used by macOS and iOS). A decompiler such as Hopper or Ghidra can make it easier to inspect. For a quick first pass, use `strings`:

```sh
strings -a /path/to/Keypad-Oracle.app/Keypad-Oracle.debug.dylib \
  | rg -i 'PinCipher|seedTable|binarySalt|outputLength|encode|Repeated digits|4-digit'
```

In this app, the readable symbol names and strings reveal useful hints:

- `PinCipherEngine` and `encode(pin)` point to the transformation routine.
- `seedTable` and `binarySalt` indicate the per-digit seed table and a fixed salt.
- `outputLength` is `0x1b`, or 27 bytes.
- The app tells us the PIN must contain four digits and cannot repeat a digit.

Those details make the search manageable: there are 10 × 9 × 8 × 7 = 5,040 valid PINs.

> `strings` is only a clue-finding tool. It does not explain how the code works. Use a disassembler/decompiler to follow the `encode`, `derive`, and `xor` functions.

## 3. Reconstruct the byte transformation

The code uses the JSON value for each entered digit as its seed. It processes the four PIN digits in order, with positions numbered `0` through `3`.

For each digit and each byte index `i` from `0` to `26`, it derives a byte. In simplified pseudocode, the relevant operations are:

```text
value = seed[i modulo seed length]
        XOR ((position + 1) * 33 modulo 256)
        XOR (digit * 19 modulo 256)
        XOR (i * 7 modulo 256)

rotate value left by ((digit + position + i) modulo 8) bits

value = value XOR ((i + digit + 11 * position) modulo 256)
```

Here, `XOR` is the bitwise exclusive-or operation. It combines two bytes bit by bit: a bit is 1 in the result when the corresponding input bits differ. All arithmetic that becomes a byte wraps modulo 256.

For each of the four PIN positions, the app derives a 27-byte sequence. It XORs those four sequences together, then XORs the result with a 27-byte salt stored in the compiled code. Finally, it displays the resulting bytes as hexadecimal text.

The operation is reversible, but for this challenge we do not need to reverse each step manually. We can reproduce the routine and try every valid PIN. The correct PIN yields bytes that decode to the hidden message.

## 4. Brute-force the valid PINs

The following Python script reproduces the transformation and checks all four-digit PINs without repeated digits. Save it as `solve.py` next to `KeypadConfig.json`, then run `python3 solve.py /path/to/KeypadConfig.json`.

```python
import itertools
import json
import sys

with open(sys.argv[1], encoding="utf-8") as f:
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
        value = rotate_left_8(value, digit + position + i)
        value ^= (i + digit + 11 * position) & 0xff
        result.append(value)
    return result


def encode(pin):
    combined = bytearray(OUTPUT_LENGTH)
    for position, digit in enumerate(pin):
        stream = derive(seeds[digit], digit, position)
        for i, value in enumerate(stream):
            combined[i] ^= value
    return bytes(value ^ salt for value, salt in zip(combined, SALT))


for pin in itertools.permutations(range(10), 4):
    result = encode(pin)
    # A likely flag/message is readable ASCII and begins with the challenge prefix.
    if result.startswith(b"deadface{"):
        print("PIN:", "".join(map(str, pin)))
        print("Message:", result.decode("ascii"))
        print("Hex:", result.hex())
```

The salt is 28 bytes in this transcription while the output is 27 bytes; Python's `zip` stops at the shorter input, so only the first 27 salt bytes are used. The binary constant has a final `53` byte; it is part of the extracted salt, while the 27-byte output length controls how many bytes participate.

Expected result:

```text
PIN: 3719
Message: deadface{your-pin-is-valid}
Hex: 64656164666163657b796f75722d70696e2d69732d76616c69647d
```

## 5. Confirm the result

The message bytes are ordinary ASCII. The hex output converts to:

```text
deadface{your-pin-is-valid}
```

The PIN order matters because each position changes the derivation. The digits must also be unique, as enforced by the app's interface.

## Flag format note

The challenge text says to enter the flag as `deadface {flag_text}` with a space after `deadface`. The app-generated message itself is `deadface{your-pin-is-valid}` with no space. Follow the event platform's exact expected syntax; the recovered message is the no-space string shown above.

## Solution recap

1. Treat the `.app` as a directory and inspect its files.
2. Read `KeypadConfig.json` to get the ten digit seeds.
3. Inspect the compiled code to identify the 27-byte output, salt, and derive/XOR steps.
4. Reproduce those steps and try all 5,040 unique four-digit PINs.
5. PIN `3719` produces `deadface{your-pin-is-valid}`.
