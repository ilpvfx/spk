from typing import NamedTuple, Optional, List
import os
import errno
import configparser

from . import storage

_DEFAULTS = {"storage": {"root": os.path.expanduser("~/.local/share/spenv")}}
_CONFIG: Optional["Config"] = None


class Config(configparser.ConfigParser):
    def __init__(self) -> None:
        super(Config, self).__init__()

    @property
    def storage_root(self) -> str:
        return str(self["storage"]["root"])

    def list_remote_names(self) -> List[str]:

        names = []
        for section in self:
            if section.startswith("remote."):
                names.append(section.split(".")[1])
        return names

    def get_repository(self) -> storage.FileRepository:

        return storage.ensure_file_repository(self.storage_root)

    def get_remote(self, name: str) -> storage.Repository:

        addr = self[f"remote.{name}"]["address"]
        return storage.open_repository(addr)


def get_config() -> Config:

    global _CONFIG
    if _CONFIG is None:
        _CONFIG = load_config()
    return _CONFIG


def load_config() -> Config:

    user_config = os.path.expanduser("~/.config/spenv/spenv.conf")
    system_config = "/etc/spenv.conf"

    config = Config()
    config.read_dict(_DEFAULTS)
    try:
        with open(system_config, "r", encoding="utf-8") as f:
            config.read_file(f, source=system_config)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise
    try:
        with open(user_config, "r", encoding="utf-8") as f:
            config.read_file(f, source=user_config)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise

    return config
