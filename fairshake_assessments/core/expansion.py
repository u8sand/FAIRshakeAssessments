import logging
import functools
from copy import copy
from typing import List, Iterator, Optional
from .types import JSONLD, JSONLDFrame
from .ld import LD
from .rule import Rule

def frame_matches_framed(frame, framed):
  ''' Check whether a given rule matches a given frame.
  This will occur *after* JSON-LD Framing and is useful for
  ensuring we don't get "None" where things should be values.
  Essentially it makes up for frames working strangely.
  '''
  if type(frame) == dict:
    if '@default' in frame:
      if framed is None:
        framed = {}
      return True
    elif framed is None:
      return False
    for pred, obj in frame.items():
      if pred in [ '@context', '@explicit', '@embed' ]:
        continue
      if not frame_matches_framed(obj, framed.get(pred, {})):
        return False
  elif type(frame) == list:
    if not any(frame_matches_framed(f, framed) for f in frame):
      return False
  else:
    return framed == frame
  return True

def _expand(ld: LD, rules: List[Rule]) -> Iterator[JSONLD]:
  ''' Match rules and return recipe results.
  '''
  logging.info('rules ' + str(rules))
  for frame, recipe in rules:
    framed = ld.frame(frame)
    if '@graph' in framed:
      framed = [
        dict(node, **{ '@context': framed.get('@context', {}) })
        for node in framed['@graph']
      ]
    else:
      framed = [framed]
    logging.info('framed ' + str(framed))
    for node in filter(functools.partial(frame_matches_framed, frame), framed):
      logging.info('framed_node ' + str(node))
      yield recipe(node)

def expand(ld: JSONLD, rules: List[Rule]) -> JSONLD:
  ''' Expand `ld` using `rules`--that-is match rules and integrate
  the recipe results into ld.
  '''
  if not rules:
    return ld

  ld: LD = LD.from_jsonld(ld)
  for node in _expand(ld, rules):
    logging.info('expanded_node ' + str(node))
    ld = ld + LD.from_jsonld(node)
  return ld.to_jsonld()

def deep_expand(ld: JSONLD, rules: List[Rule], max_depth: int = 10) -> JSONLD:
  ''' Expand `ld` using `rules` at most `max_depth` times.
  '''
  if not rules:
    return ld

  ld: LD = LD.from_jsonld(ld)
  while max_depth > 0:
    ld_ = copy(ld)
    for node in map(LD.from_jsonld, _expand(ld, rules)):
      logging.info('expanded_node ' + str(node))
      ld += node
    if ld == ld_:
      break
    max_depth -= 1
  return ld.to_jsonld()
