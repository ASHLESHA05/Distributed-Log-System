from app.components.logger.logger import MyLogger

class ServiceSimulation:
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.logger = MyLogger(service_name)

    def success_log(self):
        msg = f"{self.service_name}: Successful Operation"
        return msg

    def warn_logs(self):
        msg = f"{self.service_name}: Warning — something might be off"
        return msg

    def error_log(self):
        msg = f"{self.service_name}: ERROR — critical issue!"
        return msg

    def debug_log(self):
        msg = f"{self.service_name}: Debugging data here..."
        return msg
