# Raspberry Pi GPIO through ROS

### Example launch file

```xml
<launch>
  <node pkg="ltu_actor_rpi_gpio" type="run.py" name="rpi_gpio">
    <!-- value here is the pull-up -->
    <param name="pub/GPIO4" value="false" />
    <param name="pub/GPIO3" value="true" />
  </node>
</launch>
```
