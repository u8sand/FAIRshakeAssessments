from functools import singledispatch

@singledispatch
def morehash(obj):
  ''' Simple hash extension for sanely hashing unhashable objects.
  '''
  try:
    # Try a normal hash
    return hash(obj)
  except:
    # If it's iterable, try morehashing all its members
    iter(obj)
    return hash(tuple(map(morehash, obj)))

@morehash.register(dict)
def _(obj):
  # A dict's iterable should have both keys AND values
  return morehash(obj.items())
