import multiprocessing
import os
import sys

# ---------------------------------------------------------
# PyInstaller / Windows compatibility
# ---------------------------------------------------------

if getattr(sys, "frozen", False):
    multiprocessing.freeze_support()

# PyInstaller windowed applications can have stdout/stderr
# set to None. NiceGUI/Uvicorn expects these objects to exist.
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
# UI references
#
# These are assigned when page() builds the interface.
# ---------------------------------------------------------

size_mm_input = None
size_in_input = None
distance_input = None
round_input = None

error_card = None
error_text = None

result_card = None
result_heading = None
result_text = None
details_text = None


# ---------------------------------------------------------
# Size input handling
# ---------------------------------------------------------

def get_size_mm():
    """
    Return (size_mm, entered_size, unit_label).

    If both fields are filled in, the inches field takes
    precedence, matching the original application behavior.
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

    return (
        float(size_mm_value),
        float(size_mm_value),
        "millimeters",
    )


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

        distance_value = distance_input.value

        if distance_value is None:
            raise ValueError(
                "Enter a viewing distance in feet."
            )

        distance = float(distance_value)

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
        # Format object size
        # -------------------------------------------------

        if unit == "inches":
            size_line = (
                f"Object size: {entered_size:.2f} inches "
                f"({size:.2f} millimeters). "
            )
        else:
            size_line = (
                f"Object size: {size:.2f} millimeters. "
            )

        # -------------------------------------------------
        # Update result
        # -------------------------------------------------

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

        # Move focus to the result heading for screen-reader
        # users.
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

def page():
    """
    Build the NiceGUI page.

    Keeping the UI inside a page function is important for
    PyInstaller compatibility with current NiceGUI versions.
    """

    global size_mm_input
    global size_in_input
    global distance_input
    global round_input

    global error_card
    global error_text

    global result_card
    global result_heading
    global result_text
    global details_text

    ui.page_title("Visual Acuity Calculator")

    with ui.column().classes(
        "w-full max-w-3xl mx-auto p-6 gap-5"
    ):

        # -------------------------------------------------
        # Main content
        # -------------------------------------------------

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

                # No "min" attribute is deliberately used.
                # NiceGUI can receive an empty string while
                # editing a number input, which can cause a
                # type comparison error inside the sanitizer.
                # Positive values are validated by calculate().

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
                    "Fill in the size in millimeters OR in inches; "
                    "whichever one is filled in is used."
                ).classes(
                    "text-sm text-gray-600"
                )

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

                # -------------------------------------------------
                # Original rounding checkbox
                # -------------------------------------------------

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
The calculation uses the exact visual angle subtended
by the object.

A standard 20/20 optotype subtends 5 arcminutes.

Sizes entered in inches are converted to millimeters
(1 inch = 25.4 mm) before the calculation.

The small-angle approximation is:

**x ≈ 45.1148 × object size (mm) / distance (ft)**
"""
                )


# ---------------------------------------------------------
# Native desktop application
# ---------------------------------------------------------

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        page,
        title="Visual Acuity Calculator",
        host="127.0.0.1",
        port=8080,
        reload=False,
        native=True,
        window_size=(1000, 750),
    )