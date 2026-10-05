import multiprocessing
import os
import sys

# ---------------------------------------------------------
# PyInstaller / Windows compatibility
# ---------------------------------------------------------
#
# A frozen (PyInstaller) executable on Windows must call
# freeze_support() before anything spawns a child process,
# otherwise every child re-runs the entry script and the
# server never comes up (shows "Internal Service Error").
#
if getattr(sys, "frozen", False):
    multiprocessing.freeze_support()

# When PyInstaller builds a windowed application with
# console=False, stdout/stderr can be None.
#
# Uvicorn/NiceGUI expects these objects to exist when
# configuring its logging system.
#
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w", encoding="utf-8")

if sys.stderr is None:
    sys.stderr = open(os.devnull, "w", encoding="utf-8")


from nicegui import ui

from visual_acuity_cli_tool import calculate_visual_acuity


# ---------------------------------------------------------
# Constants
# ---------------------------------------------------------

MM_PER_INCH = 25.4


# ---------------------------------------------------------
# Size input handling
# ---------------------------------------------------------

def get_size_mm():
    """
    Return (size_mm, entered_size, unit_label) based on
    whichever size field is filled in.

    If both fields are filled in, the millimeter field is
    used; the inches field is only consulted when the
    millimeters field is empty (matching the CLI behavior
    of passing -i only when the size is given in inches).
    """

    size_mm_value = size_mm_input.value
    size_in_value = size_in_input.value

    if size_mm_value is None and size_in_value is None:
        raise ValueError(
            "Enter the object size in millimeters or in inches."
        )

    if size_in_value is not None:
        return (
            float(size_in_value) * MM_PER_INCH,
            float(size_in_value),
            "inches",
        )

    return float(size_mm_value), float(size_mm_value), "millimeters"


# ---------------------------------------------------------
# Calculation
# ---------------------------------------------------------

def calculate():
    """
    Validate the inputs, perform the calculation, and
    announce the result to screen-reader users.
    """

    try:
        size, entered_size, unit = get_size_mm()
        distance = float(distance_input.value)

        if size <= 0:
            raise ValueError(
                "Object size must be greater than zero."
            )

        if distance <= 0:
            raise ValueError(
                "Viewing distance must be greater than zero."
            )

        x_exact, x_approx, arcmin = calculate_visual_acuity(
            size,
            distance,
        )

        # -------------------------------------------------
        # Format result
        # -------------------------------------------------

        if round_input.value:
            acuity = f"20/{round(x_exact)}"

            approximation = (
                "The small-angle approximation is not displayed "
                "when whole-number rounding is selected."
            )

        else:
            acuity = f"20/{x_exact:.1f}"

            approximation = (
                f"Small-angle approximation: 20/{x_approx:.1f}"
            )

        # -------------------------------------------------
        # Update result
        # -------------------------------------------------

        size_line = (
            f"Object size: {entered_size:.2f} inches "
            f"({size:.2f} millimeters). "
            if unit == "inches"
            else f"Object size: {size:.2f} millimeters. "
        )

        result_text.text = (
            f"Equivalent visual acuity: {acuity}"
        )

        details_text.text = (
            f"{size_line}"
            f"Viewing distance: {distance:.2f} feet. "
            f"Subtended angle: {arcmin:.2f} arcminutes. "
            f"Exact Snellen denominator: {x_exact:.4f}. "
            f"{approximation}"
        )

        error_text.text = ""

        result_card.classes(remove="hidden")
        error_card.classes(add="hidden")

        # Move focus to the result heading.
        #
        # This is important for screen-reader users because
        # they receive the result immediately after pressing
        # Calculate.
        result_heading.run_method("focus")

    except (TypeError, ValueError) as error:
        result_text.text = ""
        details_text.text = ""

        error_text.text = str(error)

        error_card.classes(remove="hidden")
        result_card.classes(add="hidden")

        # Return focus to the first input.
        size_mm_input.run_method("focus")


# ---------------------------------------------------------
# Clear
# ---------------------------------------------------------

def clear_form():
    """
    Clear all inputs and results.
    """

    size_mm_input.value = None
    size_in_input.value = None
    distance_input.value = None
    round_input.value = False

    result_text.text = ""
    details_text.text = ""
    error_text.text = ""

    result_card.classes(add="hidden")
    error_card.classes(add="hidden")

    size_mm_input.run_method("focus")


# ---------------------------------------------------------
# Page
# ---------------------------------------------------------

ui.page_title("Visual Acuity Calculator")


