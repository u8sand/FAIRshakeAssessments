def test_jsonld_strict_eq():
  from .jsonld_eq import jsonld_strict_eq
  case = (
    {
      '@id': 'https://example.com/a',
      'https://example.com/b': {
        '@id': 'https://example.com/c',
        'https://example.com/d': 'e',
        'https://example.com/f': [
          'j',
          {
            '@id': 'https://example.com/g',
            'https://example.com/h': 'i'
          },
          'k'
        ],
      }
    },
    {
      '@id': 'https://example.com/a',
      'https://example.com/b': {
        '@id': 'https://example.com/c',
        'https://example.com/d': 'e',
        'https://example.com/f': [
          'k',
          'j',
          {
            '@id': 'https://example.com/g',
            'https://example.com/h': 'i'
          },
        ],
      }
    }
  )
  result = jsonld_strict_eq(*case, verbose=True)
  expectation = True

  assert result == expectation, result
