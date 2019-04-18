import logging
from typing import Dict, List, Optional, Tuple

from ..ldutil import (JSONLD, JSONLDFrame, jsonld_deep_map, jsonld_eq,
                      jsonld_flat, jsonld_frame)
from ..util.promise import Promise
from .rule import Rule

def fact_generation(rule: Rule, framed: JSONLD) -> JSONLD:
  promise = rule.resolve(framed)
  result = jsonld_deep_map(
    rule.implies,
    apply=lambda path, obj: str(promise[path]) if type(obj) == dict else obj
  )
  logging.debug('fact_generation({}, {}) => {}'.format(rule, framed, result))
  return result

def fact_resolution(ld: JSONLD):
  result = jsonld_deep_map(ld, apply=lambda path, obj: Promise.resolve(obj))
  logging.debug('fact_resolution({}) => {}'.format(ld, result))
  return result

def forward_chaining(facts: List[JSONLD], goal: Optional[JSONLDFrame] = None, rules: Optional[Dict[str, Rule]] = None, maxdepth=10):
  if rules is None:
    rules = Rule.all().values()

  current_facts = jsonld_flat(facts)
  depth = 0
  while True:
    logging.debug('depth {}: {}'.format(depth, current_facts))
    # if there is a goal, can we satisfy it with our current facts?
    if goal is not None:
      result = jsonld_frame(current_facts, goal)
      if result:
        return {
          'result': fact_resolution(result),
          'graph': current_facts,
          'depth': depth,
          'error': None,
        }

    # can we draw new conclusions given our current set of facts?
    previous_facts = jsonld_flat(current_facts)
    for rule in rules:
      framed = jsonld_frame(current_facts, rule.premise)
      for frame in framed:
        current_facts += [fact_generation(rule, frame)]
    current_facts = jsonld_flat(current_facts)
    if jsonld_eq(current_facts, previous_facts):
      return {
        'result': None,
        'graph': current_facts,
        'depth': depth - 1,
        'error': 'no progress made' if goal is not None else None,
      }

    # ensure we don't exceed some max depth
    if depth >= maxdepth:
      return {
        'result': None,
        'graph': current_facts,
        'depth': depth,
        'error': 'max depth reached',
      }
    depth += 1
