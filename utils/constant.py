# Library
from utils.models import TStatusError, TStatusSucess
import os
from pathlib import Path


THREAD_MAX_WORKER: int = 5
THREAD_SUB_MAX_WORKER: int = 3


REQUEST_RETRY_ATTEMPT = 3
REQUEST_MAX_PER_MINUTE: int = 60  # Adjust as needed
REQUEST_TIMEOUT: int = 10  # second


BRIGHTDATA_ZONE: str | None = os.getenv("BRIGHTDATA_ZONE")
BRIGHTDATA_USER: str | None = os.getenv("BRIGHTDATA_USER")
BRIGHTDATA_PASS: str | None = os.getenv("BRIGHTDATA_PASS")
OS_BRIGHTDATA_PORT: str | None = os.getenv("BRIGHTDATA_PORT")
BRIGHTDATA_PORT: int | None = int(OS_BRIGHTDATA_PORT) if OS_BRIGHTDATA_PORT else None


OS_PROXY: str | None = os.getenv("PROXY")
PROXY: list[str] = OS_PROXY.split(",") if OS_PROXY else []


FOLDER_ROOT = Path(__file__).parent.parent.as_posix()
FOLDER_OUTPUT = f"{FOLDER_ROOT}/output"
FOLDER_INPUT = f"{FOLDER_ROOT}/input"
FOLDER_LOG = f"{FOLDER_ROOT}/log"
FOLDER_DELTA = f"{FOLDER_ROOT}/delta"
FOLDER_DELTA_REPO = f"{FOLDER_DELTA}/repositories"
FOLDER_DELTA_CONTRIBUTOR = f"{FOLDER_DELTA}/contributors"
FOLDER_SPARK = f"{FOLDER_ROOT}/spark"
FOLDER_SPARK_TEMP = f"{FOLDER_SPARK}/temp"

DB_NAME = "github_logs"
DB_FILEPATH = f"{FOLDER_LOG}/{DB_NAME}.db"
DB_NAME_REPO = f"{DB_NAME}_repo"
DB_NAME_CONTRIBUTOR = f"{DB_NAME}_contributor"


STATUS_SUCCESS: TStatusSucess = TStatusSucess()
STATUS_ERROR: TStatusError = TStatusError()
STATUS_PENDING = "P"
STATUS_PROCESS = "A"
STATUS_COMPLETE = "C"
STATUS_FAILED = "F"


REPORT_COUNT = 5
REPORT_LINE_WIDTH = 50
