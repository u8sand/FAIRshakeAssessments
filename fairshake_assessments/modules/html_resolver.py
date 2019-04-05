from ..core import promise, rule

_context = {
  '@vocab': 'https://schema.org/',
  'fairsharing': 'https://fairsharing.org/',
  'html': 'fairsharing:bsg-s001284',
}

@promise
def resolve_html(url):
  from urllib.request import urlopen
  return urlopen(url).read().decode()

@rule({
  '@context': _context,
  '@type': 'WebSite',
  '@id': {},
  'url': {},
})
def html_resolver(ld):
  return dict(ld, **{
    'html': str(resolve_html(ld['url'])),
  })
