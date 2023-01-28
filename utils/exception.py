class CustomException(Exception):
    status_code = 500
    error_code = 0
    error_message = 'Internal Server Error'


class BadRequest(CustomException):
    status_code = 400
    error_code = 100
    error_message = 'Bad request'


class BadValidationRequest(BadRequest):
    error_message = 'Need to validate config version'


class Error(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

    def __str__(self):
        return "Error: " + self.message

