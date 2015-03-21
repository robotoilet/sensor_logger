import math
import time

TRIG, ECHO = 17, 18

def setup(trigger=TRIG, echo=ECHO):
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(trigger,GPIO.OUT)
    GPIO.setup(echo,GPIO.IN)
    GPIO.output(trigger, False)
    print("Waiting For Sensor To Settle")
    time.sleep(2)

    def sense():
        """
        Sonar distance sensor
        """

        GPIO.output(trigger, True)
        time.sleep(0.0001)
        GPIO.output(trigger, False)

        while GPIO.input(echo) == 0:
            pulse_start = time.time()

        while GPIO.input(echo) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        GPIO.output(trigger, False)
        return round(distance, 2)

        # TODO: do we need this???
        ##GPIO.cleanup()

    def outliers_cleaned():
        """
        Remove outliers, which are defined as having a distance from the mean
        of five measurments bigger than two standard deviations.

        Returns the mean of the remaining measurments.
        """
        measurments = [sense() for i in range(5)]
        print("measurments to be outlier cleaned: %s" % measurments)

        mean = lambda values: sum(values) / len(values)
        avg = mean(measurments)
        variance = map(lambda x: (x - avg) ** 2, measurments)
        stdev = math.sqrt(mean(variance))
        measurments = [m for m in measurments if abs(m - avg) <= stdev]
        return mean(measurments)

    return outliers_cleaned
