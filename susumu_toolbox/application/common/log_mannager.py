import os
import sys

from loguru import logger

from susumu_toolbox.infrastructure.singleton import Singleton


# noinspection PyMethodMayBeStatic
class LogManager(Singleton):
    def __init__(self):
        pass

    def __create_log_dir_if_needed(self):
        model_data_dir = "./log"
        if not os.path.exists(model_data_dir):
            os.mkdir(model_data_dir)

    def setup_logger(self):
        self.__create_log_dir_if_needed()
        logger.remove()
        # noinspection SpellCheckingInspection
        logger.add(
            sys.stdout,
            level='DEBUG',
            # format="<green>{time:YYYY-MM-DD HH:mm:ss.SSSSSS}</green> | <level>{level:<7}</level> | {message}"
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level:<8}</level> | {message}"
        )

        log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level:<8}</level> | {message}"
        logger.add("log/{time:YYYY-MM-DD}_app.log",
                   format=log_format)
        logger.add("log/{time:YYYY-MM-DD}_error.log",
                   level="ERROR",
                   format=log_format)
