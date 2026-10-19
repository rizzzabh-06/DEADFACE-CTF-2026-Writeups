# DEADFACE CTF 2026 — Chess Key
## Chess-Based Vigenère Cryptography Writeup

**Challenge:** Chess Key  
**Points:** 200  
**Competition:** DEADFACE CTF 2026  
**Techniques:** Chess PGN Analysis, Coordinate Mapping, Vigenère Cipher  
**Status:** Offline decoding completed; flag acceptance unconfirmed

---

## 1. Challenge Overview

The challenge provided an encrypted message and an unusual 8×8 chessboard containing letters instead of traditional chess pieces.

The ciphertext was:

```
nZ3ipU8_yy3p5_hvyKi0
```

We needed to determine the intended chess game, transform the player's moves into an encryption key, and use that key to decrypt the message.

The accompanying GhostTown clue referred to Magnus Carlsen and a game from 2026 involving the English Opening.

The central insight was that the chessboard functioned as a substitution grid. Each chess square corresponded to a letter, and the sequence of Carlsen's moves could be converted into a cryptographic key.

## 2. Analyzing the Chessboard

The provided image contained the following 8×8 alphabetic grid.

The coordinates follow the standard chessboard orientation: files `a` through `h` from left to right, and ranks `8` through `1` from top to bottom.

```text
      a b c d e f g h

8     A I W Y A F I O
7     J B K B F J P U
6     X L C M K Q V A
5     Z C N D O W B E
4     D G L P E Q F I
3     H M R X R F S K
2     N S Y C G T G U
1     T Z D H J L V H
```

For example:

- Square `c4` contains `L`.
- Square `g3` contains `S`.
- Square `g2` contains `G`.

This suggested that chess moves could be translated into letters by reading the destination square of each move.

## 3. Finding the Relevant Magnus Carlsen Game

The provided `Carlsen.zip` archive contained a PGN file holding thousands of recorded chess games.

We searched the games for the following characteristics:

- Magnus Carlsen played as White.
- The match occurred during 2026.
- The first move was `1.c4`, indicating the English Opening.

A matching game that produced a meaningful cryptographic result was:

| Field | Value |
|---|---|
| White | Magnus Carlsen |
| Black | Aleksandar Indjic |
| Date | January 13, 2026 |
| Event | Titled Tuesday |
| Opening | English Opening |
| ECO | A20 |
| Result | 1–0 |

The PGN began:

```text
1.c4 e5
2.g3 Nc6
3.Bg2 h5
4.Nf3 e4
5.Nh4 g5
6.Nf5 h4
7.Nc3 Nf6
8.d3 d6
9.g4 Nxg4
10.Bxe4 Nh6
11.Nxh6 Bxh6
12.Rg1 Ne5
13.d4 Nc6
```

We used only Carlsen's moves, ignoring Black's replies.

## 4. Building the Chess-Based Encryption Key

For each of Carlsen's first 13 moves, we extracted the destination square and looked up the corresponding letter on the supplied board.

| Move | Destination | Letter |
|---|---|---|
| 1. c4 | c4 | L |
| 2. g3 | g3 | S |
| 3. Bg2 | g2 | G |
| 4. Nf3 | f3 | F |
| 5. Nh4 | h4 | I |
| 6. Nf5 | f5 | W |
| 7. Nc3 | c3 | R |
| 8. d3 | d3 | X |
| 9. g4 | g4 | F |
| 10. Bxe4 | e4 | E |
| 11. Nxh6 | h6 | A |
| 12. Rg1 | g1 | V |
| 13. d4 | d4 | P |

Concatenating the letters produced:

```
LSGFIWRXFEAVP
```

This became our Vigenère decryption key.

## 5. Identifying the Encryption Method

The ciphertext contained uppercase letters, lowercase letters, digits, and underscores.

We tested a standard Vigenère decryption using the chess-derived key.

The Vigenère decryption formula is:

