import logging
from functools import wraps

class _multidispatch:
  ''' This could certainly be better, but this is a simple implementation with some limitations.
  All *args get matched by type for dispatch. **kwargs are passed along but not type-checked.
  '''

  def __init__(self, func, typefunc=type):
    self._func = func
    self._typefunc = typefunc
    self._registry = {}

  def __repr__(self):
    return repr('multidispatch<{}>'.format(repr(self._func)))

  def __call__(self, *args, **kwargs):
    ''' Execute the function matching the *arg types, otherwise fallback to the initial funciton.
    '''
    result = self._registry.get(tuple(map(self._typefunc, args)), self._func)(*args, **kwargs)
    logging.debug('{}({}) => {}'.format(
      self._func.__name__,
      ','.join([
        *map(repr, args),
        *map('='.join, zip(kwargs.keys(), map(repr, kwargs.values()))),
      ]),
      repr(result)
    ))
    return result

  def register(self, *args):
    ''' Register *arg types to get dispatched.
    '''
    def decorator(func):
      self._registry[args] = func
      return func
    return decorator

def multidispatch(typefunc=type):
  @wraps(_multidispatch)
  def wrapper(func):
    return _multidispatch(func, typefunc=typefunc)
  return wrapper
