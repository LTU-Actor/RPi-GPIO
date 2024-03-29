#!/usr/bin/env python3

import rospy

import os
os.environ['GPIOZERO_PIN_FACTORY'] = os.environ.get('GPIOZERO_PIN_FACTORY', 'mock')

from gpiozero import Button, LED
from gpiozero.pins.pigpio import PiGPIOFactory
from std_srvs.srv import Empty
from std_msgs.msg import Bool
from signal import pause
from functools import partial

# Kind of like a JS style object that you can just assign stuff to
class StorageObject: pass


# CORE

rospy.init_node('rpi_estop_loop')
hostpi = rospy.get_param('~host', None)
bounce_time = rospy.get_param('~bounce_time', 0.01)

factory = None
if hostpi is not None:
    factory = PiGPIOFactory(host=hostpi)


# PIN PUBLISHING

def pub_pin_f(pub, data):
    rospy.logerr("GOT: ")
    rospy.logerr(data)
    pub.publish(data)

pub_pins = {}
pub_pins_params = rospy.get_param('~pub', None)
if pub_pins_params is not None:
    for pin, pull_up in pub_pins_params.items():
        o = StorageObject()
        o.button = Button(pin, pin_factory=factory, pull_up=bool(pull_up), bounce_time=bounce_time)
        o.pub = rospy.Publisher('~pub/' + pin, Bool, queue_size=10)
        o.button.when_pressed = partial(pub_pin_f, o.pub, True)
        o.button.when_released = partial(pub_pin_f, o.pub, False)
        pub_pins[pin] = o


# PIN SUBSCRIBING

def sub_pin_f(led, data):
    if data.data:
        led.on()
    else:
        led.off()

sub_pins = {}
sub_pins_params = rospy.get_param('~sub', None)
if sub_pins_params is not None:
    for pin, topic in sub_pins_params.items():
        o = StorageObject()
        o.led = LED(int(pin), pin_factory=factory)
        o.sub = rospy.Subscriber(topic, Bool, partial(sub_pin_f, o.led))
        sub_pins[pin] = o

pause()
