import pkgutil
import importlib

__all__ = []
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    if not is_pkg:
        importlib.import_module(f"{__name__}.{module_name}")
        __all__.append(module_name)