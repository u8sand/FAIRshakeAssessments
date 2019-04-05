import json
import rdflib
import rdflib.compare
from pyld import jsonld
from typing import Optional, List
from .types import JSONLD, JSONLDContext, JSONLDFrame

class LD:
  ''' A class for manipulating linked data in RDF while treating it as JSON-LD.
  '''

  def __init__(self, graph: rdflib.Graph = rdflib.Graph()):
    self._graph = rdflib.compare.to_isomorphic(graph)

  def __repr__(self) -> str:
    return repr(self.compact())

  def __str__(self) -> str:
    return str(self.compact())

  def __eq__(self, other: 'LD') -> bool:
    return self._graph == other._graph

  def __gt__(self, other: 'LD') -> bool:
    return self._graph > other._graph

  def __le__(self, other: 'LD') -> bool:
    return self._graph <= other._graph

  def __add__(self, other: 'LD'):
    return LD(self._graph + other._graph)

  def compact(self, ctx: JSONLDContext = {}) -> JSONLD:
    return jsonld.compact(self.to_jsonld(), ctx)

  def frame(self, frame: JSONLDFrame, ctx: Optional[JSONLDContext] = None) -> JSONLD:
    # TODO: proper frame--drop nodes which result in nulls unless they have "@default": null
    return jsonld.frame(self.to_jsonld(), frame, { 'explicit': True })

  def to_jsonld(self) -> JSONLD:
    return json.loads(self._graph.serialize(format='json-ld', encoding='utf-8'))

  @staticmethod
  def from_jsonld(ld: JSONLD) -> 'LD':
    return LD(rdflib.Graph().parse(data=json.dumps(jsonld.expand(ld)), format='json-ld'))

  @staticmethod
  def union(lds: List['LD']) -> 'LD':
    g = LD()
    for ld in lds:
      g = g + ld
    return g
