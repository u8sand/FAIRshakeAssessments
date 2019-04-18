import json
from functools import wraps, lru_cache

def lru_cache_serializable(maxsize=128, typed=False, serialize=json.dumps, deserialize=json.loads):
  def decorator(func):
    @wraps(func)
    @lru_cache(maxsize=maxsize, typed=typed)
    def cached_func(params):
      args, kwargs = deserialize(params)
      return func(*args, **kwargs)

    @wraps(cached_func)
    def wrapper(*args, **kwargs):
      return cached_func(serialize((args, kwargs)))

    wrapper.cache_info = cached_func.cache_info
    wrapper.cache_clear = cached_func.cache_clear
    return wrapper
  return decorator