with ui.column().classes(
    "w-full max-w-3xl mx-auto p-6 gap-5"
):

    # -----------------------------------------------------
    # Main content
    # -----------------------------------------------------

    with ui.element("main").props(
        'role="main" aria-labelledby="page-title"'
    ).classes("w-full"):

        ui.label(
            "Visual Acuity Calculator"
        ).props(
            'id="page-title"'
        ).classes(
            "text-3xl font-bold"
        )

        ui.label(
            "Calculate equivalent Snellen visual acuity "
            "(20/x) from object size and viewing distance."
        ).classes("text-base")

        # -------------------------------------------------
        # Inputs
        # -------------------------------------------------

        with ui.element("form").props(
            'aria-labelledby="input-heading"'
        ).classes("w-full"):

            ui.label(
                "Calculation inputs"
            ).props(
                'id="input-heading"'
            ).classes(
                "text-xl font-semibold mt-4"
            )

            # Note: the "min" attribute is deliberately NOT
            # set on these inputs. NiceGUI's number sanitize
            # handler compares incoming values against min
            # with max(), and the browser can send an empty
            # string, which raises:
            # TypeError: '>' not supported between instances
            # of 'str' and 'float'
            # Positive values are validated in calculate().

            size_mm_input = ui.number(
                label="Object size (millimeters)",
                placeholder="Example: 18",
            ).props(
                'inputmode="decimal" '
                'step="any" '
                'aria-required="false" '
                'autocomplete="off"'
            ).classes(
                "w-full"
            )

            size_in_input = ui.number(
                label="Object size (inches)",
                placeholder="Example: 0.71",
            ).props(
                'inputmode="decimal" '
                'step="any" '
                'aria-required="false" '
                'autocomplete="off"'
            ).classes(
                "w-full"
            )

            ui.label(
                "Fill in the size in millimeters OR in "
                "inches; whichever one is filled in is used."
            ).classes("text-sm text-gray-600")

            distance_input = ui.number(
                label="Viewing distance (feet)",
                placeholder="Example: 10",
            ).props(
                'inputmode="decimal" '
                'step="any" '
                'aria-required="true" '
                'autocomplete="off"'
            ).classes(
                "w-full"
            )

            round_input = ui.checkbox(
                "Round the Snellen denominator "
                "to the nearest whole number"
            )

            # -------------------------------------------------
            # Buttons
            # -------------------------------------------------

            with ui.row().classes("gap-3"):

                ui.button(
                    "Calculate",
                    on_click=calculate,
                    icon="calculate",
                ).props(
                    'type="button"'
                )

                ui.button(
                    "Clear",
                    on_click=clear_form,
                    icon="clear",
                ).props(
                    'type="button" flat'
                )

        # -------------------------------------------------
        # Error
        # -------------------------------------------------

        with ui.card().props(
            'role="alert" aria-live="assertive"'
        ).classes(
            "w-full hidden"
        ) as error_card:

            error_text = ui.label("")

        # -------------------------------------------------
        # Result
        # -------------------------------------------------

        with ui.card().props(
            'role="region" '
            'aria-live="polite" '
            'aria-labelledby="result-heading"'
        ).classes(
            "w-full hidden"
        ) as result_card:

            result_heading = ui.label(
                "Calculation result"
            ).props(
                'id="result-heading" tabindex="-1"'
            ).classes(
                "text-xl font-semibold"
            )

            result_text = ui.label("")

            details_text = ui.label("")

        # -------------------------------------------------
        # Formula information
        # -------------------------------------------------

        with ui.expansion(
            "Formula reference",
            icon="help_outline",
        ).classes(
            "w-full"
        ):

            ui.markdown(
                """
                The calculation uses the exact visual angle
                subtended by the object.

                A standard 20/20 optotype subtends 5
                arcminutes.

                Sizes entered in inches are converted to
                millimeters (1 inch = 25.4 mm) before the
                calculation.

                The small-angle approximation is:

                **x ≈ 45.1148 × object size (mm) / distance (ft)**
                """
            )


# ---------------------------------------------------------
# Native desktop application
# ---------------------------------------------------------
#
# native=True tells NiceGUI to use a desktop webview
# instead of opening an external browser.
#
# The application should therefore appear as its own
# Windows desktop window.
#
# The __mp_main__ guard matches the process name that
# multiprocessing children use on Windows, so frozen
# executables and spawned workers both run the UI.
#
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title="Visual Acuity Calculator",
        host="127.0.0.1",
        port=8989,
        reload=False,
        native=False,  # desktop window from source, browser when packaged
        window_size=(1000, 750),
    )