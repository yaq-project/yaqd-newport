from ._newport_motor import NewportMotor


class NewportConexAGP(NewportMotor):
    _kind = "newport-conex-agp"

    def set_position(self, position: float) -> None:
        """
        specify desired position, relative to offset
        """
        position += self._state["reference_position"]
        HasLimits.set_position(self, position)

    def get_position(self) -> float:
        """
        reports the position _relative to reference position_
        i.e. that this position differs from the state position
        """
        return self._state["position"] - self._state["reference_position"]

    def get_destination(self) -> float:
        """
        reports destination _relative to reference position_
        i.e. that this destination differs from the state position
        """
        return self._state["destination"] - self._state["reference_position"]

    def get_reference_position(self) -> float:
        return self._state["reference_position"]

    def set_reference_position(self, reference):
        assert self.in_limits(reference)
        old_reference = self._state["reference_position"]
        reference_change = reference - old_reference
        self._state["reference_position"] = reference

