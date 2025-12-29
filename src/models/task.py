'''Модель задачи.'''

from time import strftime

class Task:
    def __init__(self, desc, time=None, status=False):
        self._desc = desc
        self._time = time if time else strftime('[%d.%m.%Y %H:%M]')
        self._status = status

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, value):
        self._desc = value

    @property
    def time(self):
        return self._time

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if not isinstance(value, bool):
            raise ValueError('status должен быть типа bool')
        self._status = value

    def to_dict(self):
        return {
            'desc': self.desc,
            'time': self.time,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['desc'],
            data['time'],
            data['status']
        )
