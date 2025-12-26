#!/usr/bin/python3

import json
from sys import exit
from time import strftime

__version__ = '1.3.2'

#- Идеи для улучшения и развития программки
    # Покрасить текст
# Переписать архитектуру по SRP
    # TaskStorage (save/load)
    # TaskManager (add/delete/complete)  
    # TaskView (show/welcome/prompt)
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

class Console:
    @classmethod
    def success(cls, msg):
        print(Colors.GREEN + msg + Colors.RESET)

    @classmethod
    def warn(cls, msg):
        print(Colors.YELLOW + msg + Colors.RESET)
    
    @classmethod
    def error(cls, msg):
        print(Colors.RED + msg + Colors.RESET)

class TaskTracker:
    '''Главный класс программы'''

    def __init__(self):
        self.program_name = 'Трекер задач'
        self.file_name = 'tasklist.json'
        self.task_list = self.load_data()
        self.actions = {
            'list': self.show_tasks,
            'add': self.make_task,
            'perf': self.perform_task,
            'del': self.delete_task,
            'help': self.get_help,
            'exit': self.stop,
        }

    def welcome(self):
        '''Показывает начальный экран'''

        welcome_string = f' {self.program_name} v{__version__} '
        print(f'{Colors.BOLD}{Colors.BG_WHITE}{welcome_string.center(len(welcome_string) + 6, '=')}{Colors.RESET}')

        print('  Для справки введите help.\n')

    def dump_data(self):
        '''Сохраняет данные в файл JSON'''

        try:
            with open(self.file_name, 'w', encoding='utf-8') as json_file:
                data = []
                for task in self.task_list:
                    data.append(task.to_dict())
                json.dump(data, json_file, ensure_ascii=False, indent=2)
        except json.JSONDecodeError:
            Console.error('Ошибка: не удалось сохранить изменения!')

    def load_data(self):
        '''Загружает данные из файла JSON'''

        try:
            with open(self.file_name, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                task_list = []
                for task in data:
                    task_list.append(CreateTask.from_dict(task))

                return task_list
        except FileNotFoundError:
            return []
        except (IOError, OSError):
            Console.error(f'Ошибка: не удалось загрузить задачи!')

    def stop(self):
        '''Закрывает трекер задач'''

        Console.success('До свидания!')
        exit()

    def show_tasks(self, id_is_visible=False, hide_completed_tasks=False):
        '''Показывает список всех задач'''

        if not self.task_list:
            Console.warn('Похоже, список задач пуст.')
        else:
            for i, task in enumerate(self.task_list):
                if hide_completed_tasks and task.status:
                    continue

                task_string = f'{task.time} {task.desc} {"(выполнено)" if task.status else ""}'

                if id_is_visible:
                    print(f'({i}) {task_string}')
                else:
                    print(task_string)

    def get_prompt(self, msg = ''):
        '''Забирает промпт для последующей обработки'''

        try:
            prompt = input((f'[{msg}]' if len(msg) else '') + '> ')
        except EOFError:
            Console.warn('\nВыход из трекера задач')
            self.stop()
        except KeyboardInterrupt:
            Console.warn('\nТрекет задач принудительно закрыт!')
            self.stop()
        else:
            return prompt

    def get_help(self):
        '''Отображает все команды трекера задач'''

        for action, func in self.actions.items():
            print(f'{action}: {func.__doc__}')

    def make_task(self):
        '''Создаёт новую задачу'''

        try:
            new_task_name = self.get_prompt('Введите название задачи')
            if len(new_task_name) == 0:
                raise NoNameTaskException()
        except NoNameTaskException as error:
            Console.error(f'Ошибка: {error.msg}')
        else:
            self.task_list.append(CreateTask(new_task_name))
            self.dump_data()
            Console.success(f'Задача успешно добавлена.')

    def perform_task(self):
        '''Отмечает задачу как выполненную'''

        self.show_tasks(id_is_visible=True, hide_completed_tasks=True)
        if not self.task_list: return

        try:
            task_id = int(self.get_prompt('Выберите номер задачи'))
            current_task = self.task_list[task_id]
            if current_task.status:
                Console.warn(f'Задача "{current_task.desc}" уже является выполненной! ')
            else:
                current_task.status = True
                self.dump_data()
                Console.success(f'Задача "{current_task.desc}" выполнена! ')
        except ValueError:
            Console.error('Ошибка: некорректная обработка номера задачи!')
        except IndexError:
            Console.error('Ошибка: некорректный номер задачи!')

    def delete_task(self):
        '''Удаляет задачу'''

        self.show_tasks(id_is_visible=True)
        if not self.task_list: return

        try:
            task_id = int(self.get_prompt('Выберите номер задачи'))

            current_task = self.task_list[task_id]
            del self.task_list[task_id]
            self.dump_data()
            Console.success(f'Задача "{current_task.desc}" успешно удалена.')
        except ValueError:
            Console.error('Ошибка: некорректная обработка номера задачи!')
        except IndexError:
            Console.error('Ошибка: некорректный номер задачи!')

    def run(self):
        self.welcome()
        while True:
            try:
                prompt = self.get_prompt()
                self.actions[prompt]()
            except KeyError:
                Console.error(f'Ошибка: такой команды не существует!')

class CreateTask:
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

class NoNameTaskException(Exception):
    def __init__(self):
        Exception.__init__(self)
        self.msg = 'задача не может быть пустой!'

if __name__ == '__main__':
    tracker = TaskTracker()
    tracker.run()
