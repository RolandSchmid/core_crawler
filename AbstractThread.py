from threading import Thread


class AbstractThread(Thread):

    def __init__(self, name: str) -> None:
        super().__init__(name=name)
        self.running: bool = True

    def stop(self) -> None:
        self.running = False
