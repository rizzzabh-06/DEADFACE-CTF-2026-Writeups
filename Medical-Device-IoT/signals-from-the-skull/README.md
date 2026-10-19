# DEADFACE CTF 2026 — Signals from the Skull

**Category:** Medical-Device-IoT / Bluetooth Low Energy  
**Points:** 300  
**Target:** Emedra CerebraScan CS-9000  
**Flag:** `deadface{un3ncrypt3d_b4bbl3_fr0m_th3_sku11}`

---

## Challenge Description

The CS-9000 broadcasts Bluetooth Low Energy traffic for remote maintenance. Most packets contain routine telemetry, while one characteristic leaks a maintenance log in small fragments.

**Goal:** Capture the BLE traffic, identify the log fragments, reassemble and decode them, then submit the flag in `deadface{...}` format.

## 1. Open the Device Interface

The challenge links to `https://emedra.dctf.io:8080`, but that address failed to load in the browser. Opening the same host and port over HTTP worked:

```text
http://emedra.dctf.io:8080
```

**Finding:** The page presented a 3D CS-9000 device and a toolkit containing several tools, including a BLE Sniffer USB-A.

## 2. Connect the BLE Sniffer

I selected **BLE Sniffer USB-A**, then clicked the device’s **USB-A Port**.

**Finding:** A capture window appeared. It described the capture as passive and the telemetry as unencrypted. Packets were listed with a handle, sequence number, payload length, and hex data.

## 3. Identify the Maintenance-Log Characteristic

The capture contained packets from two handles:
* `0x2a`: many 6-byte packets with apparently random-looking payloads.
* `0x37`: 12-byte packets with sequence numbers from 0 to 23.

The second set stood out because its packets were longer and formed a complete, ordered sequence. That made handle `0x37` the likely maintenance-log characteristic.

**Finding:** The fragments to reassemble were the payloads for handle `0x37`, ordered by `seq`.

## 4. Reassemble the Fragments

I sorted the `0x37` packets by sequence number and concatenated their hex payloads. Converting the combined hex to ASCII yielded a Base64-encoded string:

```text
U3QuRHltcGhuYSBDUy05MDAwIG1haW50IGxvZyB8IHNpdGU9c3Rkd21waG5hLXJtYy0wMSB8IHRlY2g9ZW1lZHJhLXN2YwpsYXN0X3BhdGllbnQ6IEdpZGVvbiBNYXJzaCAoTVJOIDEwMDQxMykKbm90ZTogdGVsZW1ldHJ5IHVuZW5jcnlwdGVkIHBlciBFTS0yMDE5IGRlZmF1bHQ7IGZsYWcgZGVhZGZhY2V7dW4zbmNyeXB0M2RfYjRiYmwzX2ZyMG1fdGgzX3NrdTExfQo=
```

**Finding:** The fragments formed valid Base64, indicating another encoding layer remained.

## 5. Decode the Log

Decoding the Base64 produced the maintenance log:

```text
St.Dymphna CS-9000 maint log | site=stdwmphna-rmc-01 | tech=emedra-svc
last_patient: Gideon Marsh (MRN 100413)
note: telemetry unencrypted per EM-2019 default; flag deadface{un3ncrypt3d_b4bbl3_fr0m_th3_sku11}
```

**Finding:** The flag was embedded directly in the log’s note.

## Flag

```text
deadface{un3ncrypt3d_b4bbl3_fr0m_th3_sku11}
```

