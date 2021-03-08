import inspect
import importlib
import logging
from pathlib import Path

log = logging.getLogger("commands")

path = Path(__path__[0])
for module_path in path.glob("*.py"):
    if module_path.name == "__init__.py":
        continue

    module_name = module_path.stem
    loaded_module = importlib.import_module(f".{module_name}", __package__)

    functions = inspect.getmembers(loaded_module, inspect.isfunction)

    # If __all__ is specified, import those functions. Otherwise, import only
    # the function matching the module name
    if "__all__" in dir(loaded_module):
        target_predicate = lambda f: f[0] in loaded_module.__all__
    else:
        target_predicate = lambda f: f[0] == module_name
        log.warning(
            f"No __all__ list defined in {__package__}.{module_name}. Only "
            "importing commands matching module name.")

    functions = {
        name: func for name, func in filter(target_predicate, functions)}
    globals().update(functions)
    if not functions:
        log.error("No commands loaded from {module_name}")

    # Remove target_predicate, which is a function
    del target_predicate
