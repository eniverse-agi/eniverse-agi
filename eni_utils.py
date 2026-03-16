from sskc_module import sskc_engine
from typing import Dict, Any

def improve_code(task: str) -> Dict[str, Any]:
    """
    ENI Utils v4.1 – csak a teljes SSKC v4.1 motort hívja
    Lazy import + nulla circular import
    """
    return sskc_engine.general_solve(task)
