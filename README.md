# Visual Acuity Calculator — NiceGUI Windows App

This project wraps the supplied `visual_acuity_cli_tool.py` in a simple, keyboard-friendly NiceGUI interface.

## What it does

The GUI accepts the same inputs as the CLI tool:

- **Object size (millimeters)** — equivalent to `--size` / `-s`
- **Object size (inches)** — equivalent to `--size` with `--inches` / `-i`
- **Viewing distance (feet)** — equivalent to `--distance` / `-d`
- **Round the Snellen denominator** — equivalent to `--round` / `-r`

Fill in the size in **millimeters or inches** — whichever field is filled in is used. If both are filled in, millimeters win. Sizes entered in inches are converted to millimeters (1 inch = 25.4 mm) before the calculation.

The calculation function is preserved from the supplied Python program. For the full mathematical derivation, see the [documentation site](https://mrhunsaker.github.io/EnvironmentalObjectVisualAcuity/) or [docs/index.md](docs/index.md).

## Accessibility

The interface is designed for screen-reader and keyboard use:

- Native form controls with visible labels.
- Explicit required/input semantics.
- Keyboard-focusable Calculate and Clear buttons.
- Errors exposed through an `alert` live region.
- Results exposed through a polite live region.
- Focus moves to the result heading after a successful calculation.
- Focus returns to the first input when the form is cleared or invalid.
- No information is conveyed by color alone.

NiceGUI runs the interface in a browser, so the accessibility experience also depends on the browser and the user's screen reader.

## Run from Python

Windows:

```bat
python -m pip install -r requirements.txt
python visual_acuity_app.py
```

The app listens only on `127.0.0.1` and automatically opens your default browser at:

`http://127.0.0.1:8080`

## CLI usage

```bash
python visual_acuity_cli_tool.py --size 18 --distance 10
```

Options:

- `-s`, `--size`: Object size in millimeters (mm), or in inches when `-i` is given
- `-i`, `--inches`: Interpret `--size` as inches instead of millimeters
- `-d`, `--distance`: Distance to object in feet (ft)
- `-r`, `--round`: (Optional) Round the visual acuity denominator to the nearest integer

## Build a portable EXE

On a Windows machine with Python installed:

```bat
build_windows.bat
```

The build uses `nicegui-pack` (bundled with NiceGUI), which wraps PyInstaller and automatically includes NiceGUI's static assets needed for a working desktop app.

The output is:

```text
dist\VisualAcuityCalculator.exe
```

This is a portable executable. PyInstaller does **not** itself create a traditional Windows installation wizard.

## Create a real Windows installer

For a normal "click Setup -&gt; Next -&gt; Install" experience, use Inno Setup:

1. Install Inno Setup.
2. Run `build_windows.bat`.
3. Open `installer.iss` in Inno Setup.
4. Compile it.
5. Give colleagues the resulting `installer\VisualAcuityCalculatorSetup.exe`.

They can then install it like a conventional Windows application.

## Documentation site

This repository publishes its documentation to GitHub Pages with GitHub Actions. The site is built from [docs/index.md](docs/index.md) with MkDocs and deploys automatically whenever `main` is updated:

`https://mrhunsaker.github.io/EnvironmentalObjectVisualAcuity/`

To build the site locally:

```bash
python -m pip install mkdocs-material
mkdocs serve
```

## Troubleshooting PyInstaller

If the built EXE shows an "Internal Service Error" window, make sure you rebuilt after the latest changes — the app now calls `multiprocessing.freeze_support()` for frozen executables and the build uses `nicegui-pack` so that NiceGUI's static files are bundled correctly.

If you previously built the EXE and saw an error involving:

```text
Unable to configure formatter 'default'
AttributeError: 'NoneType' object has no attribute 'isatty'
```

rebuild the EXE from scratch (delete the `build/`, `dist/`, and any old `.spec` first). The GUI application now provides safe stdout/stderr streams for PyInstaller's windowed mode before NiceGUI/Uvicorn configures logging.

## Notes

Because NiceGUI is a local web application, the EXE starts a local web server. The application does not need an internet connection for the calculation itself.