import os
import sys

# ---------------------------------------------------------
# PyInstaller / Windows compatibility
# ---------------------------------------------------------
#
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
# Calculation
# ---------------------------------------------------------

def calculate():
    """
    Validate the inputs, perform the calculation, and
    announce the result to screen-reader users.
    """

    try:
        size = float(size_input.value)
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

        result_text.text = (
            f"Equivalent visual acuity: {acuity}"
        )

        details_text.text = (
            f"Object size: {size:.2f} millimeters. "
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
        size_input.run_method("focus")


# ---------------------------------------------------------
# Clear
# ---------------------------------------------------------

def clear_form():
    """
    Clear all inputs and results.
    """

    size_input.value = ""
    distance_input.value = ""
    round_input.value = False

    result_text.text = ""
    details_text.text = ""
    error_text.text = ""

    result_card.classes(add="hidden")
    error_card.classes(add="hidden")

    size_input.run_method("focus")


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
        ).classes(
            "text-base"
        )

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

            size_input = ui.number(
                label="Object size (millimeters)",
                placeholder="Example: 18",
            ).props(
                'type="number" '
                'inputmode="decimal" '
                'step="any" '
                'min="0" '
                'aria-required="true" '
                'autocomplete="off"'
            ).classes(
                "w-full"
            )

            distance_input = ui.number(
                label="Viewing distance (feet)",
                placeholder="Example: 10",
            ).props(
                'type="number" '
                'inputmode="decimal" '
                'step="any" '
                'min="0" '
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

                A standard 20/20 optotype subtends 5 arcminutes.

                The small-angle approximation is:

                **x ≈ 45.1225 × object size (mm) / distance (ft)**
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
ui.run(
    title="Visual Acuity Calculator",
    host="127.0.0.1",
    port=8080,
    reload=False,
    native=True,
    window_size=(1000, 750),
)