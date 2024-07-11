from datetime import datetime

class currentTime:
    def __init__(self):
        current = self.current_time = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
        print(current)


localTime = currentTime()

