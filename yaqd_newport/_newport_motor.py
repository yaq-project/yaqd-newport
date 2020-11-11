import asyncio
import time
from typing import Dict, List, Optional

from yaqd_core import UsesUart, UsesSerial, IsHomeable, HasLimits, HasPosition, IsDaemon
from ._serial import SerialDispatcher


class NewportMotor(UsesUart, UsesSerial, IsHomeable, HasLimits, HasPosition, IsDaemon):
    _kind = "newport-motor"

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
        "0E": "NOT REFERENCED from READY",
        "0F": "NOT REFERENCED from MOVING",
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

    serial_dispatchers: Dict[str, SerialDispatcher] = {}

    def __init__(self, name, config, config_filepath):
        self._homing = True
        self._axis = config["axis"]
        if config["serial_port"] in NewportMotor.serial_dispatchers:
            self._serial = NewportMotor.serial_dispatchers[config["serial_port"]]
        else:
            self._serial = SerialDispatcher(config["serial_port"], baudrate=config["baud_rate"])
            NewportMotor.serial_dispatchers[config["serial_port"]] = self._serial
        self._read_queue = asyncio.Queue()
        self._serial.workers[self._axis] = self._read_queue
        super().__init__(name, config, config_filepath)
        self._units = config["units"]

        self._serial.write(f"{self._axis}SL?\r\n".encode())
        self._serial.write(f"{self._axis}SR?\r\n".encode())
        self._state["status"] = ""
        self._tasks.append(self._loop.create_task(self._home()))
        self._tasks.append(self._loop.create_task(self._consume_from_serial()))

    def _set_position(self, position):
        async def _wait_for_ready_and_set_position(self):
            if self._state["status"].startswith("MOVING"):
                self._serial.write(f"{self._axis}ST\r\n".encode())
            if self._busy and not self._homing:
                await self._not_busy_sig.wait()
            self._serial.write(f"{self._axis}PA{position}\r\n".encode())

        self._loop.create_task(_wait_for_ready_and_set_position(self))

    async def update_state(self):
        while True:
            if not self._homing:
                self._serial.write(f"{self._axis}TP\r\n".encode())
                self._serial.write(f"{self._axis}TE\r\n".encode())
                await asyncio.sleep(0)
            self._serial.write(f"{self._axis}TS\r\n".encode())
            self._serial.write(f"{self._axis}TE\r\n".encode())
            if not self._busy:
                try:
                    await asyncio.wait_for(self._busy_sig.wait(), 1)
                except asyncio.TimeoutError:
                    pass
            else:
                await asyncio.sleep(0.1)

    async def _consume_from_serial(self):
        while True:
            command, args = await self._read_queue.get()
            if "TP" == command:
                self._state["position"] = float(args)
            elif "TS" == command:
                self._state["error_code"] = args[:4]
                if self._state["error_code"] != "0000":
                    self.logger.error(f"ERROR CODE: {self._state['error_code']}")
                self._state["status"] = self.controller_states[args[4:]]
                self._busy = not self._state["status"].startswith("READY") or self._homing
            elif "TE" == command:
                if "@" not in args:
                    self.logger.error(f"ERROR CODE {self.error_dict[args]}")
            elif "SR" == command:
                self._state["hw_limits"][1] = float(args)
            elif "SL" == command:
                self._state["hw_limits"][0] = float(args)
            else:
                self.logger.info(f"Unhandled serial response: {command, args}")
            self._read_queue.task_done()

    def home(self):
        self._busy = True
        self._loop.create_task(self._home())

    async def _home(self):
        self._homing = True
        self._busy = True
        self._state["status"] = ""
        self._serial.write(f"{self._axis}RS\r\n".encode())
        await asyncio.sleep(5)
        while not self._state["status"].startswith("NOT REFERENCED"):
            await asyncio.sleep(0.1)
        self._serial.write(f"{self._axis}OR\r\n".encode())
        await asyncio.sleep(0.2)
        while not self._state["status"].startswith("READY"):
            await asyncio.sleep(0.1)
        self.set_position(self._state["destination"])
        self._homing = False

    def direct_serial_write(self, command: bytes):
        self._busy = True
        self._serial.write(f"{self._axis}{command.decode()}\r\n".encode())
        self._serial.write(f"{self._axis}TE\r\n".encode())

    def close(self):
        self._serial.flush()
        self._serial.close()


if __name__ == "__main__":
    NewportMotor.main()
