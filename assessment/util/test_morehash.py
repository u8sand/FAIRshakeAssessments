def assert_reproducable_func(func, val):
  assert func(val) == func(val)

def test_morehash():
  from .morehash import morehash

  assert morehash('a') == hash('a')
  assert_reproducable_func(morehash, [1, 2, 3])
  assert_reproducable_func(morehash, set([1, 2, 3]))
  assert_reproducable_func(morehash, {'a': 'b', 'c': 'd'})
  assert_reproducable_func(morehash, {'a': ['b', {'c': ['d', set(['e', 'f']), {}]}]})
