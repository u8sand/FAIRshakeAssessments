from .cache import Cache
from .types import JSONLDFrame, JSONLD
from .promise import Promise

from .rule import Rule, RuleType
from typing import Callable, Optional, List

from .expansion import expand, deep_expand
from .ld import LD
import logging

def rule(frame: JSONLDFrame, kind: RuleType = RuleType.during):
  def wrapper(recipe: Callable[[JSONLD], JSONLD]) -> Rule:
    rule = Rule(frame=frame, recipe=recipe)
    with Cache['rules']:
      Cache[kind].additem(rule)
    return rule
  return wrapper

def deep_promise_resolution(obj):
  ''' TODO: make this not recursive?
  '''
  if isinstance(obj, dict):
    return {
      k: deep_promise_resolution(v)
      for k, v in obj.items()
    }
  elif isinstance(obj, list):
    return [
      deep_promise_resolution(v)
      for v in obj
    ]
  elif isinstance(obj, str):
    return Promise.resolve(obj)
  else:
    return obj

def process(
  start: JSONLD,
  goal: JSONLDFrame,
  before: Optional[List[Rule]] = None,
  during: Optional[List[Rule]] = None,
  after: Optional[List[Rule]] = None,
):
  ''' Process JSONLD from start to finish using before, during and after rules.
  These will default to the rules registered via `set_global` if None. To make
  empty provide an empty list.
  '''
  # Get rules from cache if not specified
  with Cache['rules']:
    if before is None:
      before = Cache[RuleType.before].get().values()
    if during is None:
      during = Cache[RuleType.during].get().values()
    if after is None:
      after = Cache[RuleType.after].get().values()

  # expand any before rules
  ld = expand(start, before)
  logging.info('pre:deep_expansion ' + str(ld))
  # completely expand during rules
  ld = deep_expand(ld, during)
  logging.info('post:deep_expansion ' + str(ld))
  # prune everything, only get goal
  ld = LD.from_jsonld(ld).frame(goal)
  logging.info('post:frame ' + str(ld))
  # expand after rules
  ld = expand(ld, after)
  logging.info('pre:final_frame ' + str(ld))
  # finalize goal frame
  ld = LD.from_jsonld(ld).frame(goal)

  return deep_promise_resolution(ld)
