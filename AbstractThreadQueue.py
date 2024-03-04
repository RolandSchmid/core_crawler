from abc import abstractmethod
from queue import Empty, Queue
from time import sleep
from typing import Generic, TypeVar

from core.AbstractThread import AbstractThread

T = TypeVar('T')


class AbstractThreadQueue(AbstractThread, Generic[T]):

    def __init__(self, name: str, queue: Queue[T]) -> None:
        super().__init__(name)
        self.queue: Queue[T] = queue

    def run(self) -> None:
        while self.running:
            try:
                element: T = self.queue.get(False)
                self.process_element(element)
                self.queue.task_done()
            except Empty:
                sleep(1)
                continue

    @abstractmethod
    def process_element(self, element: T) -> None:
        raise NotImplementedError('Must override process_element')
