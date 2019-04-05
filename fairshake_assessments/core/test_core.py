from unittest import TestCase
from .core import rule, process
from .promise import promise, Promise
from .ld import LD
from .cache import Cache

_context = 'https://example.com/'

class TestCore(TestCase):
  def test_core(self):
    with Cache():
      @promise
      def promise_1(val):
        Cache.setitem('counter', Cache.getitem('counter', 0) + 1)
        return val + '!'

      @rule({
        '@context': { '@vocab': _context },
        '@id': {},
        '@type': 'Hello',
      })
      def process_1(ld):
        ret = dict(ld, **{
          'world': str(promise_1(ld['@id'])),
        })
        return ret

      @promise
      def promise_2(val):
        Cache.setitem('counter', Cache.getitem('counter', 0) + 1)
        return val + '!'

      @rule({
        '@context': { '@vocab': _context },
        '@id': {},
        'world': {},
      })
      def process_2(ld):
        return dict(ld, **{
          'hello': str(promise_2(ld['world'])),
        })

      result = process({
        '@context': { '@vocab': _context },
        '@id': _context + '1',
        '@type': 'Hello',
      }, {
        '@context': { '@vocab': _context },
        '@id': _context + '1',
        'world': {},
      })
      expectation = {
        '@context': { '@vocab': _context },
        '@id': _context + '1',
        '@type': 'Hello',
        'world': _context + '1' + '!',
      }

      if not (LD.from_jsonld(result) == LD.from_jsonld(expectation)):
        self.fail(result)

      self.assertEqual(Cache.getitem('counter'), 1, 'Unnecessary promise resolution')
