from ._newport_motor import NewportMotor


class NewportConexAGP(NewportMotor):
    _kind = "newport-conex-agp"
    defaults = {
        "baudrate": 921_600,
        "units": "deg",
        "model": "CONEX-AGP",
        "make": "Newport",
        "axis": 1,
    }
