import datetime
import json
import logging
from enum import Enum

import grpc
from google.api_core.exceptions import NotFound
from google.cloud.tasks_v2 import CloudTasksClient as _CloudTasksClient
from google.cloud.tasks_v2.services.cloud_tasks.transports import (
    CloudTasksGrpcTransport,
)
from google.protobuf import timestamp_pb2

from config import settings

log = logging.getLogger(__name__)


class HttpMethodEnum(str, Enum):
    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"


class CloudTasksClient:
    def __init__(self):
        self.url = settings.CLOUD_TASKS_URL
        self.project = settings.GCP_PROJECT_ID
        self.location = settings.GCP_LOCATION
        self._configure()

    def _configure(self) -> None:
        self.is_production = settings.FLASK_ENV == "production"
        if self.is_production:
            self.service_account_email = settings.GCP_SERVICE_ACCOUNT_EMAIL
            self.client = _CloudTasksClient()
        else:
            self.parent = f"projects/{self.project}/locations/{self.location}"
            channel = grpc.insecure_channel("gcloud-tasks-emulator:8123")
            transport = CloudTasksGrpcTransport(channel=channel)
            self.client = _CloudTasksClient(transport=transport)

    def add_task(
        self,
        payload: dict,
        method: HttpMethodEnum,
        endpoint: str,
        queue: str,
        in_seconds: int = None,
    ):
        payload = json.dumps(payload)
        self._create_task_model(payload, queue)
        http_request = {
            "http_method": method,
            "url": f"{self.url}/{self.task_obj.task_id}/{endpoint}",
            "headers": {"Content-type": "application/json"},
            "body": payload.encode(),
        }

        if self.is_production:
            parent = self.client.queue_path(self.project, self.location, queue)
            oidc_token = {"service_account_email": self.service_account_email}
            http_request["oidc_token"] = oidc_token

            task = {"http_request": http_request}

            if in_seconds:
                d = datetime.datetime.utcnow() + datetime.timedelta(seconds=in_seconds)
                timestamp = timestamp_pb2.Timestamp()
                timestamp.FromDatetime(d)
                task["schedule_time"] = timestamp

            response = self.client.create_task(request={"parent": parent, "task": task})
            log.info(f"Task created: {response.name}")
        else:
            queue_name = f"{self.parent}/queues/{queue}"
            try:
                self.client.get_queue(name=queue_name)
                log.info(f"Queue '{queue_name}' already exists.")
            except NotFound:
                log.info("Queue does not exist. Creating it...")
                self.client.create_queue(queue={"name": queue_name}, parent=self.parent)

            self.client.create_task(
                task={
                    "http_request": http_request,
                },
                parent=queue_name,
            )
