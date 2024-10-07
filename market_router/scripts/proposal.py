import sys

from loguru import logger

from market_router import object_creation


def create_proposal():
    try:
        object_creation.submit_proposal()

    except Exception as e:
        raise e


if __name__ == "__main__":
    try:
        create_proposal()
    except Exception as e:
        logger.error(f"The pipeline raised the following error: {e}")
        sys.exit(1)
