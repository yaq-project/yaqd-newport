from ._newport_motor import NewportMotor


class NewportConexAGP(NewportMotor):
    _kind = "newport-conex-agp"

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self._native_units = "deg"
