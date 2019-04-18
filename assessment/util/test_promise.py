def test_promise():
  from .promise import Promise

  def testfunc(c):
    return {
      'a': {
        'b': c
      }
    }
  p1 = Promise.create('test1', testfunc, 'c')
  p2 = Promise.create('test1', testfunc, 'd')
  p3 = Promise.create('test1', testfunc, 'c')
  p4 = Promise.create('test1', testfunc, p2['a'])

  assert p1 is p3
  
  assert p1['a']() == { 'b': 'c' }
  assert p2['a']['b']() == 'd'
  assert p3()['a']['b'] == 'c'
  assert p3[['a', 'b']]() == 'c'

  assert Promise.resolve(str(p2['a'])) == { 'b': 'd' }, Promise.resolve(str(p2['a']))
  assert p4['a']['b']() == { 'b': 'd' }, p4['a']['b']()

  assert next(iter(p4.depends())) == p2['a'], list(p4.depends())
