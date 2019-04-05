from ...core import promise, rule

_context = {
  '@vocab': 'https://schema.org/',
  'fairshake': 'https://fairshake.cloud/',
}

@promise
def perform_assessment(target = None, rubric = None, project = None):
  target = LDPromise.resolve(target['@id'])
  rubric = LDPromise.resolve(rubric['@id'])
  if project is not None:
    project = LDPromise.resolve(project['@id'])
  # TODO: use rubric to create assessment
  # e.g. rubric has metrics, metrics identify semantics
  # assert that the semantic is present in the ld

@rule({
  '@context': _context,
  '@id': {},
  'fairshake:digital_object': {
    '@type': 'fairshake:digital_object',
  },
  'fairshake:assessment': {
    '@type': 'fairshake:assessment',
    'fairshake:rubric': {},
    'fairshake:project': { "@default": None },
  }
})
def fairshake_assessment(ld):
  resolved = perform_assessment(
    target=ld['fairshake:digital_object'],
    rubric=ld['fairshake:assessment']['fairshake:rubric'],
    project=ld['fairshake:assessment']['fairshake:project']
  )
  return dict(ld, **{
    'fairshake:assessment': {
      '@type': 'fairshake:assessment',
      '@value': str(resolved),
    }
  })
