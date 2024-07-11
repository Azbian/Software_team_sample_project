import ephem
import urllib.request
import time
import os

class SatelliteTracker:
    def __init__(self, observer_latitude, observer_longitude, satellite_name):
        self.observer = ephem.Observer()
        self.observer.lat = ephem.degrees(observer_latitude)
        self.observer.lon = ephem.degrees(observer_longitude)
        self.sat_name = satellite_name
        self.tle_url = self._create_tle_url(satellite_name)
        self.tle_data = self._fetch_tle_data()
        self.sat = self._create_satellite(self.tle_data)

    def _create_tle_url(self, satellite_name):
        sat = satellite_name.replace(' ', '%20')
        return f'https://celestrak.org/NORAD/elements/gp.php?NAME={sat}&FORMAT=tle'

    def _fetch_tle_data(self):
        req = urllib.request.urlopen(self.tle_url)
        tle_data = req.read().decode("utf-8").strip().split('\n')
        return tle_data

    def _create_satellite(self, tle_data):
        return ephem.readtle(tle_data[0], tle_data[1], tle_data[2])

    def track(self):
        while True:
            self.observer.date = ephem.now()
            self.sat.compute(self.observer)

            azimuth = self.sat.az * 180 / ephem.pi
            elevation = self.sat.alt * 180 / ephem.pi

            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Real time: {ephem.localtime(ephem.now())}")
            print(f"Estimated time to next pass: {ephem.localtime(self.observer.next_pass(self.sat)[0]) - ephem.localtime(ephem.now())}")
            print(f"Azimuth: {azimuth:.2f}°, Elevation: {elevation:.2f}°")

            # Display TLE information
            print("\nTLE Information:")
            print(f"Name: {self.tle_data[0]}")
            print(f"TLE Line 1: {self.tle_data[1]}")
            print(f"TLE Line 2: {self.tle_data[2]}")
            time.sleep(1.0)

observer_latitude = '23.7719'
observer_longitude = '90.3892'
satellite_name = input("Enter Name: ")

tracker = SatelliteTracker(observer_latitude, observer_longitude, satellite_name)
tracker.track()
