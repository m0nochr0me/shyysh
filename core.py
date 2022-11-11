"""
ShyySH

Core
"""

import yaml
import shutil
from pathlib import Path
import logging


_conf_dir = Path(Path.home() / '.config/shyysh')
if not _conf_dir.is_dir():
    _conf_dir.mkdir(parents=True, exist_ok=True)

_conf_file = _conf_dir / 'config.yaml'
if not _conf_file.is_file():
    _conf_default = Path.cwd() / 'config.default.yaml'
    shutil.copy(_conf_default, _conf_file)

with open(_conf_file, mode='r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

if not config['db']['path']:
    config['db']['path'] = str(_conf_dir / 'connections.db')

if not config['log']['dir']:
    _log_dir = _conf_dir
else:
    _log_dir = Path(config['log']['dir'])

logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s',
                    datefmt='%x %X',
                    filename=_log_dir / 'shyysh.log',
                    level=config['log']['level'],
                    encoding='utf-8')
logger = logging.getLogger('ShyySH')
