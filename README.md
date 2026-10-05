# Visual Acuity Calculator — NiceGUI Windows App

This project provides a keyboard- and screen-reader-friendly NiceGUI interface around the supplied `visual_acuity_cli_tool.py` calculation.

The application calculates an equivalent **Snellen visual acuity fraction (`20/x`)** from an object's physical size and viewing distance.

## What it does

The GUI accepts:

- **Object size (millimeters)** — enter the physical target size in mm
- **Object size (inches)** — alternatively enter the physical target size in inches
- **Viewing distance (feet)** — the calculation uses feet, matching the original CLI
- **Round the Snellen denominator to the nearest whole number** — optional checkbox

The size can be entered in millimeters or inches. If the inches field contains a value, that value is used; otherwise the millimeter field is used. Inch measurements are converted to millimeters using **1 inch = 25.4 mm** before the visual-angle calculation.

The GUI and CLI use the same underlying `calculate_visual_acuity()` function. The GUI additionally accepts inches and converts them to millimeters before calling that function.

For the mathematical derivation, see [docs/index.md](docs/index.md) or the [documentation site](https://mrhunsaker.github.io/EnvironmentalObjectVisualAcuity/).

## Calculation and units

The calculation is based on the **exact visual angle** subtended by the object.

- Object size: **millimeters** internally
- Viewing distance: **feet**
- 1 foot = **304.8 mm**
- 1 inch = **25.4 mm**
- A standard 20/20 optotype subtends **5 arcminutes**
- The Snellen denominator is calculated as $x = 4\theta$, where $\theta$ is the subtended angle in arcminutes

The small-angle approximation used by the application is:

```
x ≈ 45.1148 × object size (mm) / distance (ft)
```

The application also calculates the exact trigonometric result and reports the subtended angle.

## Snellen rounding

By default, the GUI displays the exact Snellen denominator to one decimal place:

```
20/x.x
```

Selecting **Round the Snellen denominator to the nearest whole number** changes the displayed result to:

```
20/x
```

When whole-number rounding is selected, the small-angle approximation is omitted from the result details. The exact denominator remains available in the details.

This checkbox corresponds to the CLI's `-r` / `--round` option.

## Accessibility

The interface is designed for screen-reader and keyboard use:

- Native form controls with visible labels.
- Explicit input and required semantics.
- Keyboard-focusable Calculate and Clear buttons.
- Errors exposed through an `alert` live region.
- Results exposed through a polite live region.
- Focus moves to the result heading after a successful calculation.
- Focus returns to the first input when the form is cleared or invalid.
- No information is conveyed by color alone.

NiceGUI's desktop webview/browser engine also affects the final accessibility experience.

## Run from Python

Windows:

```bat
python -m pip install -r requirements.txt
python visual_acuity_app.py
```

The application starts a local NiceGUI server on:

```
http://127.0.0.1:8080
```

The application is configured with `native=True`, so the normal packaged application opens as its own desktop window rather than requiring the user to browse to the address manually.

## CLI usage

Calculate from an object size in millimeters:

```bash
python visual_acuity_cli_tool.py --size 18 --distance 10
```

Round the Snellen denominator:

```bash
python visual_acuity_cli_tool.py --size 18 --distance 10 --round
```

### CLI options

- `-s`, `--size`: Object size in millimeters.
- `-d`, `--distance`: Viewing distance in feet.
- `-r`, `--round`: Round the Snellen denominator to the nearest whole integer.

## Build a portable Windows EXE

On a Windows machine with Python installed:

```bat
build_windows.bat
```

The build script:

1. Installs the dependency ranges from `requirements.txt`.
2. Runs `nicegui-pack`.
3. Builds a one-file PyInstaller executable named `VisualAcuityCalculator.exe`.

The output is:

```
dist\\VisualAcuityCalculator.exe
```

The application code uses a NiceGUI page function:

```python
ui.run(page, ...)
```

rather than NiceGUI's global-script mode. This is important for current NiceGUI/PyInstaller packaging because script mode can attempt to execute the frozen EXE as Python source, producing errors such as:

```text
SyntaxError: source code string cannot contain null bytes
```

The packaged application also calls `multiprocessing.freeze_support()` and provides safe stdout/stderr streams for PyInstaller windowed mode.

## Create the Windows installer

The repository includes an Inno Setup script at [installer.iss](../installer.iss).

The tested installation workflow is:

1. Run `build_windows.bat`.
2. Confirm `dist\\VisualAcuityCalculator.exe` was created.
3. Open `installer.iss` in Inno Setup.
4. Compile the installer.
5. Run the resulting `installer\\VisualAcuityCalculatorSetup.exe`.
6. Launch the installed application from the Start Menu or desktop shortcut.

The Inno Setup installer is the project's normal distribution mechanism when a conventional Windows installation experience is desired.

PyInstaller itself only produces the executable; Inno Setup supplies the traditional Windows installer experience.

## Documentation site

This repository publishes its documentation to GitHub Pages with GitHub Actions. The site is built from [docs/index.md](docs/index.md) with MkDocs Material and deploys automatically whenever `main` is updated.

Documentation site:

https://mrhunsaker.github.io/EnvironmentalObjectVisualAcuity/

To build the documentation locally:

```bash
python -m pip install mkdocs-material
mkdocs serve
```

To create the production site:

```bash
mkdocs build
```

## Troubleshooting

### EXE starts but reports `source code string cannot contain null bytes`

This indicates that NiceGUI script mode is trying to parse the frozen EXE as Python source. Make sure the application uses the page-function form:

```python
def page():
    # build UI here
    ...

ui.run(page, reload=False, ...)
```

Do not move the UI widgets back to module/global scope.

### EXE reports logging or stdout/stderr errors

The application initializes safe stdout/stderr streams when PyInstaller provides `None` for them. If an old executable produces an error such as:

```text
Unable to configure formatter 'default'
AttributeError: 'NoneType' object has no attribute 'isatty'
```

rebuild the executable after updating the source.

For a clean rebuild, remove the old `build\\`, `dist\\`, and generated `.spec` file before running `build_windows.bat`.

### Browser/Vue warning

NiceGUI relies on a modern webview/browser engine. If the server starts but the interface reports that Vue failed to load or that import maps are unsupported, verify that the packaged application's webview/browser runtime is available and current. This is separate from the Python calculation itself.

## Files

- `visual_acuity_app.py` — NiceGUI desktop application
- `visual_acuity_cli_tool.py` — command-line calculation and shared calculation function
- `build_windows.bat` — Windows PyInstaller build script
- `installer.iss` — Inno Setup installer definition
- `requirements.txt` — NiceGUI and PyInstaller dependency ranges
- `docs/index.md` — mathematical and application documentation
- `.github/workflows/docs.yml` — GitHub Pages documentation deployment

## Notes

The application is a local web application hosted on `127.0.0.1`. The calculation itself does not require an internet connection.

The packaged Windows application is intended to run as a native desktop window. The Inno Setup package installs that executable and creates Start Menu and desktop shortcuts.
