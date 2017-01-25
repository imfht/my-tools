import logging


class logger_util():
    # ----------------------------------------------------------------------
    @staticmethod
    def get_formatter():
        """get_logger"""
        logger = logging.getLogger(name='UtilLogger')
        logger.setLevel(logging.ERROR)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    # ----------------------------------------------------------------------
    @staticmethod
    def log_warning(msg):
        """log warning msg"""
        logger_util.get_formatter().warning(msg)

    # ----------------------------------------------------------------------
    @staticmethod
    def log_debug(msg):
        """log debug msg"""
        logger_util.get_formatter().debug(msg)

    # ----------------------------------------------------------------------
    @staticmethod
    def log_error(msg):
        """log error msg"""
        logger_util.get_formatter().error(msg)

