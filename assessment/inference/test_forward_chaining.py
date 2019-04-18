def test_meta_forward_chaining():
  from .forward_chaining import forward_chaining
  from .rule import Rule
  from ..util.cache import Cache
  from ..ldutil import jsonld_eq

  with Cache():
    @Rule.create(
      'rule_1',
      { '@id': {}, 'url': {}, },
      { '@id': {}, 'name': {}, }
    )
    def rule_1(ld):
      return dict(ld, **{
        'name': [url + '!' for url in ld['url']]
      })

    @Rule.create(
      'rule_2',
      { '@id': {}, 'name': {}, },
      { '@id': {}, 'desc': {}, }
    )
    def rule_2(ld):
      return dict(ld, **{
        'desc': [name + '?' for name in ld['name']]
      })

    result = forward_chaining(
      {
        '@id': 'test',
        'url': 'test'
      },
      {
        '@id': {},
        'desc': {}
      }
    )
    expectation = {
      '@id': 'test',
      'desc': 'test!?'
    }

    assert jsonld_eq(result['result'], expectation), result
