from ..util.multidispatch import multidispatch
from typing import Callable, Tuple, Any

@multidispatch()
def jsonld_deep_map(frame, apply: Callable[[Tuple[str], Any], Any] = None, path = tuple()):
  assert False, 'Uncaught dispatch {} ({})'.format(frame, type(frame))

@jsonld_deep_map.register(dict)
def _(frame, apply=None, path=tuple()):
  frame_preds = set(frame.keys()) - set(['@default', '@explicit'])
  if frame_preds == set():
    return apply(path, frame)
  return {
    pred: jsonld_deep_map(frame[pred], apply=apply, path=(*path, pred,))
    for pred in frame_preds
  }

@jsonld_deep_map.register(list)
def _(frame, apply=None, path=tuple()):
  return [
    jsonld_deep_map(f, apply=apply, path=(*path, None))
    for f in frame
  ]

@jsonld_deep_map.register(str)
@jsonld_deep_map.register(int)
@jsonld_deep_map.register(float)
@jsonld_deep_map.register(type(None))
def _(frame, apply=None, path=tuple()):
  return apply(path, frame)
