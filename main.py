#!/usr/bin/python3

import os
import json
from sys import exit
from time import strftime

__version__ = '1.2'

# TODO: Сделать так, чтобы выполненные таски не отображались
# TODO: Вместо очистки экрана сделать перекрытие экрана
# TODO: Переделать промпт в команды
# TODO: Покрасить текст
# TODO: Добавить README

class TaskTracker:
    def clear_term(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def welcome(self):
        self.clear_term()
        print(f'=== Трекер задач v{__version__} ===')

    def dump_data(self):
        with open(self.file_name, 'w') as json_file:
            data = {}
            for task in self.task_list:
                data[task.desc] = task.stringify()
            json.dump(data, json_file)

            return data

    def load_data(self):
        try:
            with open(self.file_name, 'r') as json_file:
                data = json.load(json_file)
                task_list = []
                for task_name, task in data.items():
                    task_list.append(CreateTask.parse(task_name, task))
                
                return task_list

        except FileNotFoundError:
            return []

        
    def stop(self):
        self.dump_data()
        exit()
    
    def show_tasks(self, id_is_visible = False):
        if (not len(self.task_list)):
            print('Похоже, список задач пуст!')
            return
        else:
            for task_id in range(0, len(self.task_list)):
                current_task = self.task_list[task_id]
                task_string = f'{current_task.time} {current_task.desc} {current_task.get_is_completed()}'
                if id_is_visible:
                    print(f'({task_id}) {task_string}')
                else:
                    print(task_string)

    def make_task(self):
        try:
            new_task_name = input('Введите название задачи: ')
        except EOFError:
            print('\nВыход из трекера задач')
            self.stop()
        except KeyboardInterrupt:
            print('\nТрекет задач принудительно закрыт!')
            self.stop()
        else:
            self.task_list.append(CreateTask(new_task_name))
            print(f'Задача добавлена (ID: {len(self.task_list) - 1})')

    def get_prompt(self, msg, max_action_id):
        try:
            action_id = int(input(f'\n{msg} [0-{max_action_id}]: '))
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
        except WrongActionException as wae:
            print(f'Ошибка: {wae.msg}')
        else:
            return action_id

    def make_task_is_completed(self):
        self.show_tasks(True)
        task_id = self.get_prompt('Выберите номер задачи', len(self.task_list) - 1)
        current_task = self.task_list[task_id]
        current_task.is_completed = True
        print(f'Задача "{current_task.desc}" выполнена! ')

    def delete_task(self):
        self.show_tasks(True)
        task_id = self.get_prompt('Выберите номер задачи', len(self.task_list) - 1)

        current_task = self.task_list[task_id]
        del self.task_list[task_id]
        print(f'Задача \'{current_task.desc}\' успешно удалена! ')

    def __init__(self):
        self.file_name = 'tasklist.json'
        self.task_list = self.load_data()
        self.action_list = (
            {'title': 'Показать все задачи', 'func': lambda: self.show_tasks()},
            {'title': 'Добавить задачу', 'func': lambda: self.make_task()},
            {'title': 'Выполнить задачу', 'func': lambda: self.make_task_is_completed()},
            {'title': 'Удалить задачу', 'func': lambda: self.delete_task()},
            {'title': 'Выход', 'func': lambda: self.stop()},
        )

    def show_actions(self):
        print('')
        for i in range(0, len(self.action_list)):
            print(f'{i}. {self.action_list[i].get("title")}')

    def run(self):
        self.welcome()
        self.show_actions()
        while True:
            prompt = self.get_prompt('Выберите действие', len(self.action_list) - 1)
            if prompt != None:
                self.action_list[prompt].get('func')()

class CreateTask:
    def __init__(self, desc):
        self.desc = desc
        self.time = strftime('[%d.%m.%Y %H:%M]')
        self.is_completed = False
    
    def get_is_completed(self):
        return '(выполнено)' if self.is_completed else ''

    def stringify(self):
        return {
            'time': self.time,
            'is_completed': self.is_completed
        }
    
    @classmethod
    def parse(cls, desc, data):
        task = cls(desc)
        task.is_completed = data['is_completed']
        task.time = data['time']

        return task

class WrongActionException(Exception):
    def __init__(self):
        Exception.__init__(self)
        self.msg = 'указано неверное действие!'

if __name__ == '__main__':
    tracker = TaskTracker()
    tracker.run()
