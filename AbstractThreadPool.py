import logging
from abc import abstractmethod
from queue import Queue
from typing import Generic, TypeVar

from core.AbstractThread import AbstractThread
from tools.Logger import get_logger_main

logger: logging.Logger = get_logger_main()
T = TypeVar('T')
Q = TypeVar('Q')


class AbstractThreadPool(AbstractThread, Generic[T]):

    def __init__(self, name: str, n_workers: int, queue: Queue[T]) -> None:
        super().__init__(name)
        self.n_workers: int = n_workers
        self.workers: list[AbstractThread] = list()
        self.queue: Queue = queue

    def run(self) -> None:
        logger.info(f'Starting ThreadPool {self.name}')
        for i in range(self.n_workers):
            worker: AbstractThread = self.run_worker(i)
            self.workers.append(worker)
        self.queue.join()
        for w in self.workers:
            w.stop()

    @abstractmethod
    def run_worker(self, index: int) -> AbstractThread:
        raise NotImplementedError('Must override run_worker')
