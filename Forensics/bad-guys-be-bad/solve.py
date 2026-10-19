import base64

# Extracted DNS exfiltration chunks
parts = [
    "G4KVCVANDAYB",
    "KS2TLETCOASR",
    "KYGRAMBPKJKT",
    "IGZGANBVSBI6",
    "FY"
]

# Reconstruct the Base32 payload
encoded = "".join(parts)

# Add required Base32 padding
encoded += "=" * (-len(encoded) % 8)

# Decode Base32
raw = base64.b32decode(encoded)

# XOR key obtained from staging.bin
key = b"Sp00ky"

# Decrypt using repeating-key XOR
decoded = bytes(
    byte ^ key[i % len(key)]
    for i, byte in enumerate(raw)
)

print(decoded.decode())

