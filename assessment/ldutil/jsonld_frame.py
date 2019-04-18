import logging
from ..util.multidispatch import multidispatch
from .jsonld_tripleset import jsonld_to_tripleset, tripleset_to_jsonld_compact

def type_or_none(t):
  if t is None:
    return None
  return type(t)

@multidispatch(type_or_none)
def jsonld_frame_node(node, frame, explicit=False):
  ''' Frame a single node, expects both the node and the frame to be compacted (see tripleset_to_jsonld_compact)
  * Blanks nodes are ignored during framing.
  If the node is not a superset of the frame, this will return None (could not be framed).
  If the node **is**, then the node's deep properties will be filtered based on the frame specification.

  @explicit: True | False => whether or not to filter the given object tree (defaults to parent or False)
  e.g.
  Node: { 'a': [{ 'b': ['c'], 'd': ['e'] }], 'b': ['c'] }
  Frame: { '@explicit': True, 'a': { '@explicit': False } }
  Result: { 'a': [{ 'b': ['c'], 'd': ['e'] }] }

  @default: val => a default value for a given parameter, effectively making it optional.
  e.g.
  Node: { 'a': [{ 'b': ['c'] }], 'b': ['c'] }
  Frame: { 'a': [{ 'b': ['c'], 'd': { '@default': [] } }] }
  Result: { 'a': [{ 'b': ['c'], 'd': [] }], 'b': ['c'] }
  if '@default' wasn't here, the missing 'd' would cause a frame mismatch (return None)
  '''
  assert False, 'Dispatch ({}, {}) not caught'.format(type(node), type(frame))

@jsonld_frame_node.register(str, str)
@jsonld_frame_node.register(int, int)
@jsonld_frame_node.register(float, float)
@jsonld_frame_node.register(None, str)
@jsonld_frame_node.register(None, int)
@jsonld_frame_node.register(None, float)
@jsonld_frame_node.register(None, None)
def _(node, frame, explicit=False):
  if node == frame:
    return node
  else:
    return None


@jsonld_frame_node.register(None, dict)
def _(node, frame, explicit=False):
  return frame.get('@default')


@jsonld_frame_node.register(str, dict)
@jsonld_frame_node.register(int, dict)
@jsonld_frame_node.register(float, dict)
def _(node, frame, explicit=False):
  if set(frame.keys()) - set(['@default', '@explicit']) == set():
    return node
  else:
    return None


@jsonld_frame_node.register(str, None)
@jsonld_frame_node.register(int, None)
@jsonld_frame_node.register(float, None)
@jsonld_frame_node.register(dict, None)
@jsonld_frame_node.register(list, None)
def _(node, frame, explicit=False):
  if explicit:
    return None
  else:
    return node


@jsonld_frame_node.register(list, dict)
@jsonld_frame_node.register(list, str)
@jsonld_frame_node.register(list, int)
@jsonld_frame_node.register(list, float)
def _(node, frame, explicit=False):
  framed = {
    i: jsonld_frame_node(n, frame, explicit=explicit)
    for i, n in enumerate(node)
  }
  if all(n is None for n in framed.values()):
    return None
  elif explicit:
    return [
      n
      for n in framed.values()
      if n is not None
    ]
  else:
    return [
      node[i] if n is None else n
      for i, n in framed.items()
    ]

@jsonld_frame_node.register(dict, list)
@jsonld_frame_node.register(str, list)
@jsonld_frame_node.register(int, list)
@jsonld_frame_node.register(float, list)
def _(node, frame, explicit=False):
  framed = list(filter(None, (
    jsonld_frame_node(node, f, explicit=explicit)
    for f in frame
  )))
  if framed == []:
    if frame == []:
      return []
    else:
      return None
  else:
    if frame == []:
      return None
    else:
      return framed


@jsonld_frame_node.register(dict, dict)
def _(node, frame, explicit=False):
  frame_default = frame.get('@default')
  frame_explicit = frame.get('@explicit', explicit)
  if frame_explicit:
    keys = set(frame.keys() - set(['@default', '@explicit']))
  else:
    keys = set(node.keys() | frame.keys() - set(['@default', '@explicit']))

  T = {}
  for pred in keys:
    T[pred] = jsonld_frame_node(node.get(pred), frame.get(pred), explicit=explicit)
    if T[pred] is None:
      if pred in frame:
        return frame_default
      else:
        del T[pred]
  return T

def jsonld_frame(ld, frame):
  ''' Return all compacted root nodes which satisfy a given frame (see jsonld_frame_node)
  '''
  ts = jsonld_to_tripleset(ld)
  logging.debug('jsonld_frame({}) // {}'.format(ts, repr(list(set(str(subj) for subj, _, _ in ts)))))
  return list(
    filter(None,
      map(lambda node, frame=frame: jsonld_frame_node(node, frame),
        tripleset_to_jsonld_compact(
          ts, list(set(str(subj) for subj, _, _ in ts))
        )
      )
    )
  )
