
import sys
import time
import colorsys

import RPi.GPIO as GPIO

# Left
# red = 17
# green = 18
# blue = 27

# Middle
# red = 13
# green = 19
# blue = 26

# Right
# red = 16
# green = 20
# blue = 21
import itertools

PINS = (
    (17, 18, 27),
    (13, 19, 26),
    (16, 20, 21)
)

LED_LEFT = 0
LED_MIDDLE = 1
LED_RIGHT = 2

def set_led(led, r, g, b):
    pins = PINS[led]
    GPIO.output(pins[0], r)
    GPIO.output(pins[1], g)
    GPIO.output(pins[2], b)


def clear_led():
    for led in [LED_LEFT, LED_MIDDLE, LED_RIGHT]:
        set_led(led, 0, 0, 0)


def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    for pin in itertools.chain(PINS):
        GPIO.setup(pin, GPIO.OUT)


def cleanup():
    GPIO.cleanup()

def colorloop():

    RED = GPIO.PWM(red, 100)
    GREEN = GPIO.PWM(green, 100)
    BLUE = GPIO.PWM(blue, 100)

    RED.start(0)
    GREEN.start(0)
    BLUE.start(0)

    count = 0
    value = lambda x: max(min(x * 100, 100), 0)
    while True:
        inc = float(count % 100) / 100.
        r, g, b = [value(x) for x in colorsys.hsv_to_rgb(inc, 1, 1)]
        RED.ChangeDutyCycle(r)
        GREEN.ChangeDutyCycle(g)
        BLUE.ChangeDutyCycle(b)
        time.sleep(.1)
        count += 1


def debug():
    while True:
        for r, g, b in [(100, 0, 0), (0, 100, 0), (0, 0, 100)]:
            for led in [LED_LEFT, LED_MIDDLE, LED_RIGHT]:
                set_led(led, r, g, b)
            time.sleep(1)


def main(args):
    clear_led()
    time.sleep(1)

    debug()

if __name__ == "__main__":

    init()

    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        pass

    cleanup()