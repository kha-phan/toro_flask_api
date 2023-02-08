import hashlib
import io

from flask import send_file
from flask_restful import Resource

from utils import CustomRequestParser


parser = CustomRequestParser()
parser.add_argument('employee_id', type=str, required=True, location='args')


class StoreApi(Resource):
    def get(self):
        return {}, 200
