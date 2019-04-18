from .term import Term
from .jsonld_eq import jsonld_strict_eq

def test_jsonld_to_tripleset():
  from .jsonld_tripleset import jsonld_to_tripleset
  case = {
    '@id': 'https://example.com/a',
    'https://example.com/b': {
      '@id': 'https://example.com/c',
      'https://example.com/d': 'e',
      'https://example.com/f': [
        {
          '@id': 'https://example.com/g',
          'https://example.com/h': 'i'
        },
        'j'
      ],
    }
  }
  result = jsonld_to_tripleset(case)
  expectation = frozenset([
    (Term('https://example.com/a'), Term('https://example.com/b'), Term('https://example.com/c')),
    (Term('https://example.com/c'), Term('https://example.com/d'), Term('e', type='literal', datatype='https://www.w3.org/2001/XMLSchema#string')),
    (Term('https://example.com/c'), Term('https://example.com/f'), Term('https://example.com/g')),
    (Term('https://example.com/c'), Term('https://example.com/f'), Term('j', type='literal', datatype='https://www.w3.org/2001/XMLSchema#string')),
    (Term('https://example.com/g'), Term('https://example.com/h'), Term('i', type='literal', datatype='https://www.w3.org/2001/XMLSchema#string')),
  ])

  assert result == expectation, result.difference(expectation)

def test_tripleset_to_jsonld_flat():
  from .jsonld_tripleset import tripleset_to_jsonld_flat
  case = frozenset([
    (Term('https://example.com/a'), Term('https://example.com/b'), Term('https://example.com/c')),
    (Term('https://example.com/c'), Term('https://example.com/d'), Term('e', type='literal', datatype='https://www.w3.org/2001/XMLSchema#string')),
    (Term('https://example.com/c'), Term('https://example.com/f'), Term('https://example.com/g')),
    (Term('https://example.com/c'), Term('https://example.com/f'), Term('j', type='literal', datatype='https://www.w3.org/2001/XMLSchema#string')),
    (Term('https://example.com/g'), Term('https://example.com/h'), Term('i', type='literal', datatype='https://www.w3.org/2001/XMLSchema#string')),
  ])
  result = tripleset_to_jsonld_flat(case)
  expectation = [
    {
      '@id': 'https://example.com/a',
      'https://example.com/b': [
        { '@id': 'https://example.com/c' }
      ],
    },
    {
      '@id': 'https://example.com/c',
      'https://example.com/d': [ 'e' ],
      'https://example.com/f': [
        { '@id': 'https://example.com/g', },
        'j'
      ],
    },
    {
      '@id': 'https://example.com/g',
      'https://example.com/h': [ 'i' ]
    },
  ]

  assert jsonld_strict_eq(result, expectation, verbose=True), result

def test_tripleset_to_jsonld_compact():
  from .jsonld_tripleset import tripleset_to_jsonld_compact
  case = frozenset([
    (Term('https://example.com/a'), Term('https://example.com/b'), Term('https://example.com/c')),
    (Term('https://example.com/c'), Term('https://example.com/d'), Term('e', type='literal', datatype='https://www.w3.org/2001/XMLSchema#string')),
    (Term('https://example.com/c'), Term('https://example.com/f'), Term('https://example.com/g')),
    (Term('https://example.com/c'), Term('https://example.com/f'), Term('j', type='literal', datatype='https://www.w3.org/2001/XMLSchema#string')),
    (Term('https://example.com/g'), Term('https://example.com/h'), Term('i', type='literal', datatype='https://www.w3.org/2001/XMLSchema#string')),
  ])
  result = tripleset_to_jsonld_compact(case, 'https://example.com/a')
  expectation = {
    '@id': 'https://example.com/a',
    'https://example.com/b': [{
      '@id': 'https://example.com/c',
      'https://example.com/d': ['e'],
      'https://example.com/f': [
        {
          '@id': 'https://example.com/g',
          'https://example.com/h': ['i'],
        },
        'j'
      ],
    }]
  }

  assert jsonld_strict_eq(result, expectation, verbose=True), result
