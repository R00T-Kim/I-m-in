# Vgate iCar Pro 2S v2.3.14 — Initial Triage

**Source**: https://vgatemall.com/downloadcenter/  
**Download**: iCar Pro 2S_v2.3.14.rar (actually ZIP)  
**Date**: 2026-02-01

---

## Key Findings

### 1) Archive type mismatch
- File extension: `.rar`
- Actual format: **ZIP** (confirmed by `binwalk` and `7z`)

### 2) Extracted contents
```
extracted/iCarPro2S_v2.3.14/
├── MIC110301_changelog.txt
├── MIC110301_v2.3.14.txt
├── vLinkerFwUpdater v4.0.exe
└── iCar upgrade manual.pdf
```

### 3) Changelog highlights
**MIC1103 ChangeLog**
- v2.3.14 (2025/06/19):
  - ATTA hh command modifies received CAN protocol extension address
  - Bugfix: J1850 protocol data impacting ISO reception
- v2.3.12 (2025/02/11): Added `VTVLRDhh`
- v2.3.10 (2024/10/29): VPW receive supports 4128 bytes
- v2.3.08 (2024/10/22): Added `VTSWGP FC1/0..FA1/0`
- v2.3.04 (2024/05/25): Added `VTMFCA`, fixed ISO 5-baud init

### 4) Firmware payload
- `MIC110301_v2.3.14.txt` is **large ASCII hex/text** (single-line style)
- Likely firmware image or patch data embedded as hex

### 5) Updater
- `vLinkerFwUpdater v4.0.exe` (PE32 GUI)
- Likely contains update protocol + may embed firmware decoding logic

---

## Immediate Next Steps

1. **Parse firmware hex file**
   - Determine structure (header/length markers)
   - Convert to binary for diff (`xxd -r -p` or custom parser)

2. **Unpack updater EXE**
   - Inspect with `strings` / `7z` / `binwalk`
   - Identify firmware protocol and any embedded keys

3. **Baseline archive**
   - Store raw ZIP in versioned directory
   - Record metadata (hashes, sizes)

---

## Progress Update (2026-02-01)

### Firmware parsing
- Converted `MIC110301_v2.3.14.txt` → `MIC110301_v2.3.14.bin`
- Size: **~99,722 bytes** (199,444 hex chars)
- `binwalk` shows **no embedded filesystem** (likely raw MCU firmware)
- `strings` on binary mostly unreadable (expected for raw firmware)

### Updater EXE strings (highlights)
- References to **Vgate** / **Icar01** / **Icar03** / **vLinker BM/FD/MC**
- Error messages suggest **firmware version gating**
  - “Please upgrade to version vLinker_*_V2.2.2X first!”
  - “The device firmware version number is higher, please use the latest firmware file.”
- Support contact: **support@vgate.com.cn**
- PDB path leaked (internal build path):
  - `D:\work\Vgate\VgateOTA\WindowsOTA\vLinkerFwUpdater\software\Release\vLinkerFwUpdater v4.0.pdb`

---

## Next Focus

1. **Firmware structure decoding**
   - Investigate MIC1103 format (header, checksum, record structure)
   - Identify if it's Intel HEX–like or custom record format

2. **Updater reverse**
   - Look for embedded updater protocol (serial/BT/WiFi?)
   - Extract any firmware signing/verification logic

---

## Progress Update (2026-02-01) — Format Triage

### Record structure observations
- Total lines: **834**
- All records share prefix **`110301`** (device/chip identifier)
- Record type distribution:
  - `DE` **708 records** (payload len 264 chars; 2 records len 40)
  - `DD` **12 records** (payload len 264 chars; 5 records len 136)
  - `DA` **9 records** (payload len 14 chars)
  - `EE` **102 records** (payload len 36 chars; 3 records len 12)
  - `55`, `AA` seen once each (likely header/magic sequence)
- File begins with **`11030155AA0114`** (magic/header)

**Hypothesis:** Custom HEX-like format:
```
110301 [TYPE] [FIELDS...] [DATA...] [CHECKSUM?]
```

**Initial DA decode (7 bytes)**
- Example: `DA00000011000100`
  - addr = `0x00000011`
  - len  = `0x0001`
  - chk? = `0x00`

### Updater EXE structure
- PE32 GUI, **no embedded archives** (only standard .rsrc assets)
- Sections: .text / .rdata / .data + resources
- Timestamp: **2024-02-21**
- Resources only (icons/dialogs/strings)

---

## Next Action (recommended)

1. **Parse DD/DA/EE records**
   - Extract suspected address fields
   - Validate checksum (if present)

2. **Map DD blocks into binary**
   - Rebuild full firmware image with address ordering
   - Compare with naive binary conversion

---

## Progress Update (2026-02-01) — Record Assembly Attempt

### Record observations (extended)
- `DE` payload length = **132 bytes** (likely header+data or data+checksum)
- `DD` payload length = **132 / 68 bytes**
- `DA` payload length = **7 bytes** (segment/address control)
- `EE` payload length = **18 / 6 bytes** (metadata/control)

### EE(18-byte) word pattern (9 x 16-bit)
Example: `0102020C0030000800040000000400000154`
```
[0x0102, 0x020C, 0x0030, 0x0008, 0x0004, 0x0000, 0x0004, 0x0000, 0x0154]
```
**Observed distributions by word position:**
- pos0: `0x0103` (91), `0x0102` (5), `0x0104` (3)
- pos1: constant `0x020C` (99)
- pos2: varies (`0x30`, `0x10`, `0x38`, `0x90`, ...)
- pos3: `0x0008` (66) or `0x0108` (33)
- pos4: mostly `0x0004`, sometimes `0x1000` / `0x20` / `0x28`
- pos6: often `0x800B`, occasionally `0x34FE` / `0xDEDC` / `0x365B`
- pos8: varying small sizes (`0x1E8`, `0x154`, `0x280`, ...)

