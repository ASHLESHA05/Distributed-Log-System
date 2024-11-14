import json

class Logger1:
    def __init__(self, reg=None, logs=None, heartbeat=None):
        self.logs = logs
        self.heartbeat = heartbeat
        if reg:
            print("Reg: ", json.dumps(reg, indent=4))
        if self.logs:  # Use self.logs instead of logs
            print('Logs: ', json.dumps(self.logs, indent=4))
        if self.heartbeat:  # Use self.heartbeat instead of heartbeat
            print('HeartBeat: ', json.dumps(self.heartbeat, indent=4))
