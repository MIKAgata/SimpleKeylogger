from abc import ABC, abstractmethod

class BaseNotifier(ABC):
    @abstractmethod
    def send(self, message):
        pass

    @property
    def enabled(self):
        return False