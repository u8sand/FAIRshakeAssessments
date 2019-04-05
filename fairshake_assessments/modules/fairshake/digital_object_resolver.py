import os
from ...core import promise, rule

_context = {
  '@vocab': 'https://schema.org/',
  'fairshake': 'https://fairshake.cloud/',
  'rubrics': 'fairshake:rubrics',
  'authors': 'fairshake:authors',
  'projects': 'fairshake:projects',
}

def get_fairshake_client(api_key=None, username=None, email=None, password=None):
  ''' Using either the api_key directly, or with fairshake
  user credentials, create an authenticated swagger client to fairshake.
  '''
  from pyswaggerclient import SwaggerClient
  fairshake = SwaggerClient(
    'https://fairshake.cloud/swagger?format=openapi',
  )
  if not api_key:
    fairshake_auth = fairshake.actions.auth_login_create.call(data=dict({
      'username': username,
      'password': password,
    }, **({'email': email} if email else {})))
    api_key = fairshake_auth['key']
  # FAIRshake expects a Token in the Authorization request header for
  #  authenticated calls
  fairshake.update(
    headers={
      'Authorization': 'Token ' + api_key,
    }
  )
  return fairshake

@promise
def resolve_fairshake_digital_object(url, name=None, description=None, image=None, keywords=None):
  client = get_fairshake_client(
    api_key=os.environ.get('FAIRSHAKE_API_KEY'),
    email=os.environ.get('FAIRSHAKE_EMAIL'),
    username=os.environ.get('FAIRSHAKE_USERNAME'),
    password=os.environ.get('FAIRSHAKE_PASSWORD'),
  )
  def _generate():
    results = client.actions.digital_object_list.call(url=url)['results']
    for result in results:
      yield {
        '@type': 'fairshake:digital_object',
        '@id': 'https://fairshake.cloud/digital_object/' + result['id'],
        'url': result['url'].split('\n'),
        'name': result['title'],
        'description': result['description'],
        'keywords': result['tags'],
        'rubrics': result['rubrics'],
        'authors': result['authors'],
        'projects': result['projects'],
      }
  objs = list(_generate())
  if len(objs) == 0:
    result = fairshake.actions.digital_object_create.call(data={
      'url': url,
      'title': LDPromise.resolve(ld['name']),
      'description': LDPromise.resolve(ld['description']),
      'image': LDPromise.resolve(ld['image']),
      'tags': LDPromise.resolve(ld['keywords']),
    })
    return {
      '@type': 'fairshake:digital_object',
      '@id': 'https://fairshake.cloud/digital_object/' + result['id'],
      'url': result['url'].split('\n'),
      'name': result['title'],
      'description': result['description'],
      'image': result['image'],
      'keywords': result['tags'],
      'rubrics': result['rubrics'],
      'authors': result['authors'],
      'projects': result['projects'],
    }
  return objs

@rule({
  '@context': _context,
  '@id': {},
  'url': {},
  'name': { "@default": None },
  'description': { "@default": None },
  'image': { "@default": None },
  'keywords': { "@default": None },
})
def fairshake_digital_object_resolver(ld):
  if not (os.environ.get('FAIRSHAKE_API_KEY') or (os.environ.get('FAIRSHAKE_USERNAME') and os.environ.get('FAIRSHAKE_PASSWORD'))):
    return {}

  resolved = resolve_fairshake_digital_object(ld['url'],
    name=ld['name'],
    description=ld['description'],
    image=ld['image'],
    keywords=ld['keywords'],
  )
  return dict(ld, **{
    'fairshake:digital_object': {
      '@id': resolved['id'],
      '@type': 'fairshake:digital_object',
      'name': resolved['title'],
      'description': resolved['description'],
      'image': resolved['image'],
      'keywords': resolved['tags'],
      'fairshake:rubrics': resolved['rubrics'],
      'fairshake:authors': resolved['authors'],
      'fairshake:projects': resolved['projects'],
    }
  })
