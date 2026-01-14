"""
Logging utility for the documentation analysis tool.
"""
import logging
import sys
from datetime import datetime
from pathlib import Path


def setup_logger(name: str, log_file: str = None, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with both console and optional file handlers.
    
    Args:
        name: Name of the logger
        log_file: Path to the log file (optional)
        level: Logging level (default: INFO)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent adding duplicate handlers if logger already exists
    if logger.handlers:
        return logger
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        # Create parent directories if they don't exist
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_log_file_path(base_name: str = "doc_analysis") -> str:
    """
    Generate a log file path with timestamp.
    
    Args:
        base_name: Base name for the log file
        
    Returns:
        Path to the log file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"logs/{base_name}_{timestamp}.log"


# Predefined loggers for common use cases
doc_analyzer_logger = setup_logger("doc_analyzer")
scenario_extractor_logger = setup_logger("scenario_extractor")
test_plan_generator_logger = setup_logger("test_plan_generator")