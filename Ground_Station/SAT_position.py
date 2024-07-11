import requests
from skyfield.api import Topos, EarthSatellite, load, utc
from datetime import datetime, timedelta

class SatelliteTracker:
    def __init__(self, observer_location):
        self.observer_location = observer_location
        self.ts = load.timescale()

    def fetch_telemetry_data(self, sat):
        url = f'https://celestrak.org/NORAD/elements/gp.php?NAME={sat}&FORMAT=tle'
        response = requests.get(url)
        tle_lines = response.text.strip().splitlines()
        if len(tle_lines) < 3:
            raise ValueError(f"Invalid TLE data for satellite {sat}")
        name, line1, line2 = tle_lines[0], tle_lines[1], tle_lines[2]
        return EarthSatellite(line1, line2, name, self.ts)

    def current_time(self):
        return datetime.utcnow().replace(tzinfo=utc)

    def future_pass(self, satellite, duration_days=1):
        observer = Topos(latitude_degrees=self.observer_location['latitude'],
                         longitude_degrees=self.observer_location['longitude'])
        t0 = self.ts.utc(self.current_time())
        t1 = self.ts.utc(self.current_time() + timedelta(days=duration_days))
        times, events = satellite.find_events(observer, t0, t1)
        pass_times = {
            'rise': times[0].utc_datetime(),
            'culminate': times[1].utc_datetime(),
            'set': times[2].utc_datetime()
        }
        return pass_times

    def sat_angle(self, satellite, time_offset_hours=0):
        observer = Topos(latitude_degrees=self.observer_location['latitude'],
                         longitude_degrees=self.observer_location['longitude'])
        time = self.ts.utc(self.current_time() + timedelta(hours=time_offset_hours))
        difference = satellite - observer
        topocentric = difference.at(time)
        alt, az, distance = topocentric.altaz()

        return az.degrees, alt.degrees

    def get_local_time(self):
        return self.current_time()

    def get_passing_time(self, satellite):
        return self.future_pass(satellite)

    def get_azimuth_elevation(self, satellite):
        return self.sat_angle(satellite)

# Define observer location (latitude and longitude in degrees)
observer_location = {
    'latitude': 37.7749,
    'longitude': -122.4194
}

# Create SatelliteTracker object
tracker = SatelliteTracker(observer_location)

# Fetch telemetry data for a satellite
satellite_name = 'ISS (ZARYA)'
satellite = tracker.fetch_telemetry_data(satellite_name)

# Get current local time
local_time = tracker.get_local_time()
print("Local Time:", local_time)

# Get future passing time
passing_time = tracker.get_passing_time(satellite)
print("Future Pass Times:", passing_time)

# Get azimuth and elevation
azimuth, elevation = tracker.get_azimuth_elevation(satellite)
print("Azimuth:", azimuth)
print("Elevation:", elevation)