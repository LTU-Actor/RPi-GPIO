#!/usr/bin/env python

import rospy
from gpiozero import Button, LED
from gpiozero.pins.pigpio import PiGPIOFactory
from std_srvs.srv import Empty
from std_msgs.msg import Bool
from signal import pause
from functools import partial

# Kind of like a JS style object that you can just assign stuff to
class StorageObject: pass

def pub_pin_f(pub, data):
    rospy.logerr("GOT: ")
    rospy.logerr(data)
    pub.publish(data)

rospy.init_node('rpi_estop_loop')
hostpi = rospy.get_param('~host', None)
bounce_time = rospy.get_param('~bounce_time', 0.01)

factory = None
if hostpi is not None:
    factory = PiGPIOFactory(host=hostpi)

pub_pins = {}
pub_pins_params = rospy.get_param('~pub')
for pin, pull_up in pub_pins_params.iteritems():
    o = StorageObject()
    o.button = Button(pin, pin_factory=factory, pull_up=bool(pull_up), bounce_time=bounce_time)
    o.pub = rospy.Publisher('~pub/' + pin, Bool, queue_size=10)
    o.button.when_pressed = partial(pub_pin_f, o.pub, True)
    o.button.when_released = partial(pub_pin_f, o.pub, False)
    pub_pins[pin] = o

pause()
