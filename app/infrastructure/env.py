import os

DEV_RUN = os.environ.get("DEV_RUN", "no").lower() not in ("n", "no", "false", "0")

# Comma-separated list of users to take part in dev runs
DEV_USER_UUID_LIST = os.environ.get("DEV_USER_UUID_LIST", "").split(",")

TG_TOKEN = os.environ.get("TG_TOKEN", "")

GRIST_URL = os.environ.get("GRIST_URL", "")
GRIST_DOC_ID = os.environ.get("GRIST_DOC_ID", "")
GRIST_TOKEN = os.environ.get("GRIST_TOKEN", "")
