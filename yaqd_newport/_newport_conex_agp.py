from typing import Dict, Any, Optional, List

from ._newport_motor import NewportMotor
from yaqd_core import HasLimits


class NewportConexAGP(NewportMotor):
    _kind = "newport-conex-agp"
