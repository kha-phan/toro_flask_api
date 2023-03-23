import pytest
import os
from unittest.mock import patch

from utils.custom_config import Config, ConfigParser
from definitions import ROOT_DIR

CONFIG_FILE_PATH = os.environ.get('CONFIG_FILE_PATH', os.path.join('./', 'config.yml.sample'))


@pytest.fixture
def user_data() -> str:
    return 'user1'


@pytest.fixture
def config_data(user_data) -> dict:
    return {
        'username': user_data
    }


@pytest.fixture
def path_data() -> str:
    return 'username'


@pytest.fixture
def default_data() -> str:
    return 'default'


class TestConfig:
    @pytest.fixture(autouse=True)
    def _setup(self, config_data):
        self.config = Config(config_data)

    def test_init(self, config_data):
        self.config._data = config_data

    def test_get_will_return_default(self, path_data, default_data):
        res = self.config.get(path_data + '.password', default_data)
        assert res == default_data

    def test_get_will_return_location(self, path_data, user_data, default_data):
        res = self.config.get(path_data, default_data)
        assert res == user_data


class TestConfigParser:
    @pytest.fixture(autouse=True)
    def _setup(self, config_data):
        self.config_parser = ConfigParser()

    def test_post_load_config(self, config_data):
        res = self.config_parser.post_load_config(config_data)
        assert res == config_data

    def test_load_config_file(self, config_data):
        with patch('yaml.load', return_value=config_data):
            res = self.config_parser.load_config_file(CONFIG_FILE_PATH)
            assert res == config_data

    def test_get_config(self, config_data):
        with patch('yaml.load', return_value=config_data):
            res = self.config_parser.get_config(CONFIG_FILE_PATH)
            assert res is not None
