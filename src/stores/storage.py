'''Хранилище задач.'''

from ..ui.interface import Interface
from ..models.task import Task 
import json

class TaskStorage:
    def __init__(self, filename='tasklist.json'):
        self.filename = filename
        self.tasks = self.load()

    def save(self, tasks):
        '''Сохраняет данные в файл JSON'''
        try:
            with open(self.filename, 'w', encoding='utf-8') as json_file:
                data = []
                for task in tasks:
                    data.append(task.to_dict())
                json.dump(data, json_file, ensure_ascii=False, indent=2)
        except json.JSONDecodeError:
            Interface.error('Ошибка: не удалось сохранить изменения!')

    def load(self):
        '''Загружает данные из файла JSON'''
        try:
            with open(self.filename, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                task_list = []
                for task in data:
                    task_list.append(Task.from_dict(task))

                return task_list
        except FileNotFoundError:
            return []
        except (IOError, OSError):
            Interface.error(f'Ошибка: не удалось загрузить задачи!')
