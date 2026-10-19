# DEADFACE CTF 2026 — Locked... or Not?

**Challenge:** Locked... or Not?  
**Category:** Mobile / Android  
**Points:** 150  
**Flag format:** `deadface{...}`

## Challenge summary

The challenge gives us an Android APK for a simple secure-notes app. Opening the app is supposed to require a password to read one protected note. The goal is to inspect the app and recover the flag.

A useful starting idea for mobile challenges is: an APK is an archive containing the app's compiled code, resources, and manifest. A password prompt in the interface does not guarantee that the secret is stored securely. If the app needs the password or note contents locally, those values may be recoverable from its code.

## 1. Check the APK

First, locate the provided APK and check its SHA-256 hash. On macOS or Linux, run:

```sh
shasum -a 256 /path/to/df-securenotes.apk
```

The challenge page lists this hash:

```text
b5f6e9a0a75f404103fc2d08542165015f8934e8d76433a513ca1a4705f006ca
```

The APK examined for this writeup produced:

```text
f6758da2dddb28820edc86de4e001415b31d2ce9a678bfb78d4430cf34d4aca4
```

These do not match. That means the local APK is not byte-for-byte identical to the artifact identified by the challenge hash. The analysis below describes the APK at `/Users/rishabhrajsingh/Downloads/df-securenotes.apk`; if your copy has a different hash, verify that its contents match before assuming it will produce the same result.

## 2. List the APK contents

An APK is ZIP-formatted, so we can list its files with the standard `unzip` command:

```sh
unzip -l /path/to/df-securenotes.apk
```

The interesting entries here are:

- `classes.dex` and `classes2.dex`: compiled Android application code (DEX bytecode).
- `res/layout/`: compiled layouts describing screens and dialogs.
- `AndroidManifest.xml`: app components and metadata.
- `resources.arsc`: compiled app resources, such as strings and IDs.

The app's Java/Kotlin source is not normally included as readable `.java` files. The compiled DEX files are what we should inspect next.

## 3. Extract the APK

Create a working directory and unpack the archive:

```sh
mkdir apk-work
cd apk-work
unzip -o /path/to/df-securenotes.apk
```

The `-o` option lets `unzip` replace files if you repeat the extraction. Keep the original APK unchanged so you can re-check its hash later.

## 4. Inspect the compiled code

### Option A: Use JADX (recommended for beginners)

JADX decompiles DEX bytecode into Java-like source code, which is easier to read than raw bytecode. Open the APK with JADX's graphical interface, or run its command-line version:

```sh
jadx -d decompiled /path/to/df-securenotes.apk
```

Then search the decompiled files for words related to the protected note, such as `secure`, `password`, `backup`, or `Base64`. In this app, the relevant code is in `MainActivity` and handles the secure note's content.

### Option B: Search strings in DEX files

For a quick first pass, use the system `strings` utility:

```sh
strings classes.dex
strings classes2.dex
```

This lists readable text sequences embedded in each DEX file. It is a rough technique: it does not reconstruct the program, and it can miss text that is split up or encoded. Here it reveals several useful clues, including:

```text
getSecureBackupText
apiKeyBackup
Base64
ZGVhZGZhY2V7ZXotbW9iaWxlLXRvLXN0YXJ0fQ==
```

The last value looks like Base64. The nearby `Base64` and `decode` strings suggest the app decodes it at runtime. This is the key finding: the protected note's payload is embedded in the client-side app, rather than being fetched from a server after a password check.

## 5. Decode the embedded value

Base64 is an encoding, not encryption. It changes how bytes are represented as text; anyone who finds the value can reverse it without knowing a password.

Decode the string with Python:

```sh
python3 -c 'import base64; print(base64.b64decode("ZGVhZGZhY2V7ZXotbW9iaWxlLXRvLXN0YXJ0fQ==").decode())'
```

Output:

```text
deadface{ez-mobile-to-start}
```

You can also use a local Base64 decoder or a small script. Avoid pasting challenge data into unknown websites if you do not need to; a local decoder is enough.

## 6. Why the password prompt did not protect the flag

A password prompt is only meaningful if the app checks a secret in a way that prevents an attacker from recovering the protected data. In this challenge, the code includes a Base64-encoded string and decoding logic in the APK itself. Since users receive the APK, they can inspect its contents. Base64 does not provide confidentiality, and the app contains the data needed to reveal the flag locally.

For this CTF, the objective is to reverse engineer that behavior and recover the embedded value. In real apps, sensitive data should not be protected merely by hiding it in client code or encoding it. The appropriate design depends on the threat model, but secrets that must remain secret generally should not be shipped in recoverable form to every client.

## Flag

```text
deadface{ez-mobile-to-start}
```

## Short solution recap

1. Check and note the APK's SHA-256.
2. Unzip the APK and inspect `classes.dex` / `classes2.dex`.
3. Find the Base64-looking string near the app's decode logic.
4. Decode it locally.
5. Submit `deadface{ez-mobile-to-start}`.

**Artifact note:** The local APK hash did not match the hash printed in the challenge. Confirm you have the intended challenge file if this result does not match your copy.
