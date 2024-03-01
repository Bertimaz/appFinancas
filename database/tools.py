import logging
import os
from datetime import datetime

def configure_logger(log_folder):
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create the logs folder if it doesn't exist
    os.makedirs(log_folder, exist_ok=True)

    # Generate log file name based on current date and time
    current_datetime = datetime.now()
    log_file_name = f"log_{current_datetime.strftime('%Y%m%d_%H%M')}.log"
    log_file_path = os.path.join(log_folder, log_file_name)

    # Create a file handler and set the logging level
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger

if __name__ == "__main__":
    # Configure and create a logger
    logger = configure_logger()

    try:
        # Your code here
        logger.info("Program started")

        # Example log messages
        logger.debug("This is a debug message")
        logger.info("This is an info message")
        logger.warning("This is a warning message")
        logger.error("This is an error message")
        logger.critical("This is a critical message")

        # Your code here
        logger.info("Program completed")

    except Exception as e:
        # Log any exceptions
        logger.exception(f"An error occurred: {e}")