### EE pattern correlation
- For records where **pos3=0x0008, pos4=0x0004, pos6=0x800B**:
  - `pos8 = pos2 + 0x1AC` (constant offset **428**)
  - pos2 increases by 4 → pos8 increases by 4 (table-like)

- For records where **pos3=0x0108, pos4=0x0004, pos6=0x800B**:
  - `pos8 = pos2 + 0x1AD` (offset **429**)
  - pos2 again increments by 4

**Implication:** EE records likely define a **range/table mapping** (index → offset).

### EE ↔ DE correlation
- DE records grouped by first 2 bytes:
  - `0b80` (91), `0c00` (89), `0c80` (88), `0d00` (88), `0d80` (88), `0e00` (88), `0e80` (88), `0f00` (88)
- EE pos6 value **0x800B** (swapped → `0b80`) appears **91 times**

**Inference:** EE records likely map **only the `0b80` block group**, while other DE groups are raw code/data outside the EE table.

### EE pos2 ↔ DE(0b80) tentative mapping
- EE pos2 values: **64 entries** (0..252 step 4)
- EE pos2 entries with 2 records: **25** → total **89** entries
- DE(0b80) long blocks: **89**

**Heuristic mapping:**
- Sort DE(0b80) blocks by header bytes `[2:4]` (big-endian)
- Assign 1 or 2 DE blocks per pos2, matching EE counts
- Output written: `ee_de_0b80_map.csv` (pos2,pos8,hdr2,...)

### EE-derived offset hypothesis (refined)
- In EE0b80 records, **pos3 is always 0x0008 or 0x0108**
  - When a pos2 has **two EE records**, pos3 values are always `{0x0008, 0x0108}`
- `pos8 - pos2` is usually **0x1AC** or **0x1AD**

**Working hypothesis:**
- **pos2** = table index (0..252 step 4)
- **pos3** = length (8 or 264 bytes)
- **pos8** = offset (pos2 + 0x1AC/0x1AD)

Using offset = `pos8 - 0x1AC` and length = `pos3`, the mapped table size ≈ **430 bytes**.

**Artifacts:**
- `MIC110301_v2.3.14_0b80_tablemap.bin` (occupancy map)
- `MIC110301_v2.3.14_0b80_tablemap_data.bin` (filled with DE data slices)

> This still needs validation against actual firmware layout.

### Search in binary
- Exact match of `MIC110301_v2.3.14_0b80_tablemap_data.bin` **not found** in `MIC110301_v2.3.14.bin`
- No large contiguous run match (largest non-0xFF run length 293 bytes → not found)
- Binary contains multiple **0xFF padding runs** (largest ~60 bytes), but tablemap doesn’t align directly

**Implication:** The EE/DE table is likely **not stored verbatim** in the raw binary; it may be reconstructed at runtime or packed differently.

---

## Updater EXE — I/O path hints

`vLinkerFwUpdater v4.0.exe` imports show **serial COM usage**:
- `CreateFileA`, `ReadFile`, `WriteFile`
- `SetupComm`, `SetCommTimeouts`, `GetCommState`, `SetCommState`, `PurgeComm`

**Inference:** Firmware update likely over **UART/CDC (COM port)** rather than HTTP.
This is a prime area to look for **auth/signature enforcement** during update.

### Updater string artifacts (protocol hints)
- AT command traffic visible:
  - `ATE1`, `ATBRD11`, `ATBRTFF`, `ATRD`, `AT@3`, `ATRDSN`, `ATIELM327`
- Mentions **baud** and a specific message:
  - “Change the baud rate to **2Mbps!**”
- Error messages imply line-based update file parsing:
  - “Repeat three times error on %d line!”
  - “update file format error!”

**Implication:** updater likely speaks **ELM327/AT-style handshake**, then switches baud to high speed for transfer.

---

## Firmware line format quick check
- Line lengths (hex chars):
  - `DE`: 264 (706 lines), 40 (2 lines)
  - `DD`: 264 (7), 136 (5)
  - `DA`: 14 (9)
  - `EE`: 36 (99), 12 (3)
  - `55`, `AA`: 6 (1 each)

**Inference:** file is fixed-record, line-based update format.

**EE(6-byte) records** (3 entries) parsed as 3x16-bit words:
- `[0x010F, 0x0100, 0x0114]`
- `[0x0100, 0x0000, 0x0104]`
- `[0x0101, 0x0000, 0x0105]`

### Naive reconstruction (hypothesis)
- Assumption: first **4 bytes** in DE/DD are header, remaining is data
- Concatenated all DE/DD records (excluding first 4 bytes)
- **Resulting size:** **91,616 bytes** (`MIC110301_v2.3.14_concat.bin`)

### Checksum tests (failed)
- First 4 bytes of DE record **≠** CRC32(data)
- Last 4 bytes of DE record **≠** CRC32(data)
- Last 2 bytes **≠** simple sum(data)

**Conclusion:** format is custom; needs explicit field mapping.

---

## Notes
- Official file naming suggests chipset **MIC110301** (Vgate internal ID)
- The update appears to target an ELM327-compatible stack with custom AT commands

---

**Status**: ✅ Initial triage complete
