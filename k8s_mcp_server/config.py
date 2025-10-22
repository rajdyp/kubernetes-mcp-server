"""Configuration and constants"""
import logging
from pathlib import Path

# Configuration constants
DEFAULT_TIMEOUT = 30
DEFAULT_NAMESPACE = "default"
KUBECONFIG_DEFAULT_PATH = Path.home() / ".kube" / "config"

# Logging configuration
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

def setup_logging(level=LOG_LEVEL):
    """Setup logging configuration"""
    logging.basicConfig(level=level, format=LOG_FORMAT)
    return logging.getLogger(__name__)

# Global logger
logger = setup_logging()