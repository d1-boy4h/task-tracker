#!/usr/bin/python3

import json
from sys import exit
from time import strftime

PROGRAM_NAME = 'Трекер задач'
__version__ = '1.4'

#- Идеи для улучшения и развития программки
# Разбить классы по папкам
# Добавить README

class Colors:
    '''Класс с ANSI кодами для цветного вывода.'''
    # Сброс
    RESET = '\033[0m'

    # Цвета текста
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Цвета фона
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

    # Яркие цвета
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

    # Стили
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Interface:
    '''Класс ввода/вывода информации'''
    @classmethod
    def info(cls, msg):
        print(msg)

    @classmethod
    def success(cls, msg):
        cls.info(Colors.GREEN + msg + Colors.RESET)

    @classmethod
    def warn(cls, msg):
        cls.info(Colors.YELLOW + msg + Colors.RESET)
    
    @classmethod
    def error(cls, msg):
        cls.info(Colors.RED + msg + Colors.RESET)

    @classmethod
    def stop(cls):
        '''Закрывает трекер задач'''
        cls.success('До свидания!')
        exit()

    @classmethod
    def show_welcome(cls):
        '''Показывает начальный экран'''
        welcome_string = f' {PROGRAM_NAME} v{__version__} '
        cls.info(f'{Colors.BOLD}{Colors.BG_WHITE}{welcome_string.center(len(welcome_string) + 6, '=')}{Colors.RESET}')

        cls.info('  Для справки введите help.\n')

    @classmethod
    def display_tasks(cls, tasks, id_is_visible=False, hide_completed_tasks=False):
        '''Показывает список всех задач'''
        if not tasks:
            cls.warn('Похоже, список задач пуст.')
        else:
            for i, task in enumerate(tasks):
                if hide_completed_tasks and task.status:
                    continue

                task_string = f'{task.time} {task.desc} {"(выполнено)" if task.status else ""}'

                if id_is_visible:
                    cls.info(f'({i}) {task_string}')
                else:
                    cls.info(task_string)

    @classmethod
    def get_command(cls, msg = ''):
        '''Забирает промпт для последующей обработки'''
        try:
            command = input((f'[{msg}]' if len(msg) else '') + '> ')
        except EOFError:
            cls.warn('\nВыход из трекера задач')
            cls.stop()
        except KeyboardInterrupt:
            cls.warn('\nТрекет задач принудительно закрыт!')
            cls.stop()
        else:
            return command

class CreateTask:
    '''Создание задачи'''
    def __init__(self, desc, time=None, status=False):
        self._desc = desc
        self._time = time if time else strftime('[%d.%m.%Y %H:%M]')
        self._status = status

    @property
    def desc(self):
        return self._desc

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

class TaskStorage:
    '''Класс загрузки и сохранения задач'''
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
                    task_list.append(CreateTask.from_dict(task))

                return task_list
        except FileNotFoundError:
            return []
        except (IOError, OSError):
            Interface.error(f'Ошибка: не удалось загрузить задачи!')

class NoNameTaskException(Exception):
    '''Исключение создания задачи без имени'''
    def __init__(self):
        Exception.__init__(self)
        self.msg = 'задача не может быть пустой!'

class TaskManager:
    def __init__(self, storage):
        self.storage = storage

    def add_task(self):
        '''Создаёт новую задачу'''
        try:
            new_task_name = Interface.get_command('Введите название задачи')
            if len(new_task_name) == 0:
                raise NoNameTaskException()
        except NoNameTaskException as error:
            Interface.error(f'Ошибка: {error.msg}')
        else:
            self.storage.tasks.append(CreateTask(new_task_name))
            self.storage.save(self.storage.tasks)
            Interface.success(f'Задача успешно добавлена.')

    def complete_task(self):
        '''Отмечает задачу как выполненную'''
        Interface.display_tasks(self.storage.tasks, id_is_visible=True, hide_completed_tasks=True)
        if not self.storage.tasks: return

        for task_id, task in enumerate(self.storage.tasks):
            if not task.status: break
            if task.status and task_id == len(self.storage.tasks) - 1:
                Interface.warn('Все задачи уже выполнены.')
                return

        try:
            task_id = int(Interface.get_command('Выберите номер задачи'))
            current_task = self.storage.tasks[task_id]
            if current_task.status:
                Interface.warn(f'Задача "{current_task.desc}" уже является выполненной! ')
            else:
                current_task.status = True
                self.storage.save(self.storage.tasks)
                Interface.success(f'Задача "{current_task.desc}" выполнена! ')
        except ValueError:
            Interface.error('Ошибка: некорректная обработка номера задачи!')
        except IndexError:
            Interface.error('Ошибка: некорректный номер задачи!')

    def delete_task(self):
        '''Удаляет задачу'''
        Interface.display_tasks(self.storage.tasks, id_is_visible=True)
        if not self.storage.tasks: return

        try:
            task_id = int(Interface.get_command('Выберите номер задачи'))

            current_task = self.storage.tasks[task_id]
            del self.storage.tasks[task_id]
            self.storage.save(self.storage.tasks)
            Interface.success(f'Задача "{current_task.desc}" успешно удалена.')
        except ValueError:
            Interface.error('Ошибка: некорректная обработка номера задачи!')
        except IndexError:
            Interface.error('Ошибка: некорректный номер задачи!')

class TaskTracker:
    '''Главный класс программы'''
    def __init__(self, storage=None, manager=None):
        self.storage = storage or TaskStorage()
        self.manager = manager or TaskManager(self.storage)
        self.actions = {
            'list': lambda: Interface.display_tasks(self.storage.tasks),
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

if __name__ == '__main__':
    tracker = TaskTracker()
    tracker.run()
