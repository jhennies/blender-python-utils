
import logging


def set_logging(verbose=False):

    logging.basicConfig(
        format='%(asctime)s | %(levelname)s | %(message)s',
        level=logging.DEBUG if verbose else logging.INFO,
        datefmt='%y-%m-%d %H:%M:%S'
    )


