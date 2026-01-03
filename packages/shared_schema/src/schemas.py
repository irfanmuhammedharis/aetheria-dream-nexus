# Shim to re-export the real schemas from packages/shared-schema/src/schemas.py
import importlib.util
import os

real_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'shared-schema', 'src', 'schemas.py'))
if os.path.exists(real_path):
    spec = importlib.util.spec_from_file_location("_aetheria_shared_schemas", real_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # Re-export public attributes
    for name in dir(mod):
        if not name.startswith("_"):
            globals()[name] = getattr(mod, name)
else:
    raise ImportError(f"Cannot find shared-schema schemas at {real_path}")
