import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import time
import os

# will be used to configure pin 21 and 20 on the RPi as the trigger and echo pins for the ultrasonic sensor
TRIG = 21
ECHO = 20
SPEED_SOUND = 343
num_samp = 0
displacement_value = input("Please enter the displacement value measuring (cm): ")

x_values = []
y_values = []

# will use the setmode function in the GPIO.RPi module to set the specific enumeration system of the GPIO pins with BCM (Broadcom)
GPIO.setmode(GPIO.BCM)

# will use the setup function in the GPIO.RPi module to set the designated TRIGGER and ECHO GPIO pins as output and input respectively
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

while True:
    
    num_samp = num_samp + 1
    
    print("distance measurement in progress")

    # will set the trigger pin to voltage LOW
    GPIO.output(TRIG, False)

    print("Waiting for sensor to settle before operating it")
    time.sleep(0.2)

    # set the trigger pin to voltage HIGH for 10 microseconds before turning off signal
    GPIO.output(TRIG, True)
    time.sleep(0.00001) # the parameter for sleep is seconds so 10^-5 -> 10 microseconds
    GPIO.output(TRIG, False)

    # wait until ECHO is HIGH, the moment it turns to HIGH signifies that the sound wave has just been emitted
    while GPIO.input(ECHO) == 0:
        # this will keep getting current time in seconds (current time with respect to a reference time being 0) until ECHO is HIGH
        # this will serve as time initial in order to calculate the duration of ECHO
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        # will keep updating time final until the ECHO signal becomes LOW again
        pulse_end = time.time()

    # calculate the time duration of the ECHO signal (which is the time it took for the sound wave to be received)
    pulse_duration = pulse_end - pulse_start
    
    # calculate the displacement and print the result
    distance = pulse_duration * SPEED_SOUND
    displacement = distance / 2
    displacement_in_cm = displacement * 100
    print("displacement: ", displacement_in_cm, " cm")
    
    # creating data points to plot
    x_values.append(num_samp)
    y_values.append(displacement_in_cm)
    
    # will create the plot after 25 samples
    if num_samp == 25:
        
        # storing the data in text file
        with open("data.txt", 'w') as f:
            f.write("number sample : displacement (cm)")
            f.write(os.linesep)
            for i in range(0, len(x_values)):
                f.write(f"{i} : {y_values[i]}");
                f.write(os.linesep)
        
        # setting up plot
        plt.plot(x_values, y_values)
        # plt.ylim(0, 100)
        
        plt.xlabel("number sample")
        plt.ylabel("displacement")
        plt.title(f"displacement vs. number sample (for {displacement_value} cm)")
        
        # showing plot
        plt.show()
    
        # reset the num_samp value
        num_samp = 0
        # clearing the data lists for new data set
        x_values.clear()
        y_values.clear()
        # ask for new displacement measuring
        displacement_value = input("Please enter the displacement value measuring (cm): ")
    
    # wait 0.5 seconds before acquiring the next data point
    time.sleep(0.25)