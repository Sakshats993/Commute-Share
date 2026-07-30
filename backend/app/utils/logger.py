"""
==================================================
CommuteShare Logger Utility

Backend Internship Project
Bermer Software Private Limited

Provides centralized logging configuration
for the entire backend application.

Features:
- Console Logging
- File Logging
- Consistent Formatting
==================================================
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# ==========================================================
# Log Directory
# ==========================================================

LOG_DIRECTORY = Path("logs")
LOG_DIRECTORY.mkdir(exist_ok=True)

LOG_FILE = LOG_DIRECTORY / "commuteshare.log"

# ==========================================================
# Logger Configuration
# ==========================================================

LOGGER_NAME = "commuteshare"

logger = logging.getLogger(LOGGER_NAME)

logger.setLevel(logging.INFO)

# Prevent duplicate log messages
logger.propagate = False

# ==========================================================
# Formatter
# ==========================================================

formatter = logging.Formatter(
    fmt=(
        "%(asctime)s | "
        "%(levelname)-8s | "
        "%(name)s | "
        "%(filename)s:%(lineno)d | "
        "%(message)s"
    ),
    datefmt="%Y-%m-%d %H:%M:%S",
)

# ==========================================================
# Console Handler
# ==========================================================

console_handler = logging.StreamHandler()

console_handler.setLevel(logging.INFO)

console_handler.setFormatter(formatter)

# ==========================================================
# File Handler
# ==========================================================

file_handler = RotatingFileHandler(
    filename=LOG_FILE,
    maxBytes=5 * 1024 * 1024,   # 5 MB
    backupCount=5,
    encoding="utf-8",
)

file_handler.setLevel(logging.INFO)

file_handler.setFormatter(formatter)

# ==========================================================
# Avoid Duplicate Handlers
# ==========================================================

if not logger.handlers:

    logger.addHandler(console_handler)

    logger.addHandler(file_handler)

# ==========================================================
# Export
# ==========================================================

__all__ = [
    "logger",
]