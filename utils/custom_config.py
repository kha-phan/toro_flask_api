import os
import yaml
from typing import Any

from .logger import logger
from .definition import ROOT_DIR


CONFIG_FILE_PATH = os.environ.get('CONFIG_FILE_PATH', os.path.join(ROOT_DIR, 'config.yml'))


class Config:
    PATH_SEPARATOR = '.'

    def __init__(self, config_data: dict):
        self._data = config_data

    def get(self, path: str, default: Any = None) -> Any:
        locations = path.split(self.PATH_SEPARATOR)
        current_location = self._data
        for location in locations:
            if location in current_location:
                current_location = current_location[location]
            else:
                return default
        return current_location


class ConfigParser:
    _instance = None

    @staticmethod
    def post_load_config(raw_config: dict) -> dict:
        # validate & transfer config if needed, skip for now
        return raw_config

    @classmethod
    def load_config_file(cls, config_file: str) -> dict:
        try:
            with open(config_file, 'r') as config_file:
                cfg = yaml.load(config_file, Loader=yaml.FullLoader) or {}
            logger.info('Custom config has been loaded.')
        except FileNotFoundError:
            cfg = {}
            logger.warning('Custom config has NOT been loaded!')
        return cls.post_load_config(cfg)

    @classmethod
    def get_config(cls, config_file: str) -> Config:
        if cls._instance is None:
            cls._instance = Config(cls.load_config_file(config_file))
        return cls._instance


config = ConfigParser.get_config(CONFIG_FILE_PATH)
