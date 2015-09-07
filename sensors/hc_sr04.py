import math
import time

TRIG, ECHO = 17, 18

def setup(trigger=TRIG, echo=ECHO):
    import hcsr04sensor.sensor as sensor

    # todo: the temperature could actually be taken by another
    # sensor, it then would have to live rather in the actual
    # method that takes the measurment
    m = sensor.Measurement(TRIG, ECHO, 20, 'metric', 1)

    def sense():
        """
        Sonar distance sensor
        """
        return m.distance_metric(m.raw_distance(1))

    def unchanged(**kwargs):
        """
        Do whatever is the simplest to spit out a measurment
        """
        return sense()

    return unchanged
