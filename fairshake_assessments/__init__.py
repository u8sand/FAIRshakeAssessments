import logging
logging.basicConfig(level=logging.DEBUG)

import os
from .core.importer import walk_directory
walk_directory(os.path.dirname(__file__), 'modules', __package__)