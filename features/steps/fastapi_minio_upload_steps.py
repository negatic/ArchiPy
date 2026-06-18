import os
import tempfile

from behave import given, then, when
from fastapi import UploadFile
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from archipy.adapters.minio.adapters import MinioAdapter
from archipy.configs.base_config import BaseConfig
from archipy.helpers.utils.app_utils import AppUtils
from features.steps.minio_adapter_steps import get_minio_adapter
from features.test_helpers import get_current_scenario_context

_MB = 1024 * 1024


@given("a FastAPI app with a MinIO upload endpoint")
def step_build_app(context):
    scenario_context = get_current_scenario_context(context)
    app = AppUtils.create_fastapi_app(BaseConfig.global_config())

    @app.post("/buckets/{bucket_name}/objects/{object_name}")
    async def upload(bucket_name: str, object_name: str, file: UploadFile):
        adapter = MinioAdapter(BaseConfig.global_config().MINIO)
        adapter.put_object_stream(
            bucket_name,
            object_name,
            file.file,
            length=file.size or -1,
            content_type=file.content_type or "application/octet-stream",
        )
        return JSONResponse(status_code=201, content={"object": object_name, "size": file.size})

    scenario_context.store("app", app)


@given("a temporary file of {size_mb:d} MB")
def step_make_file(context, size_mb):
    scenario_context = get_current_scenario_context(context)
    fd, path = tempfile.mkstemp(suffix=".bin")
    chunk = b"\0" * _MB
    with os.fdopen(fd, "wb") as fh:
        for _ in range(size_mb):
            fh.write(chunk)
    scenario_context.store("upload_path", path)


@when('I POST the file as "{object_name}" to the upload endpoint targeting bucket "{bucket_name}"')
def step_post(context, object_name, bucket_name):
    scenario_context = get_current_scenario_context(context)
    app = scenario_context.get("app")
    path = scenario_context.get("upload_path")
    client = TestClient(app)
    try:
        with open(path, "rb") as fh:
            response = client.post(
                f"/buckets/{bucket_name}/objects/{object_name}",
                files={"file": (object_name, fh, "application/octet-stream")},
            )
    finally:
        os.unlink(path)
    scenario_context.store("response", response)


@then("the upload response status should be {code:d}")
def step_status(context, code):
    scenario_context = get_current_scenario_context(context)
    assert scenario_context.get("response").status_code == code


@then('the object "{object_name}" in bucket "{bucket_name}" should have size of at least {size_mb:d} MB')
def step_check_size(context, object_name, bucket_name, size_mb):
    adapter = get_minio_adapter(context)
    stat = adapter.stat_object(bucket_name, object_name)
    assert stat["size"] >= size_mb * _MB, f"size {stat['size']} < {size_mb * _MB}"
