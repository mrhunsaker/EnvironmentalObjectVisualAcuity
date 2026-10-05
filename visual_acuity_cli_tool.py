import argparse
import math


def calculate_visual_acuity(size_mm: float, distance_ft: float):
    """
    Calculates Snellen visual acuity denominator (20/x) given:
      - size_mm: Object size in millimeters
      - distance_ft: Viewing distance in feet
    """
    if size_mm <= 0 or distance_ft <= 0:
        raise ValueError("Size and distance must be positive numbers.")

    # Distance converted to mm (1 ft = 304.8 mm)
    distance_mm = distance_ft * 304.8

    # Exact subtended visual angle in radians
    angle_rad = 2.0 * math.atan(size_mm / (2.0 * distance_mm))

    # Angle in degrees and arcminutes
    angle_deg = math.degrees(angle_rad)
    angle_arcmin = angle_deg * 60.0

    # Snellen denominator x where 20/20 = 5 arcminutes
    x_exact = 4.0 * angle_arcmin

    # Small angle approximation
    x_approx = 45.1148 * (size_mm / distance_ft)

    return x_exact, x_approx, angle_arcmin


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Calculate Equivalent Snellen Visual Acuity "
            "(20/x) from object size and viewing distance."
        )
    )

    parser.add_argument(
        "-s",
        "--size",
        type=float,
        required=True,
        help="Object size in millimeters (mm)",
    )

    parser.add_argument(
        "-d",
        "--distance",
        type=float,
        required=True,
        help="Testing distance in feet (ft)",
    )

    parser.add_argument(
        "-r",
        "--round",
        action="store_true",
        help="Round the Snellen denominator to the nearest whole integer",
    )

    args = parser.parse_args()

    try:
        x_exact, x_approx, arcmin = calculate_visual_acuity(
            args.size,
            args.distance,
        )

        print("\n=== Visual Acuity Calculation Results ===")
        print(f"Input Object Size:   {args.size:.2f} mm")
        print(f"Input Distance:      {args.distance:.2f} ft")
        print(f"Subtended Angle:     {arcmin:.2f} arcminutes")
        print("-----------------------------------------")

        if args.round:
            print(f"Equivalent Acuity:   20/{round(x_exact)}")
        else:
            print(f"Equivalent Acuity:   20/{x_exact:.1f}")
            print(f"Approximation (45.12): 20/{x_approx:.1f}")

        print("=========================================\n")

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()