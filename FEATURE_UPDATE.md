# Rayfall Feature Update - Grid Squares & High-Res Export

## Date: March 13, 2026

## New Features Implemented

### 1. Grid Square Map Overlay
- **Feature**: Display worked Maidenhead grid squares on the map
- **How to use**: 
  - After loading QSOs, check the "Show Grid Squares" checkbox in the control panel
  - All worked grid squares will be highlighted with golden rectangles
  - Grid square labels are displayed in the center of each square
  - Works with 4-character (e.g., FN20) and 6-character (e.g., FN20xa) grid squares
  - **NEW**: Use the grid precision dropdown to choose between 4-char or 6-char grids

**Technical Details**:
- Converts Maidenhead locator system to lat/lon coordinates
- Automatically extracts grid squares from QSO data
- Displays golden overlay with 20% opacity for visibility
- Grid labels shown with dark background for readability

### 2. High-Resolution Map Export (300 DPI)
- **Feature**: Export the map as a high-quality JPEG suitable for printing
- **How to use**:
  - Click the "Export Map (300 DPI)" button in the control panel
  - The map will be captured at 3300x2550 pixels (11"x8.5" at 300 DPI)
  - File downloads automatically as `rayfall-map-YYYY-MM-DD-300dpi.jpg`
  - Button shows "Exporting..." during the process

**Technical Details**:
- Uses html2canvas library for high-quality capture
- Temporarily resizes map to print dimensions for export
- JPEG quality set to 95% for optimal file size/quality balance
- Automatically restores original map size after export

### 3. Grid Precision Selector (NEW)
- **Feature**: Choose the precision of grid square display
- **How to use**:
  - Select "4-char grids" for broader grid squares (e.g., FN20)
  - Select "6-char grids" for more detailed subsquares (e.g., FN20xa)
  - Grid display updates automatically when changed

**Technical Details**:
- Dynamically adjusts grid square parsing based on selection
- Automatically redraws grid overlays when precision changes
- Default is 6-character for maximum detail

### 4. Toggle Pins Visibility (NEW)
- **Feature**: Hide or show QSO location pins
- **How to use**:
  - Uncheck "Show Pins" to hide all QSO markers
  - Useful for cleaner grid square visualization
  - Lines (if enabled) remain visible when pins are hidden

**Technical Details**:
- Pins are tracked but not added to map when hidden
- Instant toggle without reloading data
- All QSO data remains available for filtering

### 5. Toggle QTH Station Visibility (NEW)
- **Feature**: Hide or show your home station (⚡ icon)
- **How to use**:
  - Uncheck "Show QTH" to hide the operating station marker
  - Useful for focusing on worked locations only
  - Checked by default

**Technical Details**:
- Dynamically shows/hides QTH marker without reloading
- QTH position preserved from log data
- Marker z-index ensures it displays above other elements when visible

## Files Modified

### `templates/index.html`
1. Added html2canvas library for map export functionality
2. Added "Show Grid Squares" checkbox toggle
3. Added "Export Map (300 DPI)" button
4. **NEW**: Added grid precision selector (4-char vs 6-char)
5. **NEW**: Added "Show Pins" checkbox toggle
6. **NEW**: Added "Show QTH" checkbox toggle
7. Implemented `maidenheadToLatLon()` function for grid square conversion
8. Implemented `drawGridSquares()` function to render grid overlays
9. Implemented `toggleGridSquares()` function for checkbox control
10. **NEW**: Implemented `togglePins()` function to hide/show QSO markers
11. **NEW**: Implemented `toggleQTH()` function to hide/show station marker
12. **NEW**: Implemented `updateGridPrecision()` function to change grid detail level
13. Implemented `exportMap()` function for high-resolution export
14. Updated `plotQSOs()` to collect and display worked grid squares with precision control
15. Updated `plotQSOs()` to conditionally add pins based on toggle state
16. Updated `placeQTHMarkerFromLogs()` to respect QTH visibility toggle
17. Updated `clearMap()` to properly clean up grid square overlays
18. Added `workedGrids` Set and `gridSquares` array for state management

## Deployment

### Local Development
- Files updated in: `c:\Users\chris\OneDrive\Documents\Projects\Rayfall\`
- Ready for local testing

### Production Server (homedash.taile9e59a.ts.net)
- Backup created: `~/qrz-map/templates/index.html.backup`
- Updated file deployed to: `~/qrz-map/templates/index.html`
- Application automatically restarted
- New features live at: rayfall.me

## Testing Recommendations

1. **Grid Square Display**:
   - Load QSOs with various grid squares
   - Toggle the "Show Grid Squares" checkbox
   - Verify grid squares appear correctly positioned
   - **NEW**: Switch between 4-char and 6-char precision and verify grids update
   - Test with both 4-character and 6-character grid squares

2. **Map Export**:
   - Load some QSOs on the map
   - Click "Export Map (300 DPI)"
   - Verify the downloaded JPEG is high resolution (3300x2550 pixels)
   - Check that all map elements (markers, lines, grid squares) are included
   - Verify file is suitable for printing

3. **Pin Visibility Toggle (NEW)**:
   - Load QSOs and verify pins appear
   - Uncheck "Show Pins" and verify all markers disappear
   - Re-check to verify pins reappear
   - Test with grid squares enabled for cleaner visualization

4. **QTH Visibility Toggle (NEW)**:
   - Load QSOs and verify QTH (⚡) marker appears
   - Uncheck "Show QTH" and verify station marker disappears
   - Re-check to verify marker reappears
   - Test in combination with other toggles

5. **Grid Precision Selector (NEW)**:
   - Load QSOs with 6-character grid squares
   - Switch to "4-char grids" and verify squares consolidate
   - Switch back to "6-char grids" and verify detailed subsquares appear
   - Test export with different precision levels

## User Response

These features address the ham radio user's requests:
✅ Grid square (worked locator) map overlay
✅ High-resolution JPEG export at 300 DPI for printing
✅ **NEW**: Grid precision selector (4-char vs 6-char grids)
✅ **NEW**: Toggle to hide/show QSO pins
✅ **NEW**: Toggle to hide/show operating station

All features are now live and ready to use!
