from unittest import TestCase, mock
from ..core import Recipe, LDPromise, extend
from .jsonld_resolver import html_resolver, _context

def mock_urlopen(url):
  class MockResponse:
    def read():
      return '<html></html>'

  return MockResponse()

class HTMLResolverTest(TestCase):
  @mock.patch('.jsonld_resolver.urllib.request.urlopen', side_effect=mock_urlopen)
  def test_html_resolver(self):
    self.assertDictEqual(
      LDPromise.resolve_all(
        extend({
          '@context': _context,
          '@id': 'https://example.com/test',
          'url': 'https://example.com/'
        })
      ),
      {
        '@context': _context,
        '@id': 'https://example.com/test',
        'url': 'https://example.com/',
        'html': '<html></html>'
      }
    )
