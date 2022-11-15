"""
ShyySH

Models
"""
from tinydb import TinyDB
from shyysh.core import config, logger

__all__ = ['ConnectionItem']


class ConnectionItem:
    def __init__(self):
        self._db = TinyDB(config['db']['path'])
        self._default = {
            'title': '',
            'user': '',
            'host': '',
            'port': '',
            'compression': False,
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
            return dict(_r)
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
