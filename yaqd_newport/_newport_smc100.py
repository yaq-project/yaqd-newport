from ._newport_motor import NewportMotor


class NewportSMC100(NewportMotor):
    _kind = "newport-smc100"

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self._native_units = "mm"
