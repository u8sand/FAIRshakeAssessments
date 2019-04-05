import re
from typing import Callable, Hashable, Any, Tuple, Union
from hashlib import sha1
from .cache import Cache

class Promise:
  _uri_prefix = 'promise://'
  _uri_re = re.compile(r'^(?P<prefix>promise://[^/]+)(/(?P<postfix>.+))?$')

  def __init__(self, uri: str, func: Callable[[Hashable], Any], args: Hashable, _repr: str = None):
    self._uri = uri
    self._func = func
    self._repr = repr(self._func) if _repr is None else _repr
    self._args = args
    self._value = None
  
  def __call__(self) -> Any:
    if self._value is None:
      try:
        self._value = self._func(self._args)
      except Exception as e:
        raise Exception(repr(self) + ' threw an exception') from e
    return self._value

  def resolved(self) -> bool:
    return self._value is not None

  def __repr__(self) -> str:
    return '{uri}[{func}]'.format(uri=self._uri, func=self._repr)

  def __str__(self) -> str:
    return self._uri

  def __getitem__(self, k: str) -> str:
    return self._uri + '/' + k

  @staticmethod
  def _construct_uri(func: Callable[[Hashable], Any], args: Hashable) -> str:
    return '{prefix}{id}'.format(
      prefix=Promise._uri_prefix,
      id=sha1(hex(hash((func, args))).encode()).hexdigest()
    )

  @staticmethod
  def _parse_uri(uri: str) -> Tuple[str, str]:
    ''' @returns prefix, postfix
    '''
    m = Promise._uri_re.match(uri)
    if not m:
      return None, None
    prefix, postfix = m.group('prefix'), m.group('postfix')
    return prefix, postfix

  @staticmethod
  def create(func: Callable[[Hashable], Any], args: Hashable, _repr: str = None) -> 'Promise':
    uri = Promise._construct_uri(func, args)
    promise = Cache['promise'].getitem(uri)
    if promise is None:
      promise = Promise(uri, func, args, _repr=_repr)
      Cache['promise'].setitem(uri, promise)
    return promise

  @staticmethod
  def resolve(uri: Any) -> Union['Promise', Any]:
    if isinstance(uri, Promise):
      promise, postfix = uri, None
    elif isinstance(uri, str):
      prefix, postfix = Promise._parse_uri(uri)
      promise = Cache['promise'].getitem(prefix)
    else:
      promise = None

    if promise is None:
      return uri

    if postfix:
      return promise().get(postfix)
    return promise()

def promise(func: Callable[..., Any]) -> Callable[..., Promise]:
  ''' Decorator to convert a function
  into a function which produces a promise
  for the function call.
  '''
  def back_wrapper(param):
    ''' Called when promise is resolved
    responsible for resolving any promises
    provided as arguments before execution
    '''
    args, kwargs = param
    args = [
      Promise.resolve(v)
      for v in args
    ]
    kwargs = {
      k: Promise.resolve(v)
      for k, v in kwargs
    }
    return func(*args, **kwargs)

  def front_wrapper(*args, **kwargs):
    ''' Function that will be returned
    in place of the user provided function.
    '''
    return Promise.create(
      back_wrapper,
      (args, frozenset(kwargs.items())),
      _repr=repr(func),
    )

  return front_wrapper
