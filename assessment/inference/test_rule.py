def test_rule():
  from .rule import Rule
  from ..util.promise import Promise
  from ..util.cache import Cache

  with Cache():
    @Rule.create('a', { 'url': {} }, { 'name': {}, 'desc': {} })
    def my_rule(ld):
      Cache.setitem('counter', Cache.getitem('counter', 0) + 1)
      return {
        'name': ld['url'] + '!',
        'desc': ld['url'] + '.',
      }

    resolved1 = my_rule.resolve({ 'url': 'hello' })
    resolved2 = my_rule.resolve({ 'url': 'world' })
    resolved3 = my_rule.resolve({ 'url': 'hello' })

    assert isinstance(my_rule, Rule)
    assert isinstance(resolved1, Promise)
    assert isinstance(resolved2, Promise)
    assert resolved1 is resolved3, 'Duplicate promises did not resolve the same object'
    assert Cache.getitem('counter', 0) == 0, 'Promise was evaluated before required'

    assert resolved1['name']() == 'hello!'
    assert Promise.resolve(resolved2['desc']) == 'world.'
    assert Cache.getitem('counter', 0) == 2, 'Rule executed more times than necessary'
