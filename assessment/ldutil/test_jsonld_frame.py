from .jsonld_eq import jsonld_strict_eq

def test_jsonld_frame_node():
  from .jsonld_frame import jsonld_frame_node
  case = (
    {
      '@id': 'https://example.com/a',
      'https://example.com/b': ['c'],
      'https://example.com/d': [
        'e',
        {
          '@id': 'https://example.com/f',
          'https://example.com/g': 'h',
        }
      ],
      'https://example.com/i': ['j']
    },
    {
      '@explicit': False,
      'https://example.com/d': {
        '@explicit': True,
        'https://example.com/g': 'h',
        'https://example.com/i': {
          '@default': []
        }
      }
    }
  )
  result = jsonld_frame_node(*case)
  expectation = {
    '@id': 'https://example.com/a',
    'https://example.com/b': ['c'],
    'https://example.com/d': [
      'e',
      {
        'https://example.com/g': 'h',
        'https://example.com/i': [],
      }
    ],
    'https://example.com/i': ['j'],
  }

  assert jsonld_strict_eq(result, expectation, verbose=True), result

  case = (
    {
      '@id': 'https://example.com/a',
      'https://example.com/b': ['c'],
      'https://example.com/d': [
        'e',
        {
          '@id': 'https://example.com/f',
          'https://example.com/g': 'h',
        }
      ],
      'https://example.com/i': ['j']
    },
    {
      'https://example.com/d': {
        'https://example.com/g': 'h',
        'https://example.com/i': {}
      }
    }
  )
  result = jsonld_frame_node(*case)
  expectation = None

  assert result == expectation, result


def test_jsonld_frame():
  from .jsonld_frame import jsonld_frame
  case = (
    {
      '@id': 'https://example.com/a',
      '@type': 'https://example.com/b',
      'https://example.com/c': [{
        '@id': 'https://example.com/d',
        '@type': ['https://example.com/b', 'https://example.com/e'],
        'https://example.com/f': [
          {
            '@id': 'https://example.com/g',
            'https://example.com/h': [
              'i',
              {
                '@id': 'https://example.com/j',
                '@type': 'https://example.com/e',
                'https://example.com/k': 'l',
              }
            ],
          },
          'j'
        ],
      }]
    },
    {
      '@explicit': False,
      '@type': 'https://example.com/e',
      'https://example.com/f': {
        '@default': [],
      }
    }
  )
  expectation = [
    {
      '@id': 'https://example.com/d',
      '@type': ['https://example.com/b', 'https://example.com/e'],
      'https://example.com/f': [
          {
            '@id': 'https://example.com/g',
            'https://example.com/h': [
              'i',
              {
                '@id': 'https://example.com/j',
                '@type': ['https://example.com/e'],
                'https://example.com/k': ['l'],
              }
            ],
          },
          'j',
      ],
    },
    {
      '@id': 'https://example.com/j',
      '@type': ['https://example.com/e'],
      'https://example.com/f': [],
      'https://example.com/k': ['l'],
    }
  ]
  result = jsonld_frame(*case)

  assert jsonld_strict_eq(result, expectation, verbose=True), result
