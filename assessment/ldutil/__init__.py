from .jsonld_eq import jsonld_eq, jsonld_strict_eq
from .jsonld_frame import jsonld_frame
from .jsonld_tripleset import jsonld_to_tripleset, tripleset_to_jsonld_compact, tripleset_to_jsonld_flat
from .jsonld_deep_map import jsonld_deep_map
from .type import JSONLD, JSONLDFrame

def jsonld_flat(ld):
  return tripleset_to_jsonld_flat(jsonld_to_tripleset(ld))

def jsonld_compact(ld, root=None):
  return tripleset_to_jsonld_compact(jsonld_to_tripleset(ld), root=root)

