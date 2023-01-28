from flask_restful import Api
from werkzeug.exceptions import HTTPException, BadRequest, BadRequestKeyError

from . import logger
from exception import CustomException, BadRequest as CustomBadRequest


class CustomApi(Api):
    def handle_error(self, e):
        if isinstance(e, CustomException):
            return self.make_response({'error': {'code': e.error_code, 'message': e.error_message}}, e.status_code)
        elif isinstance(e, (BadRequest, BadRequestKeyError)):
            message_data = getattr(e, 'data', {
                'error': {
                    'code': CustomBadRequest.error_code,
                    'message': getattr(e, 'description', CustomBadRequest.error_message)
                }
            })

            return self.make_response(message_data, e.code)
        elif not isinstance(e, HTTPException):
            logger.error(repr(e), exc_info=1)
            return self.make_response({
                'error': {
                    'code': CustomException.error_code,
                    'message': CustomException.error_message
                }
            }, CustomException.status_code)
        else:
            return super().handle_error(e)
