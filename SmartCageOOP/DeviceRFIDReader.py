import RPi.GPIO as GPIO
import time

import Serial as Serial
import serial


class DeviceRFIDReader:
    """
    Represents the RFID reader device
    """

    global USB_PORT
    USB_PORT = "/dev/ttyUSB1"
    serial_dev = bytes

    def __init__(self):
        self.serial_dev = serial.Serial(USB_PORT, baudrate=9600)
        self.currentRFID = ''

    def read(self): # todo check if condition works, if not put the old working code here
        self.currentRFID = ''
        RFID_lastChar = self.serial_dev.read()
        while (RFID_lastChar != '\r'):
            if (RFID_lastChar.isalpha() or RFID_lastChar.isdigit()):
                self.currentRFID = self.currentRFID + RFID_lastChar
            RFID_lastChar = self.serial_dev.read()


    def getCurrentRFID(self):
        return self.currentRFID
