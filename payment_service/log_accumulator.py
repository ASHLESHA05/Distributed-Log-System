import json
from fluent import sender
from fluent import event
sender.setup('fluentd.payment_service', host='localhost', port=9880)

class Logger1:
    def __init__(self, reg=None, logs=None, heartbeat=None):
        self.logs = logs
        self.heartbeat = heartbeat
        if reg:
            event.Event('Registration',reg)
        if self.logs:  # Use self.logs instead of logs
            event.Event('Logs',logs)
        if self.heartbeat:  # Use self.heartbeat instead of heartbeat
            event.Event('HeartBeat',heartbeat)
