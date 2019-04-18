from .jsonld_frame import jsonld_frame
from .jsonld_tripleset import jsonld_to_tripleset, tripleset_to_jsonld_flat

class lddispatch:
  def __init__(self, func):
    self._func = func
    self._registry = []

  def __repr__(self):
    return repr('lddispatch<{}>'.format(repr(self._func)))

  def __call__(self, LD, **kwargs):
    ''' Execute the function matching the frame
    '''
    results = set(jsonld_to_tripleset(self._func(LD)))
    for frame, func in self._registry:
      for framed in jsonld_frame(LD, frame):
        results.update(jsonld_to_tripleset(func(framed)))
    return tripleset_to_jsonld_flat(results)

  def register(self, frame):
    ''' Register frame to get dispatched.
    '''
    def decorator(func):
      self._registry.append((frame, func))
      return func
    return decorator
