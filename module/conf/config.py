import json
import os

from dataclasses import dataclass
from .const import DEFAULT_SETTINGS, ENV_TO_ATTR
from .version import VERSION

if VERSION == "DEV_VERSION":
    CONFIG_PATH = "config/config_dev.json"
else:
    CONFIG_PATH = "config/config.json"


class ConfLoad(dict):
    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, key, value):
        self[key] = value


@dataclass
class Settings():
    program: ConfLoad
    downloader: ConfLoad
    rss_parser: ConfLoad
    bangumi_manage: ConfLoad
    debug: ConfLoad
    proxy: ConfLoad
    notification: ConfLoad
    def __init__(self):
        self.load(CONFIG_PATH)

    def load(self, path):
        if os.path.isfile(path):
            with open(path, "r") as f:
                conf = json.load(f)
        else:
            conf = self._create_config()
        for key, section in conf.items():
            setattr(self, key, ConfLoad(section))

    def _val_from_env(self, env, attr):
        val = os.environ[env]
        if isinstance(attr, tuple):
            conv_func = attr[1]
            val = conv_func(val)
        return val

    def _create_config(self):
        settings = DEFAULT_SETTINGS
        for key, section in ENV_TO_ATTR.items():
            for env, attr in section.items():
                if env in os.environ:
                    settings[key][attr] = self._val_from_env(env, attr)
        with open(CONFIG_PATH, "w") as f:
            json.dump(settings, f, indent=4)
        return settings


settings = Settings()


