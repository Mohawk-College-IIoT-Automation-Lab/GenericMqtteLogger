import logging

class LoggerSingleton:
    _instance = None
    _logger_name = "mqtt_logger"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerSingleton, cls).__new__(cls)
            cls._instance.logger = logging.getLogger(cls._logger_name)
            cls._instance.logger.setLevel(logging.DEBUG)
            file_handler = logging.FileHandler(f"{cls._logger_name}.log")
            file_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            cls._instance.logger.addHandler(file_handler)
        return cls._instance
    
class Logger:
    def __init__(self, log_name:str="log"):
        self.log_name = log_name
        self.logger = logging.getLogger(self.log_name)
        self.logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(f"{self.log_name}.log")
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

