# DEADFACE CTF 2026 — Bad Guys Be Bad

**Category:** Network Forensics / Traffic Analysis  
**Points:** 350  
**Artifact:** `deadface_pcap02.pcap`  
**Flag:** `deadface{{c2_traffic_be_bussing}}`

---

## Challenge Summary

The flag is `deadface{{c2_traffic_be_bussing}}`.

The key clue was the DNS traffic from `192.168.1.50` to `exfil.deadface-c2.net`. Before the data appeared, the machine queried `sync.deadface-c2.net` for TXT records. One response decoded from Base64 to:

```text
fetch:http://45.13.37.7:8080/staging.bin
```

I followed that lead in the capture and found a request for `/staging.bin`. The returned staging configuration contained:

```ini
channel=dns
xor_key=Sp00ky
target=exfil.deadface-c2.net
```

The DNS queries to that target carried five numbered chunks, from `s00` through `s04`. I joined their encoded portions in order:

```text
G4KVCVANDAYBKS2TLETCOASRKYGRAMBPKJKTIGZGANBVSBI6FY
```

Decoding that string from Base32 produced binary data. XORing the bytes with the repeating key `Sp00ky` revealed:

```text
deadface{{c2_traffic_be_bussing}}
```

The Base64 text in the staging download’s User-Agent decodes to `“nice try - wrong thread, keep digging.”` It was a decoy; the staging file’s DNS channel and XOR key pointed to the actual exfiltrated data.

