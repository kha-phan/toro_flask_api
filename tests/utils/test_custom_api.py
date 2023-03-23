from unittest.mock import patch

from werkzeug.exceptions import HTTPException, BadRequest

from exceptions import CustomException, BadRequest as CustomBadRequest
from utils.custom_api import CustomApi


def test_handle_error_custom_exc():
    with patch('utils.custom_api.CustomApi.make_response', return_value='tested') as mk_res_mock:
        assert CustomApi().handle_error(CustomException()) == 'tested'
        mk_res_mock.assert_called_with(
            {'error': {'code': CustomException.error_code, 'message': CustomException.error_message}},
            CustomException.status_code)


def test_bad_request():
    with patch('utils.custom_api.CustomApi.make_response', return_value='tested') as mk_res_mock:
        assert CustomApi().handle_error(BadRequest(description='abc')) == 'tested'
        mk_res_mock.assert_called_with(
            {'error': {'code': CustomBadRequest.error_code, 'message': 'abc'}}, BadRequest.code)


def test_handle_error_unknown_exc():
    with patch('utils.custom_api.CustomApi.make_response', return_value='tested') as mk_res_mock, \
            patch('logging.Logger._log'):
        assert CustomApi().handle_error(Exception()) == 'tested'
        mk_res_mock.assert_called_with(
            {'error': {'code': CustomException.error_code, 'message': CustomException.error_message}},
            CustomException.status_code)


def test_handle_error_delegate():
    with patch('flask_restful.Api.handle_error', return_value='tested') as super_mock:
        e = HTTPException()
        assert CustomApi().handle_error(e) == 'tested'
        super_mock.assert_called_with(e)
