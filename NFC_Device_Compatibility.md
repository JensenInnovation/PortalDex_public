# Android NFC Device Compatibility (MIFARE Classic)

PortalDex reads Skylanders figures via Android's `MifareClassic` API
([nfc_scanner.dart](../portaldex_flutter/lib/services/nfc_scanner.dart)), authenticating
sector 0 with a known Key A. Skylanders figures are MIFARE Classic 1K chips, and MIFARE
Classic's Crypto-1 authentication is only supported by phones whose NFC controller chip
licenses it (almost always **NXP** controllers). Phones with Broadcom or some Qualcomm NFC
controllers can do NFC/NDEF/Google Pay but cannot authenticate MIFARE Classic sectors at
all — this is a hardware limitation, not something the app can work around.

Source: crowdsourced device reports from the
[MIFARE Classic Tool](https://github.com/ikarus23/MifareClassicTool) project, which uses
the same Android `MifareClassic` API as PortalDex. Neither list below is complete or
authoritative — it only reflects devices that have actually been tested by someone.

## ✅ Known compatible (MIFARE Classic works)

- **Google**: Pixel 1 through Pixel 8a, Nexus 6P
- **Samsung**: Galaxy S3, S7, S8–S24 FE (outside the exceptions below), most A-series
  released after ~2019
- **OnePlus**: 3, 3T, 5, 5T, 6, 6T, 7, 7 Pro
- **Xiaomi / Redmi**: most Mi and Redmi models (except Mi 3)
- **Sony**: Xperia Z, Z1, Z5, X, XA lines
- **Huawei**: P and Mate series (most)
- **Motorola**: most models released before 2014's Moto X generation
- **Asus, BQ, Honor, HTC (most), Lenovo, LG (most), Nokia, Philips, Wiko, Yota, ZTE (most)**

## ❌ Known incompatible (cannot read MIFARE Classic)

- **Samsung**: Galaxy S4, S4 Mini, S5 Mini, S5 Neo, S6, S6 Edge, S6 Edge Plus, S7 Edge,
  Alpha, Ace 3, Ace 4, Mega, Express 2, Xcover 3, A3 (2015), A5 (2016), A7 (2016/2017),
  A8 (2018), A9 (2016), J3 (2016), J5 (2017), J7 (2016/2017), Note 3, Note 4, Note 5,
  Note 6, Grand Prime
- **Google Nexus**: 4, 5, 6, 7 (2013), 9, 10
- **Motorola**: Moto X (2014, 2nd gen.), Moto X Style, Moto X Play, Moto X Force,
  Droid Turbo, Moto Maxx, One Vision Plus
- **LG**: G2, G2 mini, G3 S, G4 Beat, K10, V10, F60, Optimus L7 II, Phoenix 2
- **HTC**: One M8
- **Sony**: Xperia X Compact, Z2, Z3
- **Xiaomi**: Mi 3
- **Other**: BlackBerry Priv, Fairphone 3, Asus Zenfone 2, Nubia Z18, ZTE Nubia Z7 Max
  (NX505J), Blackview BV5500 Pro/Plus, Blackview BV8000 Pro, Doogee S60, Jiayu S3,
  Lenovo Vibe P1/P2, Foxconn InFocus M320, Sharp Aquos Zero 2, Sharp SH-02G
- **iPhone**: all models
  

## What to tell users

If a phone isn't on either list, the only reliable test is trying a real figure on it.
The app's in-scan error message already distinguishes "not a genuine figure / bad read"
from "this hardware may not support MIFARE Classic at all" — see the `reason` branches in
[nfc_scanner.dart](../portaldex_flutter/lib/services/nfc_scanner.dart).
