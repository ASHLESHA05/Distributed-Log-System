from fluent import sender
import json

class Logger1:
    def __init__(self, reg=None, heartbeat=None, logs=None):
        self.logger = sender.FluentSender(
            "inventory_service", host="localhost", port=24224
        )

        if reg:
            self.send_log("log", json.dumps(reg, indent=4))
            print("Registration Log: ", json.dumps(reg, indent=4))

        if heartbeat:
            self.send_log("heartbeat", json.dumps(heartbeat, indent=4))
            print("Heartbeat Log: ", json.dumps(heartbeat, indent=4))

        if logs:
            self.send_log("log", json.dumps(logs, indent=4))
            print("Log: ", json.dumps(logs, indent=4))

    def send_log(self, tag, data):
        try:
            self.logger.emit(tag, data)
        except Exception as e:
            print(f"Failed to send log to Fluentd: {e}")

    def close(self):
        self.logger.close()