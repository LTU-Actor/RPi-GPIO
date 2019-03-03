# Raspberry Pi GPIO through ROS

### Example launch file

```xml
<launch>
  <node pkg="ltu_actor_rpi_gpio" type="run.py" name="rpi_gpio">
    <!-- value here is the pull-up -->
    <param name="pub/GPIO4" value="false" />
    <param name="pub/GPIO3" value="true" />

    <!-- set pin 5 based on /gpio5 -->
    <param name="sub/5" value="/gpio5" />
  </node>
</launch>
```
