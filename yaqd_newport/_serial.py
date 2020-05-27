import asyncio
import re

from yaqd_core import aserial, logging


class SerialDispatcher:
    def __init__(self, port, baudrate):
        self.port = aserial.ASerial(port, baudrate)
        self.workers = {}
        self.write_queue = asyncio.Queue()
        self.loop = asyncio.get_event_loop()
        self.tasks = [
            self.loop.create_task(self.do_writes()),
            self.loop.create_task(self.read_dispatch()),
        ]

    def write(self, data):
        self.write_queue.put_nowait(data)

    async def do_writes(self):
        while True:
            data = await self.write_queue.get()
            self.port.write(data)
            self.write_queue.task_done()
            await asyncio.sleep(0.01)

    async def read_dispatch(self):
        parse = re.compile(r"^(\d*)([A-Z][A-Z])(.*)$")
        async for line in self.port.areadlines():
            line = line.decode("utf8")
            line = re.sub(r"\s", "", line.strip())
            match = parse.match(line)
            if match is None:
                continue
            index, command, args = match.groups()
            index = int(index)
            if index in self.workers:
                self.workers[index].put_nowait((command, args))

    def flush(self):
        self.port.flush()

    def close(self):
        self.loop.create_task(self._close())

    async def _close(self):
        await self.write_queue.join()
        for worker in self.workers.values():
            await worker.join()
        for task in self.tasks:
            task.cancel()
