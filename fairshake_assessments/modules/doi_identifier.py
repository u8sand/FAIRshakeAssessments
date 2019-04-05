import re
from ..core import promise, rule

# TODO: Note that the better way to do this is via some ontological inference mechanism
#       which resolves the same value; but for now DOI is the primary thing which will
#       probably be all over the place but is necessary to be present in a single place.

_context = {
  '@vocab': 'https://schema.org/',
  'fairsharing': 'https://fairsharing.org/',
  'doi': 'fairsharing:bsg-s001182',
}

_doi_re = re.compile(r'^(https?://([^\.]+)?\.doi.org/|doi:)(?P<doi>.+)$')
@promise
def resolve_doi(val):
  m = _doi_re.match(val)
  if m:
    return { 'doi': m.group('doi') }
  else:
    return {}

@rule({
  '@context': _context,
  '@id': {},
  'url': {},
})
def doi_resolver(ld):
  return dict(ld, **{
    'doi': str(resolve_doi(ld['url'])),
  })

@rule({
  '@context': _context,
  '@id': {}
})
def doi_id_converter(ld):
  return dict(ld, **{
    'doi': str(resolve_doi(ld['@id'])),
  })

@rule({
  '@context': _context,
  '@id': {},
  'identifier': {}
})
def doi_identifier_converter(ld):
  return dict(ld, **{
    'doi': str(resolve_doi(ld['identifier'])),
  })

@rule({
  '@context': _context,
  '@id': {},
  'identifier': {
    '@type': 'PropertyValue',
    'propertyID': 'doi',
    'value': {},
  },
})
def doi_identifier_property_value_converter(ld):
  return dict(ld, **{
    'doi': str(resolve_doi(ld['identifier']['value'])),
  })
