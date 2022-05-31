from typing import Dict, Any, Optional, List

from ._newport_motor import NewportMotor
from yaqd_core import HasLimits


class NewportConexAGP(NewportMotor):
    _kind = "newport-conex-agp"

    def set_position(self, position: float) -> None:
        super().set_position(self._to_absolute(position))

    def get_position(self) -> float:
        return self._to_reference(self._state["position"])

    def get_destination(self) -> float:
        return self._to_reference(self._state["destination"])

    def get_reference_position(self) -> float:
        return self._state["reference_position"]

    def set_reference_position(self, reference):
        self._state["reference_position"] = self._to_absolute(reference)

    def in_limits_relative(self, position: float) -> bool:
        return super().in_limits(self._to_absolute(position))

    def get_limits_relative(self) -> List[float]:
        return [self._to_reference(lim) for lim in super().get_limits()]

    def _to_absolute(self, position):
        return position + self._state["reference_position"]

    def _to_reference(self, position):
        return position - self._state["reference_position"]
