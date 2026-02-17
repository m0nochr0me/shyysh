"""
ShyySH

Core
"""

import logging
import shutil
from pathlib import Path

import yaml

__all__ = ["config", "logger"]

_conf_dir = Path(Path.home() / ".config/shyysh")
if not _conf_dir.is_dir():
    _conf_dir.mkdir(parents=True, exist_ok=True)

_conf_file = _conf_dir / "config.yaml"
if not _conf_file.is_file():
    _conf_default = Path(__file__).resolve().parent / "config.default.yaml"
    shutil.copy(_conf_default, _conf_file)

with open(_conf_file, mode="r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

if not config["db"]["path"]:
    _db_path = _conf_dir / "connections.db"
    _db_path.touch(exist_ok=True)
    config["db"]["path"] = str(_conf_dir / "connections.db")

_log_dir = _conf_dir if not config["log"]["dir"] else Path(config["log"]["dir"])

logging.basicConfig(
    format=r"%(asctime)s.%(msecs)03d %(levelname)s %(message)s",
    datefmt=r"%x %X",
    filename=_log_dir / "shyysh.log",
    level=config["log"]["level"],
    encoding="utf-8",
)
logger = logging.getLogger("ShyySH")
