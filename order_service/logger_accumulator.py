import fluent.sender
import fluent.event
import json

class FluentdLogger:
    def __init__(self, tag='order_service', host='localhost', port=24224):
        # Initialize Fluentd connection
        self.fluentd_logger = fluent.sender.FluentSender(tag, host=host, port=port)

    def add_registration(self, reg):
        self.fluentd_logger.emit('registration', reg)
        print("Registration logged: ", json.dumps(reg, indent=4))

    def add_log(self, log):
        self.fluentd_logger.emit('log', log)
        print("Log sent to Fluentd: ", json.dumps(log, indent=4))

    def add_heartbeat(self, heartbeat):
        self.fluentd_logger.emit('heartbeat', heartbeat)
        print("Heartbeat sent to Fluentd: ", json.dumps(heartbeat, indent=4))

    def close(self):
        # Close the Fluentd connection to ensure all logs are flushed
        self.fluentd_logger.close()