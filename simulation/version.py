from dataclasses import dataclass
from datetime import datetime
import platform

__version__ = "1.0.0"

@dataclass(frozen=True)
class FrameworkInfo:
    version: str
    build_date: str
    python_version: str
    architecture_version: int

def get_framework_info() -> FrameworkInfo:
    return FrameworkInfo(
        version=__version__,
        build_date=datetime.now().strftime("%Y-%m-%d"),
        python_version=platform.python_version(),
        architecture_version=15
    )
