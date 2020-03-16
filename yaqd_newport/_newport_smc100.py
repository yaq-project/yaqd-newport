from ._newport_motor import NewportMotor


class NewportSMC100(NewportMotor):
    _kind = "newport-smc100"
    defaults = {
        "baudrate": 57_600,
        "units": "mm",
        "model": "SMC100",
        "make": "Newport",
        "axis": 1,
    }
