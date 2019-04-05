from typing import NamedTuple, Callable
from enum import Enum
from .types import JSONLD, JSONLDFrame

class Rule(NamedTuple):
  frame: JSONLDFrame
  recipe: Callable[[JSONLD], JSONLD]

class RuleType(Enum):
  before = 'before'
  during = 'during'
  after = 'after'
