from application.interfaces import MetricsService
from config import settings
from infrastructure.cloud_monitoring.client import stats


class CloudMetricsService(MetricsService):
    def increment(self, metric: str, value: int = 1):
        if settings.ENVIRONMENT == "prod":
            stats(metric=metric, value=value)
