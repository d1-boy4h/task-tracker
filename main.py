#!/usr/bin/python3

import os
from sys import exit
from time import strftime
import pickle

__version__ = '1.1.1'

class TaskTracker:
    def clear_term(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def welcome(self):
        self.clear_term()
        print(f'=== Трекер задач v{__version__} ===')
    
    def dump_data(self, file_name, task_list):
        with open(file_name, 'wb') as file:
            pickle.dump(task_list, file)
    
    def load_data(self, file_name):
        try:
            with open(file_name, 'rb') as file:
                task_list = pickle.load(file)
                return task_list
        except FileNotFoundError:
            return []
        
    def stop(self):
        self.dump_data(self.task_list_file_name, self.task_list)
        exit()
    
    def show_tasks(self, id_is_visible = False):
        if (not len(self.task_list)):
            print('Похоже, список задач пуст!')
            return
        else:
            for task_id in range(0, len(self.task_list)):
                if id_is_visible:
                    print(f'({task_id}) {self.task_list[task_id]}')
                else:
                    print(self.task_list[task_id])

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
        self.task_list[task_id].is_completed = True
        print(f'Задача \'{self.task_list[task_id]}\' выполнена! ')

    def delete_task(self):
        self.show_tasks(True)
        task_id = self.get_prompt('Выберите номер задачи', len(self.task_list) - 1)

        task_name = self.task_list[task_id]
        del self.task_list[task_id]
        print(f'Задача \'{task_name}\' успешно удалена! ')

    def __init__(self):
        self.task_list_file_name = 'tasklist.data'
        self.task_list = self.load_data(self.task_list_file_name)
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
            print(f'{i}. {self.action_list[i].get('title')}')

    def run(self):
        self.welcome()
        self.show_actions()
        while True:
            prompt = self.get_prompt('Выберите действие', len(self.action_list) - 1)
            if prompt != None:
                self.action_list[prompt].get('func')()

class CreateTask:
    def __init__(self, desc):
        self.is_completed = False
        self.__time = strftime('[%d.%m.%Y %H:%M]')
        self.__desc = desc
    
    def __str__(self):
        is_completed = ''
        if self.is_completed:
            is_completed = '(выполнено)'
        return f'{self.__time} {self.__desc} {is_completed}'

class WrongActionException(Exception):
    def __init__(self):
        Exception.__init__(self)
        self.msg = 'указано неверное действие!'

if __name__ == '__main__':
    tracker = TaskTracker()
    tracker.run()
