def setup():
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)

    TRIG, ECHO = 17, 18

    def sense(trigger=TRIG, echo=ECHO):
        """
        Sonar distance sensor
        """
        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)
        
        GPIO.output(TRIG, False)
        print("Waiting For Sensor To Settle")
        time.sleep(2)
        
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        
        while GPIO.input(ECHO) == 0:
          pulse_start = time.time()
        
        while GPIO.input(ECHO) == 1:
          pulse_end = time.time()      
        
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        
        print("Distance:",distance,"cm")
        
        GPIO.cleanup()
    return sense
