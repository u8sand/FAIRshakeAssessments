from unittest import TestCase
from .ld import LD

_context = 'https://example.com/'

class LDTest(TestCase):
  def test_ld_union(self):
    if not (
      LD.union([
        LD.from_jsonld({
          '@id': '1',
          _context + 'hello': 'world',
        }),
        LD.from_jsonld({
          '@id': '1',
          _context + 'goodbye': 'world',
        })
      ]) == LD.from_jsonld({
        '@id': '1',
        _context + 'hello': 'world',
        _context + 'goodbye': 'world',
      })
    ):
      self.fail('result did not meet expectation')
