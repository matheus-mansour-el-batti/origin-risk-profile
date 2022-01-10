import logging


def setup_logger():
    logging.basicConfig(
        format="%(asctime)s | %(name)-30s : %(levelname)s : %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )
