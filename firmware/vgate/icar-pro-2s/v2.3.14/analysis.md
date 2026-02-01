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

## Notes
- Official file naming suggests chipset **MIC110301** (Vgate internal ID)
- The update appears to target an ELM327-compatible stack with custom AT commands

---

**Status**: ✅ Initial triage complete
