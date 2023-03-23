import pytest
from unittest.mock import patch

import logging


@pytest.fixture
def expected_logger_data():
    return logging.getLogger('betfinder')


@patch('utils.config.get', return_value={})
def test_logger(mock, expected_logger_data):
    from utils import logger
    assert logger == expected_logger_data
