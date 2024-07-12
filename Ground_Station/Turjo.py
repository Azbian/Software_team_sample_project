import requests
import math
from skyfield.api import Topos, EarthSatellite, load, utc ,wgs84
from datetime import datetime, timedelta

class CurrentTime:
    def get_utc():
        return datetime.utcnow().replace(tzinfo=utc)

class FetchTelemetryData:
    def __init__(self, timescale):
        self.ts = timescale

    def fetch(self, sat):
        url = f'https://celestrak.org/NORAD/elements/gp.php?NAME={sat}&FORMAT=tle'
        response = requests.get(url)
        if response.ok:
            data = response.text.strip().splitlines()
            satName = data[0]
            lineOne = data[1]
            lineTwo = data[2]
            return EarthSatellite(lineOne,lineTwo,satName,self.ts)
        else:
            return("Failed while fetching data")
            
class FuturePass:
    def __init__(self, timescale, observer_location):
        self.ts = timescale
        self.observer_location = observer_location

    def calculate(self, satellite, duration_days=1):
        observer = Topos(latitude_degrees=self.observer_location['latitude'],
                         longitude_degrees=self.observer_location['longitude'])
        t0 = self.ts.utc(CurrentTime.get_utc())
        t1 = self.ts.utc(CurrentTime.get_utc() + timedelta(days=duration_days))
        times, events = satellite.find_events(observer, t0, t1)
        if len(times) < 3:
            raise ValueError("Not enough events found for a complete pass.")
        pass_times = {
            'rise': times[0].utc_datetime(),
            'culminate': times[1].utc_datetime(),
            'set': times[2].utc_datetime()
        }
        return pass_times
    

class SatellitePosition:
    def __init__(self, earth_satellite, timescale):
        self.satellite = earth_satellite
        self.ts = timescale

    def propagate(self):
        # Get the current time
        now = datetime.utcnow()

        # Convert current time to a Skyfield Time object
        t = self.ts.utc(now.year, now.month, now.day, now.hour, now.minute, now.second)

        # Compute the satellite's position
        geocentric = self.satellite.at(t)

        # Get the geodetic position (latitude, longitude)
        subpoint = wgs84.subpoint(geocentric)
        latitude = subpoint.latitude.degrees
        longitude = subpoint.longitude.degrees
        

        return latitude, longitude


class Angle:
    def __init__(self, satellite_longitude, site_longitude, site_latitude):
        self.satellite_longitude = satellite_longitude
        self.site_longitude = site_longitude
        self.site_latitude = site_latitude

    def calculate_elevation_azimuth(self):
        S_rad = math.radians(self.satellite_longitude)
        N_rad = math.radians(self.site_longitude)
        L_rad = math.radians(self.site_latitude)
        
        G = S_rad - N_rad
        
        numerator = math.cos(G) * math.cos(L_rad) - 0.1512
        denominator = math.sqrt(1 - (math.cos(G) * math.cos(L_rad))**2)
        E = math.atan(numerator / denominator)
        
        E_deg = math.degrees(E)
        
        tan_G = math.tan(G)
        sin_L = math.sin(L_rad)
        A = math.atan(tan_G / sin_L)
        
        A_deg = math.degrees(A)
        
        return E_deg, A_deg
    




class SatelliteTracker:
    def __init__(self, observer_location):
        self.observer_location = observer_location
        self.ts = load.timescale()
        self.telemetry_data_fetcher = FetchTelemetryData(self.ts)
        self.future_pass_calculator = FuturePass(self.ts, self.observer_location)

    def fetch_telemetry_data(self, sat):
        return self.telemetry_data_fetcher.fetch(sat)

    def get_local_time(self):
        return CurrentTime.get_utc()

    def get_passing_time(self, satellite):
        try:
            return self.future_pass_calculator.calculate(satellite)
        except ValueError as e:
            return str(e)

# Define observer location (latitude and longitude in degrees)
observer_location = {
    'latitude': 37.7749,
    'longitude': -122.4194
}


# Example usage

observer_longitude = 37.7749       # N
observer_latitude = -122.4194      # L











ts = load.timescale()
# Create SatelliteTracker object
tracker = SatelliteTracker(observer_location)

# Fetch telemetry data for a satellite
satelliteName = 'ISS (ZARYA)'
satellite = tracker.fetch_telemetry_data(satelliteName)

sat_position = SatellitePosition(satellite, ts)
latitude, longitude = sat_position.propagate()

#print('Latitude (degrees):', latitude)
#print('Longitude (degrees):', longitude)







tracker1 =Angle(longitude, observer_longitude, observer_latitude)
elevation, azimuth = tracker1.calculate_elevation_azimuth()

print(f"Elevation angle: {elevation:.2f} degrees")
print(f"Azimuth angle: {azimuth:.2f} degrees")





# Get current local time
local_time = tracker.get_local_time()
print("Local Time:", local_time)

# Get future passing time
passing_time = tracker.get_passing_time(satellite)
print("Future Pass Times:", passing_time)

