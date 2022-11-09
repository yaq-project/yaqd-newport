from ._newport_motor import NewportMotor


class NewportConexAGP(NewportMotor):
    _kind = "newport-conex-agp"
    _native_units = "deg"
