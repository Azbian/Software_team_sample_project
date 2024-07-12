import requests

class fetchTLE:
      
      def __init__(self):
            self.satelliteName = satelliteName
            self.url = f"https://celestrak.org/NORAD/elements/gp.php?NAME={satelliteName}&FORMAT=tle"
            self.responseData = None
            
      def fetchData(self):
          response = requests.get(self.url);
          data = response.text.strip().splitlines();
          return data[1] + "\n" + data[2]
        

satelliteName = "AISSAT 1";
object = fetchTLE();
print(object.fetchData());
          