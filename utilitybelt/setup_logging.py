import logging


def setup(log_level="INFO"):
    level = getattr(logging, log_level.upper())
    
    # logging.basicConfig(format='%(levelname)s:%(message)s', level=level)
    debug_handler = logging.StreamHandler()
    debug_handler.setLevel(logging.DEBUG)

    # Define the log format for DEBUG messages (logger name, filename, line number, and message)
    debug_formatter = logging.Formatter('%(levelname)s:%(name)s:%(filename)s:%(lineno)d: %(message)s')
    debug_handler.setFormatter(debug_formatter)

    # Add a filter so that the DEBUG messages are handled only by this handler
    debug_handler.addFilter(lambda record: record.levelno == logging.DEBUG)


    non_debug_handler = logging.StreamHandler()
    non_debug_handler.setLevel(level)  # Set to the passed log level (default INFO)
    non_debug_formatter = logging.Formatter('%(levelname)s:%(name)s: %(message)s')
    non_debug_handler.setFormatter(non_debug_formatter)
    non_debug_handler.addFilter(lambda record: record.levelno >= level and record.levelno != logging.DEBUG)


    logging.basicConfig(
        format='%(levelname)s:%(name)s: %(message)s',
        level=logging.DEBUG,
        handlers=[debug_handler, non_debug_handler]
    )
