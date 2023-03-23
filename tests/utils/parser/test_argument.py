from unittest.mock import patch

from flask import Flask

from utils.parser.argument import CustomArgument


def test_handle_validation_error_bundle():
    app = Flask(__name__)
    with app.test_request_context():
        assert CustomArgument('name').handle_validation_error('error msg', True) == ('error msg', {'name': 'error msg'})


def test_handle_validation_error_no_bundle():
    app = Flask(__name__)
    with app.test_request_context(), patch('flask_restful.abort') as abort_mock:
        CustomArgument('name').handle_validation_error('error msg', False)
        abort_mock.assert_called_with(400, error={"code": 100, "message": "name: error msg"})
