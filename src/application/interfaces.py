from abc import ABC, abstractmethod


class MetricsService(ABC):

    @abstractmethod
    def increment(self, metric: str, value: int = 1):
        pass
