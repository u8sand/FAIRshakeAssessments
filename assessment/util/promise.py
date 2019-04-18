import hashlib
from functools import singledispatch
from typing import NewType, Generic, TypeVar, Callable
from urllib.parse import quote, unquote
from .cache import Cache

T = TypeVar('T')

class PromiseTree(Generic[T]):
  def __init__(self, parent, predicate):
    self._parent = parent
    self._predicate = predicate

  def root(self):
    return self if self._parent is None else self._parent.root()

  def __eq__(self, other):
    return all([
      type(self) == type(other),
      self._parent == other._parent,
      self._predicate == other._predicate,
    ])

  def __call__(self):
    return self._parent()[unquote(self._predicate)]

  def __str__(self):
    return str(self._parent) + '/' + quote(self._predicate, safe='')

  def __repr__(self):
    return repr(self._parent) + '/' + quote(self._predicate, safe='')

  def __getitem__(self, predicate):
    if type(predicate) == tuple or type(predicate) == list:
      promise = self
      for pred in predicate:
        promise = PromiseTree(promise, pred)
      return promise
    elif type(predicate) == str:
      return PromiseTree(self, predicate)
    else:
      assert False, 'Unrecognized predicate access type'

class Promise(PromiseTree, Generic[T]):
  _cache_prefix = 'promises'
  _uri_prefix = 'promise://'

  def __init__(self, id, func, *args, **kwargs):
    PromiseTree.__init__(self, None, None)

    self._id = id
    self._func = func
    self._args = args
    self._kwargs = kwargs
    self._uid = Promise.uid(self._id, self._args, self._kwargs)

  def __eq__(self, other):
    return all([
      type(self) == type(other),
      self._uid == other._uid,
    ])

  def __call__(self):
    try:
      return self._resolved
    except:
      args, kwargs = Promise.resolve(self._args), Promise.resolve(self._kwargs)
      self._resolved = self._func(*args, **kwargs)
      return self._resolved

  def __str__(self):
    return Promise._uri_prefix + self._uid

  def __repr__(self):
    return 'Promise[{}({}, {})]'.format(self._id, self._args, self._kwargs)

  def depends(self):
    ''' Identify promises this promise depends on
    '''
    Q = [self._args, self._kwargs]
    while Q != []:
      q = Q.pop()
      if type(q) == dict:
        for k, v in q.items():
          Q += [k, v]
      elif type(q) == list:
        Q += q
      elif type(q) == tuple:
        Q += list(q)
      else:
        promise = Promise.find(q)
        if promise is not None:
          yield promise

  @staticmethod
  def uid(id, args, kwargs):
    return hashlib.sha1(str((id, args, kwargs)).encode()).hexdigest()

  @staticmethod
  def create(id, func: Callable[..., T], *args, **kwargs) -> 'Promise[T]':
    uid = Promise.uid(id, args, kwargs)
    promise = Cache[Promise._cache_prefix].getitem(uid)
    if promise is None:
      promise = Promise(id, func, *args, **kwargs)
      Cache[Promise._cache_prefix].setitem(uid, promise)
    return promise

  @staticmethod
  def find(uri) -> 'Promise[T]':
    if isinstance(uri, Promise) or isinstance(uri, PromiseTree):
      return uri
    elif not (type(uri) == str and uri.startswith(Promise._uri_prefix)):
      return None
    else:
      path = uri[len(Promise._uri_prefix):].split('/', maxsplit=1)
      uid = path.pop(0)
      promise = Cache[Promise._cache_prefix].getitem(uid)
      return promise[path] if path else promise

  @singledispatch
  def resolve(obj, collapse=True):
    promise = Promise.find(obj)
    if promise is not None:
      return promise()
    else:
      return obj

  @resolve.register(list)
  def _(obj, collapse=True):
    results = []
    for v in obj:
      vv = Promise.resolve(v, collapse=collapse)
      if type(vv) == list and collapse:
        results += vv
      else:
        results += [vv]
    return results

  @resolve.register(tuple)
  def _(obj, collapse=True):
    return tuple(Promise.resolve(v, collapse=collapse) for v in obj)

  @resolve.register(dict)
  def _(obj, collapse=True):
    return {
      Promise.resolve(k, collapse=collapse): Promise.resolve(v, collapse=collapse)
      for k, v in obj.items()
    }
