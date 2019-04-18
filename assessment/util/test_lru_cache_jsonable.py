def test_lru_cache_serializable():
  from .lru_cache_serializable import lru_cache_serializable

  @lru_cache_serializable()
  def test(a, b, c=None):
    return a + b
  
  assert test(1, 1) == 2
  assert test(1, 2) == 3
  assert test(1, 1) == 2

  cache_info = test.cache_info()

  assert cache_info.hits == 1
  assert cache_info.misses == 2
