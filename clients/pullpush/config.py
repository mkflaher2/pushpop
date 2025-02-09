from os import getenv
from pydantic import BaseModel

class PullPushConfig(BaseModel):
    url: str

def load_pullpush_config() -> PullPushConfig:
    loaded_param_values = {
        "url": getenv("PULLPUSH_API_URL"),
    }

    loaded_param_values = {k: v for k, v in loaded_param_values.items() if v is not None}
    return PullPushConfig(**loaded_param_values)
