import logging
import sys

from src.settings import fast_ai_settings

logger = logging.getLogger()

formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s")

stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler(fast_ai_settings.log_file)

logger.handlers = [stream_handler, file_handler]

logger.setLevel(logging.INFO)
