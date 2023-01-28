import flask_restful
from flask import request
from flask_restful.reqparse import RequestParser, Namespace
from werkzeug import exceptions

from .argument import CustomArgument


class CustomRequestParser(RequestParser):
    def __init__(self, argument_class=CustomArgument, namespace_class=Namespace, trim=False, bundle_errors=False):
        """ Override to use our CustomArgument """
        super().__init__(argument_class, namespace_class, trim, bundle_errors)

    def parse_args(self, req=None, strict=False, http_error_code=400):
        """ Override to change the abort message

        :param req: Can be used to overwrite request from Flask
        :param strict: if req includes args not in parser, throw 400 BadRequest exception
        :param http_error_code: use custom error code for `flask_restful.abort()`
        """
        if req is None:
            req = request

        namespace = self.namespace_class()

        # A record of arguments not yet parsed; as each is found
        # among self.args, it will be popped out
        req.unparsed_arguments = dict(self.argument_class('').source(req)) if strict else {}
        errors = {}
        for arg in self.args:
            value, found = arg.parse(req, self.bundle_errors)
            if isinstance(value, ValueError):
                errors.update(found)
                found = None
            if found or arg.store_missing:
                namespace[arg.dest or arg.name] = value
        if errors:
            flask_restful.abort(http_error_code, code=100, message=', '.join(f'{k}: {v}' for k, v in errors.items()))

        if strict and req.unparsed_arguments:
            raise exceptions.BadRequest('Unknown arguments: %s' % ', '.join(req.unparsed_arguments.keys()))

        return namespace
