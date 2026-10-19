# DEADFACE CTF 2026 — A Pirate’s Life for Me (Part 1)

**Category:** Forensics / Network Traffic Analysis  
**Points:** 100  
**Artifact:** PCAPNG packet capture  
**Flag:** `deadface{X-M4rk5_th3_sp0t_I_gu355}`

---

Challenge
We received a packet capture from a university café after several breaches. A barista noticed someone using an unfamiliar browser. The goal was to investigate the capture and submit the flag in the format deadface{flag-text}.
1. Check the capture
I first checked the file type, size, and SHA-256 hash. It was a large pcapng capture, which can be inspected with packet analysis tools such as tcpdump.
The file’s SHA-256 did not match the hash provided in the challenge:
* Challenge hash: 7bcebd81928b2d01718f2f853c507ea313a44e2b19037f4b7d0cc1c638affe93
* Supplied file hash: f96bfa4644c668009434f767eb138177fc5a8b582d728bf84300f5554e3b1de5
I continued investigating the supplied capture because it contained traffic matching the challenge description.
2. Look for the unfamiliar browser
I inspected the HTTP traffic and found requests from a client using this User-Agent:
SunstalkerDFBrower/2.0 (Linux; Android 14)
That unusual browser name was a strong lead. Its requests contacted several hosts, including:
nvucafe.com
birdsarejustbirds.gov
nightvaleuniversity.edu
aurorahhs.com
These names fit the challenge’s references to the café, university, government website, and hospital.
3. Inspect the requests for hidden data
I examined the HTTP requests from that client more closely. Three requests contained unusual custom headers:
Host: nightvaleuniversity.edu
X-1-Trace-Part: deadface{X-M4rk5_
Host: aurorahhs.com
X-2-Mark: th3_sp0t_
Host: birdsarejustbirds.gov
X-3-Spot: I_gu355}
The headers were numbered and their values formed consecutive pieces of a string. Joining the values in order gives:
deadface{X-M4rk5_th3_sp0t_I_gu355}
Flag
deadface{X-M4rk5_th3_sp0t_I_gu355}
The X-M4rk5_th3_sp0t_I_gu355 text resembles “marks the spot, I guess,” which reinforces that the three custom headers were intended to be assembled in order.

