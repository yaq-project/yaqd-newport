import asyncio
import time

import yaq_serial
from yaqd_core import ContinuousHardware, logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class NewportMotor(ContinuousHardware):
    _kind = "newport-motor"
    defaults = {
        "make": "newport",
        "axis": 1,
        "units": "mm",
    }

    error_dict = {
        "0": None,
        "@": None,
        "A": "Unknown message code or floating point controller address [A]",
        "B": "Controller address not correct [B]",
        "C": "Parameter missing or out of range [C]",
        "D": "Command not allowed [D]",
        "E": "Home sequence already started [E]",
        "F": "ESP stage name unknown [F]",
        "G": "Displacement out of limits [G]",
        "H": "Command not allowed in NOT REFERENCED state [H]",
        "I": "Command not allowed in CONFIGURATION state [I]",
        "J": "Command not allowed in DISABLE state [J]",
        "K": "Command not allowed in READY state [K]",
        "L": "Command not allowed in HOMING state [L]",
        "M": "Command not allowed in MOVING state [M]",
        "N": "Current position out of software limit [N]",
        "S": "Communication time-out [S]",
        "U": "Error during EEPROM access [U]",
        "V": "Error during command execution [V]",
        "W": "Command not allowed for PP version [W]",
        "X": "Command not allowed for CC version [X]",
    }

    controller_states = {
        "0A": "NOT REFERENCED from reset",
        "0B": "NOT REFERENCED from HOMING",
        "0C": "NOT REFERENCED from CONFIGURATION",
        "0D": "NON REFERENCED from DISABLE",
        "OE": "NOT REFERENCED from READY",
        "OF": "NOT REFERENCED from MOVING",
        "10": "NOT REFERENCED ESP stage error",
        "11": "NOT REFERENCED from JOGGING",
        "14": "CONFIGURATION",
        "1E": "HOMING command from RS-232-C",
        "1F": "HOMING command by SMC-RC",
        "28": "MOVING",
        "32": "READY from HOMING",
        "33": "READY from MOVING",
        "34": "READY from DISABLE",
        "35": "READY from JOGGING",
        "3C": "DISABLE from READY",
        "3D": "DISABLE from MOVING",
        "3E": "DISABLE from JOGGING",
        "46": "JOGGING from READY",
        "47": "JOGGING from DISABLE",
    }

    status_dict = {value: key for key, value in controller_states.items()}

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self._serial = yaq_serial.YaqSerial(
            config["serial_port"], baudrate=config.get("baudrate", 57600)
        )
        self._axis = config["axis"]
        self._status = ""
        self._error_code = ""

        self._serial.write(f"{self._axis}SL?\r\n".encode())
        self._serial.write(f"{self._axis}SR?\r\n".encode())

        time.sleep(1)

        """
        line = self._serial.readline()
        lo = float(line[len(str(self._axis)) + 2 :].decode())
        line = self._serial.readline()
        hi = float(line[len(str(self._axis)) + 2 :].decode())
        self._limits = [(lo, hi)]
        """

    def _set_position(self, position):
        self._serial.write(f"{self._axis}PA{position}\r\n".encode())

    async def update_state(self):
        asyncio.get_event_loop().create_task(self._consume_from_serial())
        while True:
            self._serial.write(f"{self._axis}TP\r\n".encode())
            self._serial.write(f"{self._axis}TE\r\n".encode())
            self._serial.write(f"{self._axis}TS\r\n".encode())
            self._serial.write(f"{self._axis}TE\r\n".encode())
            await asyncio.sleep(0.01)
            self._busy = not self._status.startswith("READY")
            if not self._busy:
                await self._busy_sig.wait()
            else:
                await asyncio.sleep(0.01)

    async def _consume_from_serial(self):
        async for line in self._serial.areadlines():
            if b"TP" in line:
                self._position = float(position_response.split(b"TP")[1])
            elif b"TS" in line:
                status_response = line.decode()
                self._error_code = status_response[-8:-4]
                self._status = self.controller_states[status_response[-4:-2]]
            elif b"TE" in line:
                if b"@" not in line:
                    logger.error(f"ERROR CODE {line}")
            else:
                logger.info(f"Unhandled serial response: {line}")

    def home(self):
        self._busy = True
        asyncio.get_event_loop().create_task(self._home())

    async def _home(self):
        self._serial.write(f"{self._axis}RS\r\n".encode())
        self._busy = True
        await asyncio.sleep(0.5)
        self._serial.write(f"{self._axis}OR\r\n".encode())
        await asyncio.sleep(1)
        await self._not_busy_sig.wait()
        logger.debug(self._status)
        self.set_position(self._destination)

    def get_state(self):
        state = super().get_state()
        try:
            state["status"] = self._status
            state["error_code"] = self._error_code
        except AttributeError:
            pass
        return state

    def direct_serial_write(self, command):
        self._busy = True
        self._serial.write(f"{self._axis}{command}\r\n".encode())
        self._serial.write(f"{self._axis}TE\r\n".encode())

    def close(self):
        self._serial.flush()
        self._serial.close()


if __name__ == "__main__":
    NewportMotor.main()
