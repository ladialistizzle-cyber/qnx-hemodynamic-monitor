import time
import random
import rpi_gpio as GPIO
from datetime import datetime

# LA Hacks 2026 — QNX Hemodynamic Monitoring Demonstration
# Synthetic data and illustrative threshold rules only.
# Not a validated clinical prediction model or medical device.

PINS = {
    "RED1": 16, "YELLOW1": 20, "GREEN1": 21,
    "RED2": 26, "YELLOW2": 19, "GREEN2": 13
}

def lights_off():
    for pin in PINS.values():
        GPIO.output(pin, GPIO.LOW)

def show_lights(status, falling):
    lights_off()

    # Hemodynamic Status: overall alert state
    color = {
        "STABLE": "GREEN1",
        "CAUTION": "YELLOW1",
        "HIGH": "RED1"
    }[status]
    GPIO.output(PINS[color], GPIO.HIGH)

    # MAP Trend: independent change between consecutive readings
    GPIO.output(
        PINS["YELLOW2"] if falling else PINS["GREEN2"],
        GPIO.HIGH
    )


def generate_vitals(step):
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
    falling = (
        previous_map is not None
        and previous_map - map_value >= 1.5
    )

    if map_value < 65:
        reasons.append("MAP below illustrative 65 mmHg threshold")
    if falling:
        reasons.append("MAP trending downward")
    if hr > 100:
        reasons.append("Heart rate elevated")

    if map_value < 60:
        status = "HIGH"
    elif reasons:
        status = "CAUTION"
    else:
        status = "STABLE"

    return status, reasons, falling

def main():
    print("=" * 65)
    print("QNX HEMODYNAMIC MONITOR | LA HACKS 2026")
    print("Synthetic patient data | Demonstration only")
    print("Left LED: risk status | Right LED: MAP trend")
    print("=" * 65)

    previous_map = None

    for step in range(30):
        hr, map_value = generate_vitals(step)
        status, reasons, falling = assess_status(
            hr, map_value, previous_map
        )

        show_lights(status, falling)

        timestamp = datetime.now().strftime("%H:%M:%S")
        print(
            f"[{timestamp}] HR: {hr:3d} bpm | "
            f"MAP: {map_value:5.1f} mmHg | Risk: {status}",
            flush=True
        )

        if reasons:
            print("  Explanation: " + "; ".join(reasons), flush=True)

        previous_map = map_value
        time.sleep(1)

    print("\nSimulation complete.")

if __name__ == "__main__":
    try:
        for pin in PINS.values():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
        main()
    finally:
        lights_off()
        print("LEDs off.")
