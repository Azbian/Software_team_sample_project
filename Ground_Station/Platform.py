import time
import os
import stepper
import tracker


azimuth_stepper=stepper(5,6,200,(17,27,22))
elevation_stepper=stepper(23,24,200,(14,15,18))

# Latitude and longitude of he observer (in degrees)
#BSMRAAU

observer_location = {
    'latitude': 25.9023522,
    'longitude': 89.4325258
}

#Dhaka
#observer_lat = '23.7131986'  
#observer_lon = '90.4016137'

sat_tracker = tracker.SatelliteTracker(observer_location)


# User input and change that name according to URL
sat_name= input("Enter the name of the CUBESAT (e.g. CUTE-1 (CO-55)): ")

satellite = sat_tracker.fetch_telemetry_data(sat_name)

current_azimuth=0
current_elevation=0

while True:
    os.system('clear')
    local_time = sat_tracker.get_local_time()
    passing_time = sat_tracker.get_passing_time(satellite)
    latitude, longitude = sat_tracker.get_satellite_position(satellite)

    # Get the azimuth and elevation angles
    new_elevation, new_azimuth= sat_tracker.get_elevation_azimuth(satellite)

    print(f"Local time: {local_time}\nPassing time: {passing_time}\nSatellite current position:\nAzimuth: {new_azimuth}    Elevation: {new_elevation}")

    #Move the position if the satellite elevation is greater than -2
    if new_elevation>-2:
        azimuth_stepper.move(current_azimuth,new_azimuth,'full')
        elevation_stepper.move(current_elevation,new_elevation,'full')
        current_azimuth=new_azimuth
        current_elevation=new_elevation
    else:
        azimuth_stepper.move(current_azimuth,0,'full')
        elevation_stepper.move(current_elevation,0,'full')
        current_azimuth=0
        current_elevation=0