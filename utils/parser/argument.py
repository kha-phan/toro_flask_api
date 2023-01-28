import flask_restful
import six
from flask import current_app
from flask_restful.reqparse import Argument

from ..exception import BadRequest


class CustomArgument(Argument):
    def handle_validation_error(self, error, bundle_errors):
        """ Override to change the abort message

        :param error: the error that was raised
        :param bundle_errors: do not abort when first error occurs, return a
            dict with the name of the argument and the error message to be
            bundled
        """
        error_str = six.text_type(error)
        error_msg = self.help.format(error_msg=error_str) if self.help else error_str
        msg = {self.name: error_msg}

        if current_app.config.get("BUNDLE_ERRORS", False) or bundle_errors:
            return error, msg
        flask_restful.abort(400, error={"code": BadRequest.error_code, "message": f"{self.name}: {error_msg}"})
