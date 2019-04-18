def test_jsonld_deep_map():
  from .jsonld_deep_map import jsonld_deep_map

  case = {
    '@id': 'test',
    'hello': [
      {
        'world': {
          '@default': 'okay',
        },
      },
      {
        '!': {},
      },
    ],
    'good/bye': {},
  }
  expectation = {
    '@id': 'test',
    'hello': [
      {
        'world': 'hello.world',
      },
      {
        '!': 'hello.!',
      },
    ],
    'good/bye': 'good/bye',
  }
  result = jsonld_deep_map(
    case, apply=lambda path, obj: '.'.join(filter(None, path)) if type(obj) == dict else obj
  )

  assert result == expectation, result
