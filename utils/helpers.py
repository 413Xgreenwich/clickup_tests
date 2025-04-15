import os
import json
from dotenv import load_dotenv

load_dotenv()


def get_env_variable(name):
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Environment variable '{name}' is not set")
    return value


CLICKUP_API_KEY = get_env_variable("CLICKUP_API_KEY")
CLICKUP_EMAIL = get_env_variable("CLICKUP_EMAIL")
CLICKUP_PASSWORD = get_env_variable("CLICKUP_PASSWORD")
CLICKUP_BASE_URL = get_env_variable("CLICKUP_BASE_URL")
CLICKUP_HEADERS = json.loads(get_env_variable("CLICKUP_HEADERS"))
CLICKUP_BAD_HEADERS = json.loads(get_env_variable("CLICKUP_BAD_HEADERS"))
CLICKUP_POST_HEADER = json.loads(get_env_variable("CLICKUP_POST_HEADER"))
CLICKUP_PAYLOAD = json.loads(get_env_variable("CLICKUP_PAYLOAD"))
CLICKUP_PAYLOAD_UPDATE = json.loads(get_env_variable("CLICKUP_PAYLOAD_UPDATE"))
CLICKUP_BAD_PAYLOAD = json.loads(get_env_variable("CLICKUP_BAD_PAYLOAD"))
