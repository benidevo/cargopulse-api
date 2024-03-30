import logging
import time

from google.api_core.exceptions import GoogleAPICallError
from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp

from config import settings


class CloudMonitoringClient:
    _instances = {}

    def __new__(cls, project_id: str):
        if project_id not in cls._instances:
            cls._instances[project_id] = super(CloudMonitoringClient, cls).__new__(cls)
            cls._instances[project_id].client = monitoring_v3.MetricServiceClient()
            cls._instances[project_id].project_name = f"projects/{project_id}"
        return cls._instances[project_id]

    def write_custom_metric(self, metric_type: str, value: int):
        series = monitoring_v3.TimeSeries()
        series.metric.type = f"custom.googleapis.com/{metric_type}"
        series.resource.type = "global"

        now = time.time()
        end_time = Timestamp(seconds=int(now))

        start_time = end_time

        point = monitoring_v3.Point(
            interval=monitoring_v3.TimeInterval(
                start_time=start_time, end_time=end_time
            ),
            value=monitoring_v3.TypedValue(int64_value=value),
        )
        series.points.append(point)

        try:
            self.client.create_time_series(name=self.project_name, time_series=[series])
        except GoogleAPICallError as e:
            logging.error(
                f"Failed to write custom metric due to Google API call error: {e}"
            )
        except Exception as e:
            logging.error(
                f"Failed to write custom metric due to an unexpected error: {e}"
            )


def stats(metric: str, value: int):
    """
    Sends a custom metric to Cloud Monitoring with the specified metric name and value.

    Args:
        metric (str): The name of the metric to send.
        value (int, optional): The value of the metric. Defaults to 1.

    Returns:
        None
    """
    project_id: str = settings.DEV_GCP_PROJECT_ID or settings.PROD_GCP_PROJECT_ID
    client = CloudMonitoringClient(project_id)
    client.write_custom_metric(metric, value)
