# Quick Start: Using Rayfall with ADI Files

## Why Use ADI Import?

✅ **No API Key Required** - Works completely offline  
✅ **Privacy First** - Your logs never leave your computer  
✅ **Universal** - Works with logs from any software  
✅ **Fast** - Instant loading, no network delays  

---

## Step-by-Step Guide

### 1. Export Your Log as ADI

**From QRZ Logbook:**
1. Go to https://logbook.qrz.com
2. Click "Logbook" → "ADIF"
3. Select date range
4. Click "Download ADIF"
5. Save the `.adi` file

**From Other Software:**
- **Log4OM**: File → Export → ADIF
- **WSJT-X**: File → Export ADIF
- **N1MM Logger+**: File → Export → ADIF
- **Ham Radio Deluxe**: Logbook → Export → ADIF

### 2. Import to Rayfall

1. Open Rayfall in your browser
2. Click **"Import ADI File"** button
3. Select your `.adi` or `.adif` file
4. Wait for "Loaded X QSOs" confirmation
5. Your contacts appear on the map!

### 3. Customize Your Map

Click **"⚙️ Display Options"** to:
- Change QTH station icon
- Select pin marker style
- Customize grid square colors
- Adjust opacity and precision

### 4. Export for Printing

1. Arrange your map as desired
2. Toggle visibility options
3. Click **"Export Map (300 DPI)"**
4. Print your high-resolution map!

---

## Supported ADI Fields

Rayfall reads these fields from your ADI file:

| Field | Purpose |
|-------|---------|
| `CALL` | Station callsign ✅ Required |
| `BAND` | Frequency band (e.g., 20m, 40m) |
| `MODE` | Operating mode (SSB, CW, FT8, etc.) |
| `QSO_DATE` | Date of contact |
| `TIME_ON` | Time of contact |
| `GRIDSQUARE` | Maidenhead locator |
| `LAT` / `LON` | Contact station coordinates |
| `MY_LAT` / `MY_LON` | Your station coordinates |
| `COUNTRY` | Contact's country |
| `STATE` | Contact's state (US/Canada) |
| `DISTANCE` | Distance in miles/km |

**Note:** Only `CALL` is required. Fields with coordinates or grid squares enable map plotting.

---

## Coordinate Formats Supported

### DMS Format (QRZ Standard)
```
LAT: N039 02.244
LON: W077 24.538
```

### Decimal Format
```
LAT: 39.037400
LON: -77.408967
```

Both formats are automatically detected and converted!

---

## Troubleshooting

### "No valid QSOs found in ADI file"

**Possible causes:**
- File is corrupted or not valid ADIF format
- No QSOs have `CALL` field
- File encoding issues

**Solutions:**
- Try re-exporting from your logging software
- Open file in text editor to verify format
- Ensure file starts with `<ADIF>` header

### QSOs load but don't appear on map

**Cause:** Missing coordinates or grid squares

**Solution:** 
- Ensure your logging software looks up coordinates
- Or enable QRZ lookups in your logger
- Or use QRZ API method for automatic coordinate lookup

### Wrong coordinates on map

**Cause:** Some loggers use different DMS formats

**Solution:**
- Check if coordinates look reasonable in your ADI file
- Report the format on GitHub for support

---

## ADI + QRZ API: Best of Both Worlds

You can use both methods:

1. **Import ADI** for bulk of your log
2. **Use QRZ API** for recent contacts with full data
3. Mix and match as needed!

---

## Privacy & Security

### Your Data Stays Local
- ADI files are processed in your browser
- No upload to servers
- Works completely offline
- No logging or tracking

### Safe for Sensitive Operations
- Field operations
- POTA/SOTA activations
- Contest logging review
- Award progress tracking

---

## Sample ADI File

Here's a minimal example:

```adif
ADIF Export
<ADIF_VER:5>3.1.0
<EOH>

<CALL:5>W1ABC <BAND:3>20m <MODE:3>SSB <QSO_DATE:8>20260301 <TIME_ON:4>1430 <GRIDSQUARE:6>FN31pr <eor>
<CALL:5>K2XYZ <BAND:3>40m <MODE:2>CW <QSO_DATE:8>20260301 <TIME_ON:4>1530 <LAT:11>N042 45.123 <LON:11>W073 30.456 <eor>
```

Each QSO ends with `<eor>` (end of record).

---

## Tips for Best Results

1. **Include Grid Squares**: Enable grid lookup in your logger
2. **Use Consistent Dates**: Helps with filtering and export
3. **Add States/Countries**: Enriches popup information
4. **Regular Exports**: Keep your maps up to date

---

## Get Creative!

### Contest Analysis
Export just your contest QSOs and visualize propagation patterns

### Award Progress
Import your entire log and use grid squares to see what you need

### Field Day Memories
Import Field Day logs with custom icons and colors

### Comparison Maps
Import different time periods with different grid colors

---

## Need Help?

- 📧 Questions? Open an issue on GitHub
- 🐛 Found a bug? Report it!
- 💡 Feature ideas? We're listening!
- ⭐ Like Rayfall? Star us on GitHub!

**Created by N2CLW - 73!** 📻
