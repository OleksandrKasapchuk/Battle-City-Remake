import sys,logging
from constants import *
logging.basicConfig(level=logging.INFO, filename=log_file, filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
class StreamToLogger:
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())
    def flush(self):
        pass

sys.stdout = StreamToLogger(logging.getLogger(), logging.INFO)
sys.stderr = StreamToLogger(logging.getLogger(), logging.ERROR) 
