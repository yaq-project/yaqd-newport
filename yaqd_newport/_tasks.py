from __future__ import annotations

import asyncio


class TaskSet(set):
    def __init__(self, iterable=()):
        super().__init__(iterable)
        for task in self:
            task.add_done_callback(self.discard)

    def add(self, task:asyncio.Task):
        super().add(task)
        task.add_done_callback(self.discard)
    
    def add_coro(self, coro):
        task = asyncio.get_running_loop().create_task(coro)
        self.add(task)

