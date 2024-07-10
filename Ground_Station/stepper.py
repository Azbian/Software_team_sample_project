import RPi.GPIO as GPIO
import time

class stepper():
    def __init__(self, DIRECTION_PIN : int, STEP_PIN : int, STEPS_PER_REVOLUTION : int,MODE_PINS = None):
        self.DIRECTION_PIN=DIRECTION_PIN
        self.STEP_PIN=STEP_PIN
        self.DELAY=0.0208
        self.MODE_PINS=MODE_PINS
        self.STEPS_PER_REVOLUTION=STEPS_PER_REVOLUTION
        self.MULTIPLIER=[1,2,4,8,16,32]
        self.RESOLUTION={
            'full':(0,0,0),
            'half':(1,0,0),
            '1/4':(0,1,0),
            '1/8':(1,1,0),
            '1/16':(0,0,1)
            '1/32':(1,0,1)
        }

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIRECTION_PIN,GPIO.output)
        GPIO.setup(STEP_PIN,GPIO.output)
        if MODE_PINS is not None:
            GPIO.setup(MODE_PINS,GPIO.output)
    
    def move(self, current_angle : float, new_angle : float, direction : str, usr_reolution=None):
        direction=direction.lower()
        usr_reolution=usr_reolution.lower()
        if direction=='cw':
            GPIO.output(self.DIRECTION_PIN, 1)
        elif direction=='acw':
            GPIO.output(self.DIRECTION_PIN, 0)
        else:
            print("Enter appropiate direction")
            return
        
        reolution=self.RESOLUTION['full']
        if usr_reolution is not None:
            reolution=self.RESOLUTION[usr_reolution]
        GPIO.output(self.MODE_PINS,reolution)
        
        multilpier=self.MULTIPLIER[self.RESOLUTION.get(usr_reolution,None)]

        delay=self.DELAY/multilpier

        steps=(((new_angle-current_angle)*self.STEPS_PER_REVOLUTION)/360)*multilpier

        for i in range(steps):
            GPIO.output(self.STEP_PIN,GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(self.STEP_PIN,GPIO.LOW)
            time.sleep(delay)
                    
