def vigenere_decrypt(ciphertext, key):
    key = key.upper()
    key_indices = [ord(k) - ord('A') for k in key]
    key_len = len(key_indices)
    key_pos = 0

    plaintext = []
    for ch in ciphertext:
        if ch.isalpha():
            shift = key_indices[key_pos % key_len]
            key_pos += 1
            if ch.isupper():
                base = ord('A')
                decrypted = chr((ord(ch) - base - shift) % 26 + base)
            else:
                base = ord('a')
                decrypted = chr((ord(ch) - base - shift) % 26 + base)
            plaintext.append(decrypted)
        else:
            plaintext.append(ch)

    return "".join(plaintext)

ciphertext = "nZ3ipU8_yy3p5_hvyKi0"
key = "LSGFIWRXFEAVP"
plaintext = vigenere_decrypt(ciphertext, key)

print("Ciphertext:", ciphertext)
print("Chess key: ", key)
print("Plaintext: ", plaintext)
print("Flag:      deadface{" + plaintext + "}")

