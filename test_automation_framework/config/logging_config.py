import logging
from datetime import datetime
from pathlib import Path
from test_automation_framework.config.config import Config

def setup_logging():
    """
    Global logging configuration for the entire framework.
    Uses directory paths and log levels defined in the main Config class.
    """
    # 1. Fetch settings from the base configuration
    log_dir = Path(Config.LOGS_DIR)
    log_level_str = Config.LOG_LEVEL.upper()
    log_level = getattr(logging, log_level_str, logging.INFO)

    # 2. Create the logs directory if it doesn't exist
    log_dir.mkdir(parents=True, exist_ok=True)

    # 3. Generate a log filename with a timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    log_file_name = f"test_run_{timestamp}.log"
    log_path = log_dir / log_file_name

    # 4. Define the log message format
    log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"

    # 5. Configure the root logger
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.StreamHandler(),                              # Console output (useful for Docker logs)
            logging.FileHandler(str(log_path), encoding='utf-8')  # Persistent log file
        ]
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Level: {log_level_str}, File: {log_path}")

    return logger