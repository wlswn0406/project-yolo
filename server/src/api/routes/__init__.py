from .detection_process import detection_process_router
from .stream import stream_router
from .detections import detections_router
from .models import models_router
from .datasets import datasets_router
from .data_yaml import data_yaml_router
from .notifications import notifications_router
from .events import events_router
from .settings import settings_router
from .system import system_router
from .batch import batch_router
from .analytics import analytics_router

ALL_ROUTERS = (
    detection_process_router,
    stream_router,
    detections_router,
    models_router,
    datasets_router,
    data_yaml_router,
    notifications_router,
    events_router,
    settings_router,
    system_router,
    batch_router,
    analytics_router
)