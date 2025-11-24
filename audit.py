import logging
import logging.handlers
import os


def _configure_logger(path='app.log'):
    logger = logging.getLogger('registrasi_audit')
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    handler = logging.handlers.RotatingFileHandler(path, maxBytes=5 * 1024 * 1024, backupCount=5)
    fmt = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    return logger


logger = _configure_logger()


def log(action: str, message: str = '', **extra):
    """Log an audit action with optional extra details."""
    extras = ' '.join(f"{k}={v}" for k, v in extra.items())
    logger.info(f"{action} - {message} {extras}")
