#!/usr/bin/python3

import os
import json
from sys import exit
from time import strftime

__version__ = '1.2.2'

#- Идеи для улучшения и развития программки
# Переделать промпт в команды
# Вместо очистки экрана сделать перекрытие экрана
# Покрасить текст
# Добавить README
# Переписать архитектуру по SRP
    # TaskStorage (save/load)
    # TaskManager (add/delete/complete)  
    # TaskView (show/welcome/prompt)
# Разбить классы по папкам

class TaskTracker:
    def __init__(self):
        self.program_name = 'Трекер задач'
        self.file_name = 'tasklist.json'
        self.task_list = self.load_data()
        self.action_list = (
            {'title': 'Показать все задачи', 'func': lambda: self.show_tasks()},
            {'title': 'Добавить задачу', 'func': lambda: self.make_task()},
            {'title': 'Выполнить задачу', 'func': lambda: self.make_task_is_completed()},
            {'title': 'Удалить задачу', 'func': lambda: self.delete_task()},
            {'title': 'Выход', 'func': lambda: self.stop()},
        )

    def clear_term(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def welcome(self):
        self.clear_term()

        welcome_string = f' {self.program_name} v{__version__} '
        print(welcome_string.center(len(welcome_string) + 6, '='))

    def dump_data(self):
        try:
            with open(self.file_name, 'w', encoding='utf-8') as json_file:
                data = []
                for task in self.task_list:
                    data.append(task.to_dict())
                json.dump(data, json_file, ensure_ascii=False, indent=2)
        except json.JSONDecodeError:
            print('Ошибка: не удалось сохранить изменения!')

    def load_data(self):
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
            print(f'Ошибка: не удалось загрузить задачи!')

    def stop(self):
        self.dump_data()
        exit()

    def show_tasks(self, id_is_visible=False, hide_completed_tasks=False):
        if not self.task_list:
            print('Похоже, список задач пуст!')
        else:
            for i, task in enumerate(self.task_list):
                if hide_completed_tasks and task.status:
                    continue

                task_string = f'{task.time} {task.desc} {"(выполнено)" if task.status else ""}'

                if id_is_visible:
                    print(f'({i}) {task_string}')
                else:
                    print(task_string)

    def make_task(self):
        print('Создание задачи:\n')

        try:
            new_task_name = input('Введите название задачи: ')
            if len(new_task_name) == 0:
                raise NoNameTaskException()
            self.clear_term()
        except EOFError:
            print('\nВыход из трекера задач')
            self.stop()
        except KeyboardInterrupt:
            print('\nТрекет задач принудительно закрыт!')
            self.stop()
        except NoNameTaskException as error:
            print(f'Ошибка: {error.msg}')
        else:
            self.task_list.append(CreateTask(new_task_name))
            print(f'Задача добавлена (ID: {len(self.task_list) - 1})')

    def get_prompt(self, msg, max_action_id):
        try:
            ids_str = f'[0-{max_action_id}]' if max_action_id > 0 else '[0]'
            action_id = int(input(f'{msg} {ids_str}: '))
            self.clear_term()
            if action_id > max_action_id or action_id < 0:
                raise WrongActionException()
        except EOFError:
            print('\nВыход из трекера задач')
            self.stop()
        except KeyboardInterrupt:
            print('\nТрекет задач принудительно закрыт!')
            self.stop()
        except ValueError:
            print('Ошибка: действие может быть только в виде цифры!')
        except WrongActionException as error:
            print(f'Ошибка: {error.msg}')
        else:
            return action_id

    def make_task_is_completed(self):
        print('Отметка задачи как выполненной:\n')

        self.show_tasks(id_is_visible=True, hide_completed_tasks=True)
        task_id = self.get_prompt('Выберите номер задачи', len(self.task_list) - 1)
        current_task = self.task_list[task_id]
        if current_task.status:
            print(f'Задача "{current_task.desc}" уже является выполненной! ')
        else:
            current_task.status = True
            print(f'Задача "{current_task.desc}" выполнена! ')

    def delete_task(self):
        print('Удаление задачи:\n')

        self.show_tasks(id_is_visible=True)

        if self.task_list:
            task_id = self.get_prompt('Выберите номер задачи', len(self.task_list) - 1)

            current_task = self.task_list[task_id]
            del self.task_list[task_id]
            print(f'Задача \'{current_task.desc}\' удалена! ')
        else:
            print('Похоже, список задач пуст!')

    def show_actions(self):
        print('')
        for i, action in enumerate(self.action_list):
            print(f'{i}. {action.get("title")}')

    def run(self):
        self.welcome()
        self.show_actions()
        while True:
            prompt = self.get_prompt('\nВыберите действие', len(self.action_list) - 1)

            if prompt is None:
                continue

            self.action_list[prompt].get('func')()

class CreateTask:
    def __init__(self, desc, time=None, status=False):
        self._desc = desc
        self._time = time if time else strftime('[%d.%m.%Y %H:%M]')
        self._status = False

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

class WrongActionException(Exception):
    def __init__(self):
        Exception.__init__(self)
        self.msg = 'указано неверное действие!'

class NoNameTaskException(Exception):
    def __init__(self):
        Exception.__init__(self)
        self.msg = 'задача не может быть пустой!'

if __name__ == '__main__':
    tracker = TaskTracker()
    tracker.run()
