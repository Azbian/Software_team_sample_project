import time
import os
import tracker



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
    current_time=tracker.CurrentTime()
    local_time = sat_tracker.get_local_time()
    passing_time = sat_tracker.get_passing_time(satellite)
    latitude, longitude = sat_tracker.get_satellite_position(satellite)

    # Get the azimuth and elevation angles
    new_elevation, new_azimuth= sat_tracker.get_elevation_azimuth(satellite)

    print(f"Local time: {local_time}")
    current_time.pretty_print_passing_time(passing_time)
    print(f"Satellite current position:\nAzimuth: {new_azimuth:.3f}    Elevation: {new_elevation:.3f}")
    time.sleep(.2)