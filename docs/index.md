# Visual Acuity Calculation and Application Reference

This document describes the calculation implemented by `visual_acuity_cli_tool.py` and the NiceGUI Windows application.

---

## 1. Purpose

The application calculates an equivalent **Snellen visual acuity** value in the form:

```
20/x
```

It uses the physical size of an object and the distance between the observer and the object to determine the object's visual angle.

The implementation uses **feet for viewing distance** and **millimeters for the internal object-size calculation**, matching the original CLI implementation.

---

## 2. Inputs and Units

### Object size

The user may provide object size in either:

- millimeters (mm), or
- inches (in)

For an inch measurement:

```
S_mm = S_in × 25.4
```

where S is object size.

The GUI has separate millimeter and inch fields. If the inches field contains a value, the inches value is used; otherwise the millimeter value is used.

### Viewing distance

Viewing distance is entered in **feet (ft)**.

The calculation converts feet to millimeters:

```
D_mm = D_ft × 304.8
```

because:

```
1 foot = 304.8 millimeters
```

---

## 3. Exact Visual-Angle Calculation

Let:

- S = object size in millimeters
- D = viewing distance in feet
- D_mm = viewing distance in millimeters

First:

```
D_mm = D × 304.8
```

The exact visual angle in radians is:

```
θ_rad = 2 × atan(S / (2 × D_mm))
```

Substituting the feet-to-millimeter conversion:

```
θ_rad = 2 × atan(S / (609.6 × D))
```

The angle is converted to arcminutes:

```
θ_arcmin = θ_rad × 180 × 60 / π
```

The implementation uses **5 arcminutes as the standard 20/20 visual angle**. Therefore the Snellen denominator is:

```
x = 20 × (θ_arcmin / 5)
x = 4 × θ_arcmin
```

The resulting acuity is:

```
20/x
```

---

## 4. Small-Angle Approximation

For small visual angles:

```
atan(z) ≈ z
```

This produces the approximation implemented by the CLI:

```
x ≈ 45.1148 × S_mm / D_ft
```

Therefore:

```
Snellen ≈ 20 / (45.1148 × S_mm / D_ft)
```

The application calculates both the exact denominator and this approximation.

The approximation is displayed when the user leaves the whole-number rounding checkbox unchecked.

---

## 5. Snellen Rounding

The GUI provides a checkbox labeled:

**Round the Snellen denominator to the nearest whole number**

When unchecked, the primary result is formatted to one decimal place:

```
20/x.x
```

For example:

```
20/31.7
```

When checked, the exact denominator is rounded to the nearest integer:

```
20/32
```

The GUI intentionally does not expose a general decimal-place selector. The checkbox preserves the original application's simple whole-number Snellen option.

When whole-number rounding is selected, the small-angle approximation is not displayed in the result details.

The CLI provides the equivalent behavior through:

```bash
python visual_acuity_cli_tool.py --size 18 --distance 10 --round
```

---

## 6. Quick Reference

| Quantity | Unit / Formula |
|---|---|
| Object size input | mm or inches |
| Internal object size | mm |
| Viewing distance | ft |
| Feet conversion | 1 ft = 304.8 mm |
| Inch conversion | 1 in = 25.4 mm |
| 20/20 reference | 5 arcminutes |
| Exact Snellen denominator | x = 4 × θ_arcmin |
| Approximate denominator | x ≈ 45.1148 S_mm / D_ft |
| Normal GUI display | 20/x.x |
| Rounded GUI display | 20/x |

---

## 7. CLI Usage

### Millimeters

```bash
python visual_acuity_cli_tool.py --size 18 --distance 10
```

### Inches

```bash
python visual_acuity_cli_tool.py --size 0.71 --inches --distance 10
```

### Whole-number Snellen denominator

```bash
python visual_acuity_cli_tool.py --size 18 --distance 10 --round
```

Available options:

- `-s`, `--size`: Object size. Millimeters by default.
- `-i`, `--inches`: Interpret the size as inches.
- `-d`, `--distance`: Viewing distance in feet.
- `-r`, `--round`: Round the Snellen denominator to the nearest integer.

---

## 8. GUI Application

The GUI is implemented in `visual_acuity_app.py`.

It provides:

1. Object size in millimeters
2. Object size in inches
3. Viewing distance in feet
4. Optional whole-number Snellen rounding
5. Calculate and Clear controls
6. Exact visual angle and denominator details
7. Formula reference information

The application is configured as a native NiceGUI desktop application:

```python
ui.run(
    page,
    title="Visual Acuity Calculator",
    host="127.0.0.1",
    port=8080,
    reload=False,
    native=True,
    window_size=(1000, 750),
)
```

The important packaging detail is that the interface is constructed inside `page()` and passed to `ui.run(page, ...)`. This avoids NiceGUI script-mode behavior that can attempt to execute the PyInstaller EXE as Python source.

---

## 9. Windows Packaging

The Windows build is performed by:

```bat
build_windows.bat
```

The script installs the dependency ranges from `requirements.txt` and invokes:

```text
nicegui-pack --onefile --name "VisualAcuityCalculator" visual_acuity_app.py
```

The resulting portable executable is:

```
dist\VisualAcuityCalculator.exe
```

The packaged application includes the PyInstaller compatibility handling needed for Windows multiprocessing and windowed execution.

---

## 10. Inno Setup Installer

The repository includes `installer.iss` for Inno Setup.

The installer packages:

```
dist\VisualAcuityCalculator.exe
```

and creates:

- a Start Menu shortcut
- a desktop shortcut
- an optional post-install launch

The installer is the recommended distribution format for users who want a conventional Windows installation rather than a standalone EXE.

The current installer workflow has been verified to work.

---

## 11. Accessibility

The GUI includes accessibility features such as:

- labeled form controls
- keyboard-accessible buttons
- explicit ARIA semantics
- an assertive error live region
- a polite result live region
- focus movement to the result heading after calculation
- focus return to the first input after an error or clear operation

The final screen-reader experience also depends on the webview/browser engine used by the desktop application.

---

## 12. PyInstaller / NiceGUI Packaging Note

Current NiceGUI versions support application/page functions passed to `ui.run()`.

For this project, the page-function architecture is intentional:

```python
def page():
    # Construct the UI here.
    ...

ui.run(page, ...)
```

Do not move the UI construction back to module/global scope when building the Windows EXE.

The previous failure mode was:

```text
SyntaxError: source code string cannot contain null bytes
```

with a traceback through NiceGUI's script execution and `runpy.run_path(sys.argv[0])`.

A frozen PyInstaller executable is binary data, not Python source. The page-function architecture prevents NiceGUI from treating the EXE itself as the application source file.

---

## 13. Formula Verification

The implementation in `visual_acuity_cli_tool.py` was checked against the equations above:

1. Feet are converted using 304.8 mm/ft.
2. The exact angle uses the symmetric `2 × atan(S / (2D))` formula.
3. Radians are converted to degrees and then arcminutes.
4. The Snellen denominator is four times the angle in arcminutes.
5. The approximation uses the same 45.1148 coefficient documented here.
6. The GUI calls the same `calculate_visual_acuity()` function as the CLI.

This keeps the GUI and CLI calculation paths consistent.
