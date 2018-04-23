from rest_framework.exceptions import APIException


class Http422(APIException):
    status_code = 422
    default_detail = 'Invalid data supplied'
    default_code = 'Unprocessable Entity'


class Http400(APIException):
    status_code = 400
    default_detail = 'Bad Request'
    default_code = 'Bad Request'
