from .jsonld_eq import jsonld_strict_eq

def test_lddispatch():
  from .lddispatch import lddispatch

  @lddispatch
  def test(ld):
    return ld

  @test.register({
    '@type': 'test'
  })
  def _(ld):
    return dict(ld, **{
      'hello': 'world'
    })

  @test.register({
    'hello': 'world'
  })
  def _(ld):
    return dict(ld, **{
      'goodbye': 'world'
    })

  result = test({'@id': 'example', '@type': 'test'})
  expectation = [{'@id': 'example', '@type': ['test'], 'hello': ['world']}]
  assert jsonld_strict_eq(result, expectation), result

  result = test(result)
  expectation = [{'@id': 'example', '@type': ['test'], 'hello': ['world'], 'goodbye': ['world']}]
  assert jsonld_strict_eq(result, expectation), result

  result = test(result)
  expectation = [{'@id': 'example', '@type': ['test'], 'hello': ['world'], 'goodbye': ['world']}]
  assert jsonld_strict_eq(result, expectation), result
