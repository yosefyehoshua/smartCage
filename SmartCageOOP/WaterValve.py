import Adafruit_MPR121.MPR121 as MPR121

from SmartCageOOP.LickDetectorError import LickDetectorError


class WaterValve:
    global cap
    cap = MPR121.MPR121()

    def __init__(self, PIN_WATER):
        self.GPIO.setup(PIN_WATER, GPIO.OUT, initial=GPIO.LOW)
        try:
            if not cap.begin():
                raise LickDetectorError("Error initializing MPR121 Lick Detector. Check wiring!")




