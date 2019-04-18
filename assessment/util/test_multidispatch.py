def test_single_multidispatch():
  from .multidispatch import multidispatch
  @multidispatch()
  def my_multi_func(A, D=None):
    return 0

  @my_multi_func.register(list)
  def _(A, D=None):
    return sum(map(my_multi_func, A))

  @my_multi_func.register(str)
  def _(A, D=None):
    return int(A)

  @my_multi_func.register(int)
  @my_multi_func.register(float)
  def _(A, D=None):
    return A

  assert my_multi_func('6') == 6
  assert my_multi_func(['6', 6]) == 12

def test_multidispatch():
  from .multidispatch import multidispatch

  @multidispatch()
  def my_multi_func(A, B, C, D=None, E=None):
    return 0
  
  @my_multi_func.register(int, int, int)
  @my_multi_func.register(float, float, float)
  def _(A, B, C, D=0, E=0):
    return A + B + C + D + E

  @my_multi_func.register(bool, bool, bool)
  def _(A, B, C, D=True, E=True):
    return A and B and C and D and E

  assert my_multi_func('a', 'b', 'c') == 0
  assert my_multi_func(1, 2, 3) == 6
  assert my_multi_func(1.5, 2., 3.5) == 7.
  assert my_multi_func(True, True, False) == False
  assert my_multi_func(True, 1, False) == 0

def test_multidispatch_type():
  from .multidispatch import multidispatch

  class typeof:
    def __init__(self, typ):
      self._type = typ
    
    def __repr__(self):
      return 'typeof<{}>'.format(self._type)

    def __hash__(self):
      return hash(self._type)
    
    def __eq__(self, other):
      return hash(self) == hash(other)

  def typeof_func(v):
    if isinstance(v, typeof):
      return v
    return type(v)

  @multidispatch(typeof_func)
  def test(inp, outtype):
    print('types not recognized', typeof_func(inp), typeof_func(outtype))

  @test.register(int, typeof(str))
  @test.register(float, typeof(str))
  def _(inp, outtype):
    return str(inp)

  @test.register(str, typeof(int))
  def _(inp, outtype):
    return int(inp)

  @test.register(str, typeof(float))
  def _(inp, outtype):
    return float(inp)

  assert test('6.7', typeof(float)) == 6.7
  assert test(6.7, typeof(str)) == '6.7'
