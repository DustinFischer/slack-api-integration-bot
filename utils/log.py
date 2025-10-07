import logging

from config import Config

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
)


def get_logger(name):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG if Config.DEBUG else logging.INFO)
    # add handlers here
    return log