\[
P_i = (C_i - K_i) \bmod 26
\]

Where:

- \(P_i\) is the decrypted character.
- \(C_i\) is the encrypted character.
- \(K_i\) is the corresponding key character.
- Characters are represented using `A = 0` through `Z = 25`.

For this interpretation, digits and underscores are preserved and do not consume key characters.

We also preserve the original alphabetic character case.

## 6. Python Decryption Script

The following script reproduces the chessboard lookup and Vigenère decryption without any external dependencies.

```python
board = [
    "AIWYAFIO",  # Rank 8
    "JBKBFJPU",  # Rank 7
    "XLCMKQVA",  # Rank 6
    "ZCNDOWBE",  # Rank 5
    "DGLPEQFI",  # Rank 4
    "HMRXRFSK",  # Rank 3
    "NSYCGTGU",  # Rank 2
    "TZDHJLVH"   # Rank 1
]

destinations = [
    "c4", "g3", "g2", "f3", "h4",
    "f5", "c3", "d3", "g4", "e4",
    "h6", "g1", "d4"
]

# Create coordinate-to-letter mapping
square_map = {}

for row_index, row in enumerate(board):
    rank = 8 - row_index

    for col_index, letter in enumerate(row):
        file = chr(ord("a") + col_index)
        square = f"{file}{rank}"
        square_map[square] = letter

# Generate encryption key
key = "".join(
    square_map[square]
    for square in destinations
)

ciphertext = "nZ3ipU8_yy3p5_hvyKi0"

def vigenere_decrypt(text, key):
    result = []
    key_index = 0

    for char in text:
        if char.isascii() and char.isalpha():
            c = ord(char.upper()) - ord("A")
            k = ord(key[key_index % len(key)]) - ord("A")

            decoded = chr((c - k) % 26 + ord("A"))

            if char.islower():
                decoded = decoded.lower()

            result.append(decoded)
            key_index += 1
        else:
            result.append(char)

    return "".join(result)

plaintext = vigenere_decrypt(ciphertext, key)

print("Ciphertext:", ciphertext)
print("Chess key: ", key)
print("Plaintext: ", plaintext)
print("Flag:      deadface{" + plaintext + "}")
```

### Output

```text
Ciphertext: nZ3ipU8_yy3p5_hvyKi0
Chess key:  LSGFIWRXFEAVP
Plaintext:  cH3ckM8_ch3s5_cryPt0
Flag:       deadface{cH3ckM8_ch3s5_cryPt0}
```

The program reproduces this plaintext using the actual board coordinates and the selected Carlsen game.

## 7. Flag Candidate

The offline decoding produced:

```
deadface{cH3ckM8_ch3s5_cryPt0}
```

An earlier all-lowercase version was rejected by the challenge platform:

```
deadface{ch3ckm8_ch3s5_crypt0}
```

The mixed-case version preserves the ciphertext's capitalization and is mathematically consistent with the decryption.

However, platform acceptance of this corrected candidate has not yet been confirmed.

The supplied challenge SHA-256 was not matched to the available chessboard image or PGN archive. A file checksum does not independently establish whether a decoded flag is accepted.

## 8. Conclusion

Chess Key combined chess notation and classical cryptography into a single puzzle.

The investigation involved identifying a Magnus Carlsen game that matched the clues, extracting White's move destinations, mapping those destinations onto a custom alphabetic chessboard, and using the resulting letters as a Vigenère key.

The main lessons from the challenge were:

1. External contextual clues can identify cryptographic key material.
2. Chess PGN notation provides structured coordinate data.
3. Custom grids can act as substitution tables.
4. Correct handling of character case and nonalphabetic characters matters.
5. A reproducible local decryption does not by itself confirm that a CTF flag is accepted.

**Result:** A reproducible candidate flag was recovered offline. Final challenge validation remains pending.

---

*All analysis described in this writeup was performed locally using the supplied chessboard and PGN archive. No challenge-server submission was performed as part of the analysis.*
