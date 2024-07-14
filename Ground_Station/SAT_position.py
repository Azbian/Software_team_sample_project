import ephem
import urllib.request

class SatelliteTracker:
    def __init__(self, observer_latitude, observer_longitude, satellite_name):
        """
        Initialize the SatelliteTracker with the observer's latitude and longitude and the satellite's name.
        """
        self.observer = ephem.Observer()
        self.observer.lat = ephem.degrees(observer_latitude)
        self.observer.lon = ephem.degrees(observer_longitude)
        self.sat_name = satellite_name
        self.tle_url = self.create_tle_url(satellite_name)
        self.tle_data = self.fetch_tle_data()

    def create_tle_url(self, satellite_name):
        """
        Create the URL to fetch TLE data for the given satellite name.
        """
        sat = satellite_name.replace(' ', '%20')
        return f'https://celestrak.org/NORAD/elements/gp.php?NAME={sat}&FORMAT=tle'

    def fetch_tle_data(self):
        """
        Fetch the TLE data from the URL and return it as a list of lines.
        """
        req = urllib.request.urlopen(self.tle_url)
        tle_data = req.read().decode("utf-8").strip().split('\n')
        return tle_data

    def get_tle_data(self):
        """
        Return the TLE data.
        """
        return self.tle_data