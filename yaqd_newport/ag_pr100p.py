import asyncio

from yaq_daemon_core import hardware
import yaq_serial

__all__ = ["AgPr100PDaemon"]


class AgPr100PDaemon(hardware.ContinuousHardwareDaemon):
    defaults = {
        "make": "Newport",
        "model": "AG-PR100P",
        "axis": 1,
        "units": "deg",
        "baudrate": 921600,
    }

    def __init__(self, name, config, config_filepath):
        self.serial_port = yaq_serial.YaqSerial(config["serial_port"], baudrate=config["baudrate"])
        super().__init__(name, config, config_filepath)
        self.axis = config["axis"]

        self.serial_port.write(f"{self.axis}SL?\r\n".encode())
        self.serial_port.write(f"{self.axis}SR?\r\n".encode())

        line = self.serial_port.readline()
        lo = float(line[len(str(self.axis)) + 2 :].decode())
        line = self.serial_port.readline()
        hi = float(line[len(str(self.axis)) + 2 :].decode())
        self._limits = [(lo, hi)]

    def _set_position(self, position):
        self.serial_port.write(f"{self.axis}PA{position}\r\n".encode())

    async def update_state(self):
        while True:
            self.serial_port.write(f"{self.axis}TP\r\n".encode())
            self.serial_port.write(f"{self.axis}TS\r\n".encode())
            self.serial_port.write(f"{self.axis}TE\r\n".encode())
            try:
                pos = await asyncio.wait_for(
                    self.serial_port.read_regex(f"^{self.axis}TP.*\r\n".encode()), timeout=1.0
                )
                self._position = float(pos[3:])
            except asyncio.TimeoutError:
                pass
            try:
                status = await asyncio.wait_for(
                    self.serial_port.read_regex(f"^{self.axis}TS.*\r\n".encode()), timeout=1.0
                )
                status = status.strip()
                if status[-2:] in (b"32", b"33", b"34"):
                    self._not_busy.set()
                else:
                    self._busy.set()
            except asyncio.TimeoutError:
                pass
            try:
                error = await asyncio.wait_for(
                    self.serial_port.read_regex(f"^{self.axis}TE.*\r\n".encode()), timeout=0.01
                )
                if b"@" not in error:
                    print("ERROR CODE", error)
            except asyncio.TimeoutError:
                pass

            await self._busy.wait()

    @hardware.set_action
    def home(self):
        self.serial_port.write(f"{self.axis}RS\r\n".encode())

        async def _home():
            self.serial_port.write(f"{self.axis}OR\r\n".encode())

        loop = asyncio.get_event_loop()
        loop.call_later(0.1, _home)

    @hardware.set_action
    def stop(self):
        self.serial_port.write(f"{self.axis}ST\r\n".encode())

    @hardware.set_action
    def send_raw(self, command):
        self.serial_port.write(f"{self.axis}{command}\r\n".encode())


if __name__ == "__main__":
    AgPr100PDaemon.main()
