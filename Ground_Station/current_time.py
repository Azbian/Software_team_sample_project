from datetime import datetime,timezone

class currentTime:
    def __init__(self):
        # current = self.current_time = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
        # print(current)
        current = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + datetime.now(timezone.utc).strftime('%z')
        print(current)

localTime = currentTime()

