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
