import time
import os
import stepper

azimuth_stepper=stepper(5,6,200,(17,27,22))
elevation_stepper=stepper(23,24,200,(14,15,18))

# Latitude and longitude of he observer (in degrees)
#BSMRAAU
observer_lat = '25.9023522'   
observer_lon = '89.4325258'

#Dhaka
#observer_lat = '23.7131986'  
#observer_lon = '90.4016137'


# User input and change that name according to URL
sat_name= input("Enter the name of the CUBESAT (e.g. CUTE-1 (CO-55)): ")


current_azimuth=0
current_elevation=0

while True:
    # Get the azimuth and elevation angles and convert them radian to degree
    new_azimuth = 0
    new_elevation = 0

    #Move the position
    azimuth_stepper(current_azimuth,new_azimuth,'c','full')
    elevation_stepper(current_elevation,new_elevation,'c','full')