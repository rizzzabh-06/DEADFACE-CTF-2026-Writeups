# DEADFACE CTF 2026 — Challenges & Writeups

[![CTF](https://img.shields.io/badge/CTF-DEADFACE%202026-red.svg)](https://deadface.io)
[![Challenges](https://img.shields.io/badge/Challenges-12%20Writeups%20%7C%2019%20Flags-brightgreen.svg)](#challenge-index)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

This repository contains detailed writeups, methodology notes, exploit payloads, and solve scripts for **DEADFACE CTF 2026**.

All challenges are organized strictly by category, with structured writeups and reproducible solve scripts.

---

## Repository Structure

```text
DEADFACE-CTF-2026-Writeups/
├── Cryptography/              # Vigenère coordinate ciphers & chess PGN cryptanalysis
│   └── chess-key/
├── Exploitation/              # Buffer overflows, ROP chains & Linux privilege escalation
│   ├── hostbusters-charon/
│   ├── skeleton-key/
│   └── the-crypt/
├── Forensics/                 # C2 DNS exfiltration, packet captures & HTTP header smuggling
│   ├── a-pirates-life-for-me-part-1/
│   └── bad-guys-be-bad/
├── Medical-Device-IoT/        # Emedra CerebraScan CS-9000 scanner firmware & BLE telemetry
│   ├── bad-calibration/
│   └── signals-from-the-skull/
├── Mobile-Security/           # Android APK reverse engineering & iOS simulator PIN cracking
│   ├── keypad-oracle/
│   └── locked-or-not/
└── Web-Exploitation/          # Health Spark portal SQLi credential leaks & multi-tenant IDOR
    ├── doctor-appointment/
    └── real-pain-in-the-prostate/
```

---

## Challenge Index

| Category | Challenge Name | Artifacts / Tools | Solved Flag |
|---|---|---|---|
| **Cryptography** | [Chess Key](./Cryptography/chess-key/README.md) | `solve.py`, Vigenère cipher, PGN analysis | `deadface{cH3ckM8_ch3s5_cryPt0}` |
| **Exploitation** | [Hostbusters: Charon](./Exploitation/hostbusters-charon/README.md) | Linux PrivEsc (8 stages: shell history, git, cron, sudo, caps, SUID PATH hijack) | `deadface{f00th0ld_p4st_th3_v31l}` *(8 flags)* |
| **Exploitation** | [Skeleton Key](./Exploitation/skeleton-key/README.md) | `solve.py`, 64-bit ELF buffer overflow, ROP gadget | `deadface{R355UR3CT_D34D_C0D3}` |
| **Exploitation** | [The Crypt](./Exploitation/the-crypt/README.md) | `solve.py`, ELF buffer overflow, ret2win (`nowhere`) | `deadface{d3crypt3d_1nt0_n0th1ng}` |
| **Forensics** | [A Pirate’s Life for Me (Part 1)](./Forensics/a-pirates-life-for-me-part-1/README.md) | PCAPNG packet capture, HTTP custom header trace | `deadface{X-M4rk5_th3_sp0t_I_gu355}` |
| **Forensics** | [Bad Guys Be Bad](./Forensics/bad-guys-be-bad/README.md) | `solve.py`, `deadface_pcap02.pcap`, DNS TXT C2 beacon & Base32/XOR tunnel | `deadface{c2_traffic_be_bussing}` |
| **Medical-Device-IoT** | [Bad Calibration](./Medical-Device-IoT/bad-calibration/README.md) | CS-9000 ScanWorks, SHA-256 signature forgery, threshold bypass | `deadface{c4l1br4t10n_f0rg3ry_h4rms_l1v3s}` |
| **Medical-Device-IoT** | [Signals from the Skull](./Medical-Device-IoT/signals-from-the-skull/README.md) | BLE sniffer capture, packet handle reassembly, Base64 | `deadface{un3ncrypt3d_b4bbl3_fr0m_th3_sku11}` |
| **Mobile-Security** | [Keypad Oracle](./Mobile-Security/keypad-oracle/README.md) | `solve.py`, `Keypad-Oracle.app`, Mach-O decompile, permutation cipher | `deadface{your-pin-is-valid}` |
| **Mobile-Security** | [Locked... or Not?](./Mobile-Security/locked-or-not/README.md) | `df-securenotes.apk`, JADX / `classes.dex`, hardcoded secret | `deadface{ez-mobile-to-start}` |
| **Web-Exploitation** | [Doctor Appointment (1 of 4)](./Web-Exploitation/doctor-appointment/README.md) | Health Spark portal, SQL Injection credential disclosure | `deadface{typical_and_classic}` |
| **Web-Exploitation** | [Real Pain in the Prostate (2 of 4)](./Web-Exploitation/real-pain-in-the-prostate/README.md) | Health Spark API, BOLA / IDOR across tenant departments | `deadface{hipaa_exposure_is_bad}` |

---

Happy Hacking & Learning :)
