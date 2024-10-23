import logging


def setup(log_level="INFO", force_reconfigure=False):
    level = getattr(logging, log_level.upper())
    
    # logging.basicConfig(format='%(levelname)s:%(message)s', level=level)
    debug_handler = logging.StreamHandler()
    debug_handler.setLevel(logging.DEBUG)

    # Define the log format for DEBUG messages (logger name, filename, line number, and message)
    debug_formatter = logging.Formatter("[%(asctime)s][%(levelname)s][%(name)s][%(filename)s:%(lineno)d] - %(message)s")
    debug_handler.setFormatter(debug_formatter)

    # Add a filter so that the DEBUG messages are handled only by this handler
    debug_handler.addFilter(lambda record: record.levelno == logging.DEBUG)


    non_debug_handler = logging.StreamHandler()
    non_debug_handler.setLevel(level)  # Set to the passed log level (default INFO)
    non_debug_formatter = logging.Formatter("[%(asctime)s][%(levelname)s][%(name)s] - %(message)s")
    non_debug_handler.setFormatter(non_debug_formatter)
    non_debug_handler.addFilter(lambda record: record.levelno >= level and record.levelno != logging.DEBUG)


    if not force_reconfigure:
        # logging.basicConfig will not do anything if
        # someone else has already used logging.
        logging.basicConfig(
            level=level,
            handlers=[debug_handler, non_debug_handler]
        )
    else:
        root_logger = logging.getLogger()
        
        # nuke any other configurations
        while root_logger.hasHandlers():
            root_logger.removeHandler(root_logger.handlers[0])

        root_logger.addHandler(debug_handler)
        root_logger.addHandler(non_debug_handler)
        root_logger.setLevel(level)
            
