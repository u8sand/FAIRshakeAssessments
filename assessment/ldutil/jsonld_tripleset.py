import itertools
from toposort import toposort
from .term import Term

_jsonld_datatype_lookup = {
  str: 'https://www.w3.org/2001/XMLSchema#string',
}
def _jsonld_to_tripleset_generate(ld):
  Q = [(None, None, ld)]
  n = iter(itertools.count())

  while Q != []:
    subj, pred, obj = Q.pop()

    if isinstance(obj, dict):
      if obj.get('@id') is not None:
        id = Term(obj['@id'], type='IRI')
      else:
        id = Term('_:%d' % (next(n)), type='blank node')

      if pred is not None:
        yield (subj, pred, id)

      for p, o in obj.items():
        if p == '@id':
          continue
        Q.append((id, Term(p, type='IRI'), o))

    elif isinstance(obj, list):
      for o in obj:
        Q.append((subj, pred, o))

    else:
      if isinstance(obj, Term):
        yield (subj, pred, obj)
      else:
        datatype = _jsonld_datatype_lookup.get(type(obj))
        if datatype is None:
          yield (subj, pred, Term(obj, type='literal'))
        else:
          yield (subj, pred, Term(obj, type='literal', datatype=datatype))


def jsonld_to_tripleset(ld):
  ''' Convert JSONLD to a set of subject, predicate, object triples.
  We convert each part of the triple to preserve extra RDF information.
  '''
  return frozenset(_jsonld_to_tripleset_generate(ld))

def tripleset_to_jsonld_flat(ts):
  ''' Convert a set of subject, predicate, object triples back into Normalized flat JSONLD.
  '''
  T = {}
  for s, p, o in ts:
    if not T.get(s):
      T[s] = { '@id': str(s) }
    if not T[s].get(str(p)):
      T[s][str(p)] = []
    if o.type == 'IRI' or o.type == 'blank node':
      T[s][str(p)].append({ '@id': str(o) })
    else:
      T[s][str(p)].append(str(o))
  return list(T.values())

def tripleset_to_jsonld_compact(ts, root=None):
  ''' Convert a set of subject, predicate, object triples back into JSONLD.
  We resolve and embed dependent nodes in an effort to build a compact structure.

  Essentially this works by the use of toposort followed by construction of the
   tree by using previously created tree elements where applicable.
  '''
  if isinstance(root, list):
    root = set(map(Term, root))
    as_list = True
  elif isinstance(root, str):
    root = set([Term(root)])
    as_list = False
  elif root is not None:
    raise 'Unrecognized root argument type'

  # Setup toposort--each subject depends on the object
  #  at the other side of the predicate.
  D = {}
  for s, p, o in ts:
    if D.get(s) is None:
      D[s] = set()
    D[s].add(o)

  # toposort results in each tree layer
  #  bottom up
  T = {}
  steps = list(toposort(D))

  # build tree (bottom up), using any existing
  #  nodes as children
  for step in steps:
    for s, p, o in ts:
      if s not in step:
        continue
      if T.get(s) is None:
        if s.type == 'IRI':
          T[s] = { '@id': str(s) }
        elif s.type == 'blank node':
          T[s] = {}
      if o.type == 'IRI':
        # Collapse @type
        if str(p) == '@type':
          T[s][str(p)] = T[s].get(str(p), []) + [T.get(o, str(o))]
        else:
          T[s][str(p)] = T[s].get(str(p), []) + [T.get(o, { '@id': str(o) })]
      elif o.type == 'blank node':
        T[s][str(p)] = T[s].get(str(p), []) + [T.get(o, {})]
      else:
        T[s][str(p)] = T[s].get(str(p), []) + [str(o)]

  results = list({
    k: v
    for k, v in T.items()
    if root is None or k in root
  }.values())

  return results if as_list else results[0]
