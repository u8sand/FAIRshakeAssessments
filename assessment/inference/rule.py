from ..util.promise import Promise
from ..util.cache import Cache
from ..ldutil import JSONLD, JSONLDFrame
from functools import partial
from typing import NamedTuple, Callable

class Rule(NamedTuple):
  _cache_prefix = 'rules'

  id: str
  premise: JSONLDFrame
  implies: JSONLDFrame
  resolve: Callable[[JSONLD], Promise[JSONLD]]

  @staticmethod
  def create(id: str, premise: JSONLDFrame, implies: JSONLDFrame):
    ''' Decorator for constructing and registering a rule object

    @params id:       globally unique identifier for this rule.
    @params premise:  the premise as a JSONLDFrame for which this rule is applicable
    @params implies:  the shape of the implications, as a JSONLDFrame for which this rule will resolve
    '''
    def decorator(func):
      r = Rule(
        id=id,
        premise=premise,
        implies=implies,
        resolve=partial(Promise.create, id, func)
      )
      Cache[Rule._cache_prefix].setitem(id, r)
      return r
    return decorator

  @staticmethod
  def all():
    return Cache[Rule._cache_prefix].get()
