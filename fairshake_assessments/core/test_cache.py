from unittest import TestCase
from .cache import Cache

class CacheTest(TestCase):
  def test_cache(self):
    c = Cache()
    self.assertIsNone(c.getitem('hello'))
    c.setitem('hello', 'world')
    self.assertEqual(c.getitem('hello'), 'world')
    c.setitem('goodbye', 'world')
    c.clearitem('hello')
    self.assertNotIn('hello', c.get())
    self.assertIn('goodbye', c.get())

  def test_cache_ctx(self):
    with Cache():
      Cache.setitem('hi', 'okay')
      with Cache():
        self.assertIsNone(Cache.getitem('hello'))
        Cache.setitem('hello', 'world')
        self.assertEqual(Cache.getitem('hello'), 'world')
        Cache.setitem('goodbye', 'world')
        Cache.clearitem('hello')
        self.assertNotIn('hello', Cache.get())
        self.assertIn('goodbye', Cache.get())
        self.assertIsNone(Cache.getitem('hi'))
      self.assertEqual(Cache.getitem('hi'), 'okay')

  def test_cache_ns(self):
    with Cache():
      with Cache['test']:
        Cache['okay'].setitem('hello', 'world')
      self.assertIsNone(Cache.getitem('hello'))
      self.assertEqual(Cache['test']['okay'].getitem('hello'), 'world')
