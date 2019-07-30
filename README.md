# Raspberry Pi GPIO through ROS

## Setup

This requires that the raspberry Pi has
[gpiozero remote gpio enabled](https://gpiozero.readthedocs.io/en/stable/remote_gpio.html).

## Usage

One node needs to be launched for each RPi that needs to be controlled. Ros parameters dictate what pins/topics are listened to.

### Set the host ip

The parameter `host` must be set to the ip of the raspberry running the remote gpio server.

### Publish the values of gpio pins (digital input pins)

For each pin where you want its value published onto an arbritrary topic, create a "pub" parameter. For this, the syntax is the following:

```xml
<param name="pub/<pin_name>" value="<pull_up>" />
```

 - The `pin_name` can be any pin-name-string accepted by gpiozero
 - The value of the gpio pin will be published to the internal topic `~/pin_name`
 - Set `pull_up` to true for pull up, or false for pull down mode.
 
### Set pins based on topic (digital output pins)

For any pin where you want to set its value based on a `std_msgs/Bool` topic, create a "sub" parameter. For this, the syntax is the following:

```xml
<param name="sub/<pin_name>" value="<topic_to_listen_on>" />
```

 - The `pin_name` can be any pin-name-string accepted by gpiozero
 - The topic can be from anywhere, but must be `std_msgs/Bool` type

### Example launch file

```xml
<launch>
  <node pkg="ltu_actor_rpi_gpio" type="run.py" name="rpi_gpio">
    <!-- the ip of the rpi -->
    <param name="host" value="192.168.0.10" />
    
    <!-- publish pin values on local topics. value here is the pull-up -->
    <param name="pub/GPIO4" value="false" />
    <param name="pub/GPIO3" value="true" />

    <!-- set pin 5 based on /gpio5 -->
    <param name="sub/5" value="/gpio5" />
  </node>
</launch>
```
