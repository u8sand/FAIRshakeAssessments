import logging
from ..core import promise, rule

_context = {
  '@vocab': 'https://schema.org/',
  'fairsharing': 'https://fairsharing.org/',
  'html': 'fairsharing:bsg-s001284',
  'json-ld': 'fairsharing:bsg-s001214',
  'microdata': 'https://www.w3.org/TR/microdata-rdf/',
  'opengraph': 'http://ogp.me/ns/',
  'rdfa': 'fairsharing:bsg-s001338',
}

@promise
def resolve_jsonld(html):
  from extruct import extract
  ld = extract(html, syntaxes=['json-ld', 'microdata', 'opengraph', 'rdfa'], uniform=True)
  # TODO: deal with other types that aren't json-ld
  #  by converting them.
  logging.info('!', ld)
  return ld

@rule({
  '@context': _context,
  '@type': 'WebSite',
  '@id': {},
  'html': {},
})
def jsonld_resolver(ld):
  resolved = resolve_jsonld(ld['html'])
  return dict(ld, **{
    'json-ld': resolved['json-ld'],
    'microdata': resolved['microdata'],
    'opengraph': resolved['opengraph'],
    'rdfa': resolved['rdfa'],
  })
