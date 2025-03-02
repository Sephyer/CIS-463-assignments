# main.py

import machine

from machine import Pin
import time

TRIG_PIN = 14
ECHO_PIN = 12
GREEN_PIN = 16
RED_PIN = 5

SOUND_VELOCITY = 0.034

trigger = Pin(TRIG_PIN, Pin.OUT, pull=None)
echo = Pin(ECHO_PIN, Pin.IN, pull=None)

green_lt = Pin(GREEN_PIN, Pin.OUT)
red_lt = Pin(RED_PIN, Pin.OUT)

def get_pulse_time():
    trigger.value(0)
    time.sleep_us(5)
    trigger.value(1)
    time.sleep_us(10)
    trigger.value(0)
#    return machine.time_pulse_us(echo, 1)
    try:
        pulse_time = machine.time_pulse_us(echo, 1)
        return pulse_time
    except OSSError as ex:
        if ex.args[0] == 110:
            raise OSError('Out of Range')
        raise ex

while True:
    pulse_time = get_pulse_time()
    distance_cm = (pulse_time/2) * SOUND_VELOCITY
    print('Distance ', distance_cm, ' (cm)')

    ### FIX-ME ###

    time.sleep(1)

