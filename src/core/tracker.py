'''Основной координатор программы'''

from ..stores import TaskStorage
from ..services import TaskManager
from ..ui import Interface

class TaskTracker:
    def __init__(self, storage=None, manager=None):
        self.storage = storage or TaskStorage()
        self.manager = manager or TaskManager(self.storage)

        self._display_tasks_handler = lambda: Interface.display_tasks(self.storage.tasks)
        self._display_tasks_handler.__doc__ = Interface.display_tasks.__doc__

        self.actions = {
            'list': self._display_tasks_handler,
            'add': self.manager.add_task,
            'complete': self.manager.complete_task,
            'delete': self.manager.delete_task,
            'help': self.get_help,
            'exit': Interface.stop,
        }

    def get_help(self):
        '''Отображает все команды трекера задач'''
        for action, func in self.actions.items():
            print(f'{action}: {func.__doc__}')

    def run(self):
        Interface.show_welcome()
        while True:
            try:
                command = Interface.get_command()
                self.actions[command]()
            except KeyError:
                Interface.error(f'Ошибка: такой команды не существует!')
