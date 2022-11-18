"""
ShyySH

Models
"""

import yaml
from tinydb import TinyDB, Storage
from shyysh.core import config, logger

__all__ = ['ConnectionItem']


class YAMLStorage(Storage):
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        with open(self.filename) as handle:
            try:
                data = yaml.safe_load(handle.read())
                return data
            except yaml.YAMLError:
                return None

    def write(self, data):
        with open(self.filename, 'w+') as handle:
            yaml.dump(data, handle, sort_keys=False, allow_unicode=True)

    def close(self):
        pass


class ConnectionItem:
    def __init__(self):
        self._db = TinyDB(config['db']['path'], storage=YAMLStorage)
        self._default = {
            'title': '',
            'user': '',
            'host': '',
            'port': '',
            'compression': False,
            'fwd_x': False,
            'fwd_a': False,
            'allow_rpc': False,
            'no_exec': False,
            'custom_opt': '',
            'prepend_cmd': '',
            'append_cmd': '',
            'sort': '1000'
        }
        self.cursor = None

    def add(self, data: dict):
        return self._db.insert(data)

    def all(self):
        return self._db.all()

    def update(self, doc_ids: tuple[int], data: dict):
        return self._db.update(data, doc_ids=doc_ids)

    def delete(self, doc_ids: tuple[int]):
        self._db.remove(doc_ids=doc_ids)

    def delete_single(self, doc_id: int):
        self.delete(doc_ids=(doc_id,))
        return True

    def get(self, doc_id: int, as_dict=False):
        _r = self._db.get(doc_id=doc_id)
        if as_dict:
            return {**self._default, **dict(_r)}
        return _r

    def get_current(self, as_dict=False):
        if self.cursor:
            _r = self.get(self.cursor, as_dict=as_dict)
        else:
            _r = self._default
        return _r

    def update_current(self, data: dict):
        if self.cursor:
            _r = self.update(doc_ids=(self.cursor,), data=data)[0]
        else:
            _r = self.add(data=data)
            self.cursor = _r
        return self.cursor

    def summary(self):
        _r = []
        for item in self.all():
            _r.append((item['title'], item.doc_id))
        return _r

    def reorder(self):
        _items = self.all()

        def _sort(item):
            try:
                _s = int(item['sort'])
            except Exception as e:
                logger.error(e)
                _s = 1000
            return _s

        _items.sort(key=lambda i: _sort(i))

        self._db.drop_tables()
        self._db.insert_multiple(_items)
        self.cursor = None
