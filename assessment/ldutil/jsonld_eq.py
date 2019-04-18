import logging
from ..util.multidispatch import multidispatch
from .jsonld_tripleset import jsonld_to_tripleset

@multidispatch()
def jsonld_strict_eq(A, B, verbose=False):
  if type(A) != type(B):
    if verbose:
      logging.debug('type({}) != type({})'.format(A, B))
    return False
  elif A != B:
    if verbose:
      logging.debug('{} != {}'.format(A, B))
    return False
  if verbose:
    logging.debug('{} == {}'.format(A, B))
  return True

@jsonld_strict_eq.register(dict, dict)
def _(A, B, verbose=False):
  if set(A.keys()) != set(B.keys()):
    if verbose:
      logging.debug('set({}.keys()) != set({}.keys())'.format(A, B))
    return False
  if not all(jsonld_strict_eq(A[k], B[k], verbose=verbose) for k in A.keys()):
    return False
  if verbose:
    logging.debug('{} == {}'.format(A, B))
  return True

@jsonld_strict_eq.register(list, list)
def _(A, B, verbose=False):
  if len(A) != len(B):
    if verbose:
      logging.debug('len({}) != len({})'.format(A, B))
    return False
  if not all(
    any(
      jsonld_strict_eq(a, b, verbose=verbose)
      for b in B
    )
    for a in A
  ):
    if verbose:
      logging.debug('set({}) != set({})'.format(A, B))
    return False
  if verbose:
    logging.debug('{} == {}'.format(A, B))
  return True

def jsonld_eq(A, B):
  result = jsonld_to_tripleset(A) == jsonld_to_tripleset(B)
  logging.debug('json_eq({}, {}) => {}'.format(A, B, result))
  return result
