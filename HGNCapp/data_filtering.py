import sys
import logging
from logger import setup_logging

logger = logging.getLogger(__name__)

def echo(phrase: str) -> None:
   """A dummy wrapper around print."""
   # for demonstration purposes, you can imagine that there is some
   # valuable and reusable logic inside this function]
   logger.debug(f"Printing: {phrase}")
   print(phrase)

def main() -> int:
    """Echo the input arguments to standard output"""
    logger.debug(f"Received argument: {sys.argv[1]}")
    phrase = sys.argv[1]
    echo(phrase)
    return 0

if __name__ == '__main__':
    setup_logging()
    logger.debug(f"Entry function")
    sys.exit(main())