import os
from ..core import promise, rule

_context = {
  '@vocab': 'https://schema.org/',
  'fairsharing': 'https://fairsharing.org/',
  'fairshake': 'https://fairshake.cloud/metrics/',
  'doi': 'fairsharing:bsg-s001182',
  'indexed': 'fairsharing:bsg-s001346',
  'license': 'fairsharing:bsg-s001353',
  'taxonomy': 'fairshake:101',
  'domain': 'fairshake:102',
}

@promise
def ask_fairsharing(doi):
  from pyswaggerclient import SwaggerClient
  client = SwaggerClient(
    'https://fairsharing.org/api/?format=openapi',
    headers={ 'Api-Key': os.environ.get('FAIRSHARING_API_KEY') }
  )
  results = client.actions.database_summary_list.call(doi=doi)['results']

  return {
    'keywords': list(filter(None, [
      result.get('user_defined_tags')
      for result in results
    ])),
    'doi': list(filter(None, [
      result.get('doi')
      for result in results
    ])),
    'name': list(filter(None, [
      result.get('name')
      for result in results
    ])),
    'description': list(filter(None, [
      result.get('description')
      for result in results
    ])),
    'indexed': list(filter(None, [
      ('https://fairsharing.org/' + result['bsg_id']) if result.get('bsg_id') else None
      for result in results
    ])),
    'url': list(filter(None, [
      result.get('homepage')
      for result in results
    ])),
    'license': list(filter(None, [
      result.get('licence')
      for result in results
    ])),
    'taxonomy': list(filter(None, [
      result.get('taxonomies')
      for result in results
    ])),
    'domain': list(filter(None, [
      result.get('domains')
      for result in results
    ])),
  }

@rule({
  '@context': _context,
  '@id': {},
  'doi': {},
})
def fairsharing_resolver(ld):
  if not os.environ.get('FAIRSHARING_API_KEY'):
    return {}
  resolved = ask_fairsharing(ld['doi'])
  return dict(ld, **{
    'keywords': resolved['keywords'],
    'name': resolved['name'],
    'description': resolved['description'],
    'indexed': resolved['indexed'],
    'homepage': resolved['homepage'],
    'license': resolved['license'],
    'taxonomy': resolved['taxonomy'],
    'domain': resolved['domain'],
  })
