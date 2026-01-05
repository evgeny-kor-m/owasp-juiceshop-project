import logging
import os
from datetime import datetime
from pathlib import Path
from test_automation_framework.config.config import Config

def setup_logging():
    """
    Global logging configuration for the entire framework.
    Uses directory paths and log levels defined in the main Config class.
    """
    log_dir = Path(Config.LOGS_PATH)
    log_level_str = Config.LOG_LEVEL.upper()
    log_level = getattr(logging, log_level_str, logging.INFO)

    if not log_dir.exists():
        os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    log_file_name = f"test_run_{timestamp}.log"
    log_path = log_dir / log_file_name

    log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"

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