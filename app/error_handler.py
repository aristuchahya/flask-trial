from flask import jsonify
from werkzeug.exceptions import HTTPException

class ApiException(HTTPException):
    def __init__(self, message, status_code):
        super().__init__(description=message)
        self.message = message
        self.status_code = status_code
        
def handle_api_exception(e):
    response = jsonify({
        'error' : e.message,
        'status_code' : e.status_code
    })
    response.status_code = e.status_code
    return response

def handle_http_exception(e):
    response = jsonify({
        'error' : e.description,
        'status_code' : e.code
    })
    response.status_code = e.code
    return response

def handle_unexpected_exception(e):
    response = jsonify({
        'error' : 'An unexpected error occurred',
        'status_code' : 500
    })
    response.status_code = 500
    return response