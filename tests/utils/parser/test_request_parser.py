from unittest.mock import patch, MagicMock

import pytest

from utils.parser.request_parser import CustomRequestParser


def test_parse_args_success():
    def parse(req, bundle_errors):
        return 'value', True

    req = MagicMock()
    ns = MagicMock()
    ns.return_value = {}
    arg = MagicMock
    arg.dest = 'dest'
    arg.parse = parse
    ins = CustomRequestParser(namespace_class=ns)
    ins.args = [arg]
    assert ins.parse_args(req=req) == {'dest': 'value'}


def test_parse_args_error():
    def parse(req, bundle_errors):
        return ValueError(), {'key': 'error'}

    def raise_error():
        raise Exception

    req = MagicMock()
    ns = MagicMock()
    ns.return_value = {}
    arg = MagicMock
    arg.dest = 'dest'
    arg.parse = parse
    arg.store_missing = True
    ins = CustomRequestParser(namespace_class=ns)
    ins.args = [arg]
    with patch('flask_restful.abort', side_effect=raise_error) as abort_mock:
        with pytest.raises(Exception):
            ins.parse_args(req=req)
        abort_mock.assert_called_with(400, code=100, message='key: error')
