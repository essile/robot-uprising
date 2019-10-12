#!/usr/bin/env python3
__author__ = 'Anton Vanhoucke'

import evdev
import ev3dev.auto as ev3
import threading

## Some helpers ##
def scale(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst.

    val: float or int
    src: tuple
    dst: tuple

    example: print(scale(99, (0.0, 99.0), (-1.0, +1.0)))
    """
    return (float(val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]

def scale_stick(value):
    return scale(value,(0,255),(-100,100))

def clamp(value, floor=-100, ceil=100):
    """
    Clamp the value within the floor and ceiling values.
    """
    return max(min(value, ceil), floor)

## Initializing ##
print("Finding ps3 controller...")
devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
for device in devices:
    if device.name == 'PLAYSTATION(R)3 Controller':
        ps3dev = device.fn

gamepad = evdev.InputDevice(ps3dev)

# Initialize globals
speed = 0
turn = 0
liftSpeed = 0
running = True

# Within this thread all the motor magic happens
class MotorThread(threading.Thread):
    def __init__(self):
        # Add more sensors and motors here if you need them
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.middle_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        threading.Thread.__init__(self)

    def run(self):
        print("Engine running!")
        # Change this function to suit your robot.
        # The code below is for driving a simple tank.
        while running:
            right_dc = clamp(-speed-turn)
            left_dc = clamp(-speed+turn)
            middle_dc = clamp(liftSpeed)
            self.right_motor.run_direct(duty_cycle_sp=right_dc)
            self.left_motor.run_direct(duty_cycle_sp=left_dc)
            self.middle_motor.run_direct(duty_cycle_sp=middle_dc)

        self.motor.stop()

# Multithreading magics
motor_thread = MotorThread()
motor_thread.setDaemon(True)
motor_thread.start()

class ControllerEvents:
    TYPE_ANALOG = 3
    TYPE_BUTTON = 1
    LEFT_X_AXIS = 0
    LEFT_Y_AXIS = 1
    RIGHT_X_AXIS = 2
    RIGHT_Y_AXIS = 5
    TRIANGLE = 300
    CIRCLE = 301
    CROSS = 302
    SQUARE = 303

for event in gamepad.read_loop():   #this loops infinitely
    if event.type == ControllerEvents.TYPE_ANALOG:             #One of the sticks is moved
        if event.code == ControllerEvents.LEFT_Y_AXIS:
            speed = scale_stick(event.value)
        else if event.code == ControllerEvents.LEFT_X_AXIS:
            turn = scale_stick(event.value)
        else if event.code == ControllerEvents.RIGHT_Y_AXIS:
            # nosta/laske kauhaa
            liftSpeed = scale_stick(event.value)
        else if event.code == ControllerEvents.RIGHT_X_AXIS:


    if event.type == ControllerEvents.TYPE_BUTTON and event.code == 302 and event.value == 1:
        print("X TYPE_BUTTON is pressed. Stopping.")
        running = False
        break
