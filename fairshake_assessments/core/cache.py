from typing import Callable, Hashable, Dict, Optional, Any

class MetaCache(type):
  def __getattribute__(cls, attr):
    ''' Use the current cache when static methods are accessed.
    '''
    if not attr.startswith('_'):
      return cls._current[-1].__getattribute__(attr)
    return super().__getattribute__(attr)

  def __getitem__(cls, ns):
    ''' Cache namespace; enables the following:
    Cache['hello'].setitem('hi', 'world')
    Cache['hello'].getitem('hi')

    By storing a cache in the cache under the ns name.
    '''
    return cls._current[-1][ns]

class Cache(object, metaclass=MetaCache):
  ''' Cache with context support.
  All staticmethods within `with` will operate on
   the given cache. This makes it easy to modify
   the cache being used without bothering the implementation
   of anything which uses it.

  Usage:
  ```
  with Cache():
    Cache.setitem('a', 'b')
    Cache.get()
  ```
  '''
  def __init__(self):
    self._cache: Dict[Hashable, Any] = {}

  def get(self) -> Any:
    return self._cache

  def getitem(self, name: Hashable, default: Any = None) -> Any:
    return self._cache.get(name, default)

  def __getitem__(self, ns: Hashable):
    item = self.getitem(ns)
    if item is None:
      item = Cache()
      self.setitem(ns, item)
    return item

  def additem(self, value: Any) -> None:
    self._cache[str(id(value))] = value

  def register(self) -> Callable[[Any], Any]:
    def wrapper(value: Any) -> Any:
      self.additem(value)
      return value
    return wrapper

  def setitem(self, name: Hashable, value: Any) -> None:
    self._cache[name] = value

  def registeritem(self, name: Hashable) -> Callable[[Any], Any]:
    def wrapper(value: Any) -> Any:
      self.setitem(name, value)
      return value
    return wrapper

  def clearitem(self, name: Hashable) -> None:
    del self._cache[name]

  def clear(self) -> None:
    self._cache = {}

  def __enter__(self):
    ''' push current cache to the global context stack '''
    Cache._current.append(self)
    return self
  
  def __exit__(self, type, value, traceback):
    ''' pop current cache off the global context stack '''
    assert Cache._current.pop(-1) == self

# cache context stack, defaults to a global cache
Cache._current = [Cache()]
