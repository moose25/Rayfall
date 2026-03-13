# Rayfall New Features - March 13, 2026

## Major Updates

### 1. ADI File Import 📁
**No API key required!** Users can now import their logbook directly from ADI/ADIF files.

**How to use:**
- Click "Import ADI File" button in the control panel
- Select your .adi or .adif file
- QSOs will be loaded and displayed on the map instantly
- Works offline - no internet connection needed!

**Benefits:**
- Privacy - no need to share API keys
- Works with any logging software that exports ADIF
- Faster loading for large logbooks
- Alternative for users without QRZ subscription

---

### 2. Display Options Dropdown Menu ⚙️
Cleaned up the UI by organizing all display-related controls into a dropdown menu.

**Located in:** Control panel, right side - "⚙️ Display Options" button

**Contains:**
- Map Style selector
- QTH Station Icon customization
- Pin Icon styles
- Grid Square appearance settings

---

### 3. QTH Station Icon Selector 🏠
Customize the icon that represents your home station!

**Available icons:**
- ⚡ Lightning Bolt (default)
- 📍 Pin
- 🏠 House
- 📡 Satellite Dish
- 🗼 Tower
- ⭐ Star

**Features:**
- Live preview next to selector
- Changes update instantly on the map
- Icon persists through filtering operations

---

### 4. Pin Icon Customization 📍
Choose different styles for your QSO markers!

**Available styles:**
- **Teardrop Pins** (default) - Classic map pin shape
- **Circle Markers** - Clean circular markers
- **Square Markers** - Square pins with center dot
- **Star Markers** - Star-shaped markers

**Features:**
- All styles maintain band color coding
- Instant preview on the map
- Optimal sizes for each style

---

### 5. Grid Square Customization 🎨

#### Color Picker
- Choose any color for grid square overlays
- Default: Golden (#FFD700)
- Updates labels to match selected color
- Perfect for creating themed maps

#### Opacity Slider
- Adjust transparency from 0% to 100%
- Default: 20%
- Live preview of current percentage
- Find the perfect balance between visibility and map detail

---

### 6. Interactive Help Guide 📖

**New "How to Use Rayfall" button** provides instant access to tutorials!

**Features:**
- Step-by-step instructions for QRZ API setup
- ADI file import guide with software-specific instructions
- Display customization tutorials
- Filtering and export instructions
- Pro tips for advanced users

**Located:** Top-right corner, next to "Change API Key" button

**Contents:**
- 🔑 Method 1: Using QRZ API
- 📁 Method 2: Import ADI/ADIF Files
- 🎨 Customizing Your Map
- 🔍 Filtering Contacts
- 🖨️ Exporting for Printing
- 💡 Pro Tips

---

## Updated UI Layout

### Top-Right Buttons
```
[📖 How to Use Rayfall] [🔑 Change API Key]
```

### Control Panel - Row 1
```
[Start Date] [End Date] [Load from QRZ] [Import ADI File] 
[Show Lines] [Color by Band] [⚙️ Display Options] [Export Map (300 DPI)]
```

### Display Options Dropdown
```
⚙️ Display Options
├─ Map Style
│  └─ [Light/Dark/Topo/Satellite/Streets]
├─ QTH Station Icon
│  ├─ [Icon Selector] [Preview]
│  └─ [✓] Show QTH Station
├─ Pin Icons
│  ├─ [Style Selector]
│  └─ [✓] Show Pins
└─ Grid Squares
   ├─ [✓] Show Grid Squares
   ├─ Precision: [4-char/6-char]
   ├─ Color: [Color Picker]
   └─ Opacity: [Slider] [20%]
```

---

## Use Cases

### Contest Logging Analysis
1. Export contest log as ADI file
2. Import to Rayfall (no API needed)
3. Choose 6-char grid precision
4. Select custom grid color (e.g., red for contests)
5. Adjust opacity for optimal visibility

### Clean Award Maps
1. Load QSOs
2. Choose satellite basemap
3. Select tower icon (🗼) for QTH
4. Use circle markers for clean look
5. Set grid color to match award theme
6. Export at 300 DPI

### Offline Operation
1. Export logs as ADI from your logging software
2. Import to Rayfall - works without internet
3. No API keys required
4. Perfect for field operations or demonstrations

---

## Technical Implementation

### ADI Parser
- Supports both .adi and .adif extensions
- Parses field length specifications
- Handles DMS and decimal coordinate formats
- Validates required fields (call, band, mode)
- Compatible with all major logging software

### Grid Square Styling
- Dynamic color application to borders and fills
- Opacity control with percentage display
- Label colors match grid color
- Instant updates without data reload

### Icon Systems
- SVG-based pin icons for crisp rendering
- Emoji-based QTH icons for universal compatibility
- Band color integration maintained across all styles
- Optimized sizes for each icon type

---

## Files Modified

### `templates/index.html`
**Additions:**
- ADI file import functionality (~100 lines)
- Display options dropdown menu (CSS + HTML)
- Pin icon generation system
- Grid style configuration system
- New control functions

**Changes:**
- Reorganized control panel layout
- Moved display options to dropdown
- Updated button text ("Load from QRZ" vs "Import ADI")
- Enhanced styling with dropdown CSS

---

## Backward Compatibility

✅ All existing features work exactly as before
✅ QRZ API loading still available
✅ Default icons and colors preserved
✅ No database or config file changes required
✅ Existing exports/screenshots unaffected

---

## Testing Checklist

- [ ] ADI file import with sample file
- [ ] QTH icon selector changes and updates map
- [ ] Pin style selector changes all markers
- [ ] Grid color picker updates overlays
- [ ] Grid opacity slider works smoothly
- [ ] Display dropdown opens/closes correctly
- [ ] All toggles work in dropdown
- [ ] **Help modal opens and displays all sections**
- [ ] **Help modal closes on button click or overlay click**
- [ ] Export includes custom icons and colors
- [ ] Works with QRZ API loading
- [ ] Works with ADI file loading
- [ ] Mobile/touch screen compatibility

---

## Future Enhancements (Ideas)

- Import from multiple ADI files simultaneously
- Save custom icon/color preferences to localStorage
- Export grid square list to CSV
- Animated propagation paths
- Custom pin images (user upload)
- Gradient grid colors based on date/distance
- Dark mode for dropdown menu

---

## User Feedback

Created by **N2CLW** based on community feature requests:
- ✅ ADI import for privacy-conscious users
- ✅ Icon customization for personalization
- ✅ Grid square styling for award applications
- ✅ Cleaner UI through dropdown organization

**Need help?** Visit [rayfall.me](https://rayfall.me) or open an issue on GitHub!

---

## Deployment

### Local Testing
```bash
cd Rayfall
python -m uvicorn main:app --reload
```
Visit: http://localhost:8000

### Production (homedash server)
```bash
ssh chris@homedash.taile9e59a.ts.net
cd ~/qrz-map
cp templates/index.html templates/index.html.backup
# Upload new index.html
sudo systemctl restart rayfall
```

Live at: https://rayfall.me

---

**73 and happy mapping! 📻📡🗺️**
