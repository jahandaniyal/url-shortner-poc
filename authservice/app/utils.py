# -*- coding: utf-8 -*-

import re


def sanitize_json_input(func):
    """Decorator for sanitizing JSON data.
    Args:
        func (:function:): decorated function.
    Returns:
        Returns a decorator for sanitizing JSON data.
    Raises:
        ValueError: If JSON is invalid.
    """
    def wrapper(*args, **kwargs):
        try:
            json_string = args[1].body.decode(encoding='latin1')
            json_string = re.sub(r"[\n\t\r]*", "", json_string)
            json_string = re.sub(r",}$", "}", json_string)
            args[1].body = json_string.encode(encoding='latin1')
        except ValueError:
            print("Incorrect JSON data")

        returned_value = func(*args, **kwargs)

        return returned_value
    return wrapper