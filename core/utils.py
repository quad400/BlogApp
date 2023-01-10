import uuid
import re
from django.db import models
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.exceptions import APIException




class Exception(Exception):
    message = "An Error Occured"
    code = HTTP_400_BAD_REQUEST

    def __init__(self, message=None, code=None):
        self.message = message or self.message or self.__doc__
        self.code = code or self.code

    def __str__(self):
        if isinstance(self.message, str):
            return self.message
        return ""

    def __dict__(self):
        if isinstance(self.message, dict):
            return self.message
        return {}


def handle_errors():
    """
        Error handler decorator
    """
    def handle_errors(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as error:
                message = error.__dict__() or error.__str__()
                code = getattr(error, "code", HTTP_400_BAD_REQUEST)

                return Response({"error": message}, status=code)
            except APIException as error:
                code = getattr(error, "code", status=HTTP_400_BAD_REQUEST)
                return Response({"error": error}, status=code) 

        return wrapper
    
    return handle_errors


def raise_errors():
    """
        Decorator to raise errors
    """
    def raise_errors(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as error:
                raise error

        return wrapper

    return raise_errors


def remove_none_values(obj):
    """Remove none values from dict/list"""
    if isinstance(obj, dict):
        return {k:remove_none_values(v) for k,v in obj.items() if v is not None}
    elif isinstance(obj, list):
        return [remove_none_values(v) for v in obj if v is not None]
    else:
        return obj


