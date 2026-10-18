import time
import random
from datetime import datetime

# LA Hacks 2026 - QNX Hemodynamic Monitoring Demo
# Synthetic data and illustrative rules only.
# Not a validated clinical prediction model.

def generate_vitals(step):
    # Simulate hypotension followed by recovery
    if step < 10:
        map_value = 85 - step * 1.5
    elif step < 20:
        map_value = 70 - (step - 10) * 1.8
    else:
        map_value = 54 + (step - 20) * 2.5

    map_value += random.uniform(-1, 1)
    hr = 75 + max(0, 85 - map_value) * 0.7
    hr += random.uniform(-2, 2)

    return round(hr), round(map_value, 1)


def assess_status(hr, map_value, previous_map):
    reasons = []

    if map_value < 65:
        reasons.append("MAP below illustrative 65 mmHg threshold")

    if previous_map is not None:
        if previous_map - map_value >= 1.5:
            reasons.append("MAP trending downward")

    if hr > 100:
        reasons.append("Heart rate elevated")

    if map_value < 60:
        status = "HIGH"
    elif reasons:
        status = "CAUTION"
    else:
        status = "STABLE"

    return status, reasons


def main():
    print("=" * 65)
    print("QNX HEMODYNAMIC MONITOR | LA HACKS 2026")
    print("Synthetic patient data | Demonstration only")
    print("=" * 65)

    previous_map = None

    for step in range(30):
        hr, map_value = generate_vitals(step)
        status, reasons = assess_status(
            hr, map_value, previous_map
        )

        timestamp = datetime.now().strftime("%H:%M:%S")

        print(
            f"[{timestamp}] "
            f"HR: {hr:3d} bpm | "
            f"MAP: {map_value:5.1f} mmHg | "
            f"Risk: {status}"
        )

        if reasons:
            print("  Explanation: " + "; ".join(reasons))

        previous_map = map_value
        time.sleep(1)

    print("\nSimulation complete.")


if __name__ == "__main__":
    main()
