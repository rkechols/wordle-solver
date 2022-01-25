from abc import ABC, abstractmethod


class WordleDriver(ABC):
    @abstractmethod
    def start(self):
        pass
