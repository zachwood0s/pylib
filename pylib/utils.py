import functools
import unittest

def require(condition, fail_value=None):
  def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      if condition(*args, **kwargs):
        return func(*args, **kwargs)
      else:
        return fail_value
    return wrapper
  return decorator