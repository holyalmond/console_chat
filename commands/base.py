from typing import Callable, Dict, List, Any

COMMANDS: Dict[str, Callable[..., Any]] = {}

def command(name: str, description: str = ""):
    def decorator(func: Callable[..., Any]):
        func._cmd_name = name
        func._cmd_description = description
        COMMANDS[name] = func
        return func
    return decorator

def get_command(name: str) -> Callable[..., Any]:
    return COMMANDS.get(name)

def list_commands() -> List[Dict[str, str]]:
    return [{"name": name, "description": getattr(func, '_cmd_description', '')} for name, func in COMMANDS.items()]
