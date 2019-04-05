import os
import logging
from importlib import import_module, reload
from .cache import Cache

def walk_directory(parent_dir: str, mod_dir: str, package: str):
  ''' Walk directory, importing all files for their side-effects.
  Parameters
  ----------
  mod_dir
    The directory to traverse.
  '''
  for root, dirs, files in os.walk(os.path.join(parent_dir, mod_dir)):
    # Prepare list of directories to NOT walk
    dirs_rm = [d for d in dirs if d.startswith('__')]
    for f in files:
      # import all python files
      if f.endswith('.py') and not f.startswith('test_'):
        cmd = os.path.splitext(f)[0]
        # app/sub/module -> .sub.module
        entity_mod = '.' + os.path.relpath(
          os.path.join(
            root, cmd,
          ),
          parent_dir,
        ).replace(
          os.path.sep,
          '.',
        )
        mod = Cache.getitem('importer.' + entity_mod)
        if mod is None:
          logging.debug('importing %s...' % (entity_mod))
          Cache.setitem('importer.' + entity_mod, import_module(entity_mod, package))
        else:
          logging.debug('reloading %s...' % (entity_mod))
          reload(mod)
    # Remove dirs_rm so we don't walk those directories in subsequent iterations
    for d in dirs_rm:
      dirs.remove(d)
