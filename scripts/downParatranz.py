import logging
import os
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path

import coloredlogs
from openapi_client import ApiClient, Configuration
from openapi_client.api import ArtifactsApi

coloredlogs.install(level=logging.DEBUG)

logger = logging.getLogger()

CACHE_PATH = tempfile.TemporaryDirectory()

logger.debug("cache: %s", CACHE_PATH)

PARAZ_PROJECT_ID = int(os.environ["PARAZ_PROJECT_ID"])
PARAZ_TOKEN = os.environ["PARAZ_TOKEN"]

cache_path = Path(str(CACHE_PATH))
cache_path.mkdir(parents=True, exist_ok=True)

timemark = datetime.now().strftime("%m%d%H%M%S")
artifacts_name = f"paraz-{PARAZ_PROJECT_ID}-{timemark}.zip"
artifacts_path = cache_path / artifacts_name

trans_path = cache_path / "out"
trans_path.mkdir(parents=True, exist_ok=True)

conf = Configuration(
    api_key={"Token": PARAZ_TOKEN},
    api_key_prefix={"Token": ""},
    debug=True)

with ApiClient(conf) as ParazClient:
    api = ArtifactsApi(ParazClient)

    artifacts = api.download_artifact_without_preload_content(
        project_id=PARAZ_PROJECT_ID)

    with open(artifacts_path, "wb") as f:
        f.write(artifacts.data)

with zipfile.ZipFile(artifacts_path, "r") as zfile:
    zfile.extractall(trans_path)
'''
layout:

xxxx.zip
out/utf8/{控件,人物,台词,etc}
'''
