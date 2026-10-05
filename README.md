# Visual Acuity Calculator — NiceGUI Windows App

This project wraps the supplied `visual_acuity_cli_tool.py` in a simple, keyboard-friendly NiceGUI interface.

## What it does

The GUI accepts the same three CLI arguments:

- **Object size (millimeters)** — equivalent to `--size` / `-s`
- **Viewing distance (feet)** — equivalent to `--distance` / `-d`
- **Round the Snellen denominator** — equivalent to `--round` / `-r`

The calculation function is preserved from the supplied Python program.

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

## Build a portable EXE

On a Windows machine with Python installed:

```bat
build_windows.bat
```

The output is:

```text
dist\VisualAcuityCalculator.exe
```

This is a portable executable. PyInstaller does **not** itself create a traditional Windows installation wizard.

## Create a real Windows installer

For a normal "click Setup -> Next -> Install" experience, use Inno Setup:

1. Install Inno Setup.
2. Run `build_windows.bat`.
3. Open `installer.iss` in Inno Setup.
4. Compile it.
5. Give colleagues the resulting `installer\VisualAcuityCalculatorSetup.exe`.

They can then install it like a conventional Windows application.

## Troubleshooting PyInstaller

If you previously built the EXE and saw an error involving:

```text
Unable to configure formatter 'default'
AttributeError: 'NoneType' object has no attribute 'isatty'
```

rebuild the EXE using the supplied `visual_acuity_calculator.spec`. The GUI application now provides safe stdout/stderr streams for PyInstaller's windowed mode before NiceGUI/Uvicorn configures logging.

## Notes

Because NiceGUI is a local web application, the EXE starts a local web server. The application does not need an internet connection for the calculation itself.
