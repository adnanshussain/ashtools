import logging, sys
from ashtools.common import *

# Define color dictionary based on logging levels
LOG_COLORS = {
    logging.DEBUG: WHITE_BOLD.ascii,
    logging.INFO: RESET.ascii,
    logging.WARN: ORANGE.ascii,
    logging.ERROR: BRIGHT_RED_BOLD.ascii,
    logging.CRITICAL: RED_BOLD.ascii,
    "RESET": RESET.ascii,
}


# Create a custom log formatter
class _ColorFormatter(logging.Formatter):
    def format(self, record):
        log_message = super(_ColorFormatter, self).format(record)
        return f"{LOG_COLORS[record.levelno]}{log_message}{LOG_COLORS['RESET']}"


_app_logger = logging.getLogger("ashtools")

logging.basicConfig(level=logging.INFO, datefmt="%d-%m-%Y %H:%M:%S", handlers=[])

format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Create a console handler and set the formatter
_console_handler = logging.StreamHandler()
_console_handler.setFormatter(_ColorFormatter(format))

# Add the console handler to the logger
_app_logger.addHandler(_console_handler)


def change_log_level(level):
    _app_logger.setLevel(level)


def also_log_to_file(file_path):
    _app_logger.addHandler(logging.FileHandler(file_path))


def debug_log(message):
    _app_logger.debug(message)


def info_log(message):
    _app_logger.info(message)


def error_log(message):
    _app_logger.error(message)


debug_log(
    f"{GREEN_BOLD_ITALIC.ascii}logginghelper loaded. logging INFO by default. Change this at any point in time by calling change_log_level(whatever_level)."
)
