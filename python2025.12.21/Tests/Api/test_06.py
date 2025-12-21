import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)


def test_06():
    logger.info("this is a log")
