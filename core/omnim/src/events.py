from enum import Enum


class EventType(Enum):
    SERVICE_RESTORED = "service_restored"
    SERVICE_FAILING = "service_failing"
    ERROR = "error"
    NULL = "null"
    DEPLOY_FAILED = "deploy_failed"
    BUILD_FAILED = "build_failed"
    TEST_FAILED = "test_failed"
    TEST_SUCCESS = "test_success"
    DEPLOY_SUCCESS = "deploy_success"
    BUILD_SUCCESS = "build_success"
