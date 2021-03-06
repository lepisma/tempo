# The module to interact with arduino baord for inside temperature

import serial
import time

def inside_temperature(port):
    """
    Requests arduino to provide current temperature
    """

    ser = serial.Serial(port, 9600)
    try:
        time.sleep(4)
        ser.write('A')

        get = ser.readline()
        if get == "ok\r\n":
            rec = ser.readline()
            temp = float(rec.split("\r")[0])
        else:
            raise Exception()
    except Exception:
        return -1

    return temp
