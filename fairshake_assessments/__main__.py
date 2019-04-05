import sys
import json
import traceback
import os
from .core import process

try:
  goal = json.loads(sys.argv[1])
  start = json.load(sys.stdin)
  json.dump(process(start, goal), sys.stdout, sort_keys=True, indent=2)
except Exception as e:
  traceback.print_exc(file=sys.stderr)
  print('Usage: {name} [goal-LD] < start.jsonld > results.jsonld', file=sys.stderr)
