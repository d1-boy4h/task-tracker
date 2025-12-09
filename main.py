#!/usr/bin/python3

from os import system
from sys import exit
from time import strftime
import pickle

# TODO: Отрефакторить перед тем, как заливать в портфолио

__version__ = '1.0'

class CreateAction():
    def __init__(self, title, func = None):
        self.__title = title
        self.__func = func

    def __str__(self):
        return self.__title

    def __call__(self):
        if self.__func:
            return self.__func()
        return None

class CreateTask():
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

def clear_term():
    system('clear')

def exit_the_app():
    global task_list_file_name
    global task_list

    dump_data(task_list_file_name, task_list)
    exit()

def welcome():
    clear_term()
    print(f'=== Трекер задач v{__version__} ===')

def show_actions():
    global action_list

    print('')
    for i in range(0, len(action_list)):
        print(f'{i}. {action_list[i]}')

def get_prompt(msg, max_action_id):
    try:
        action_id = int(input(f'\n{msg} [0-{max_action_id}]: '))
        if action_id > max_action_id or action_id < 0:
            raise WrongActionException()
    except EOFError:
        print('\nВыход из трекера задач')
        exit_the_app()
    except KeyboardInterrupt:
        print('\nТрекет задач принудительно закрыт!')
        exit_the_app()
    except ValueError:
        print('Ошибка: действие может быть только в виде цифры!')
    except WrongActionException as wae:
        print(f'Ошибка: {wae.msg}')
    else:
        return action_id

def dump_data(file_name, task_list):
    with open(file_name, 'wb') as file:
        pickle.dump(task_list, file)

def load_data(file_name):
    try:
        with open(file_name, 'rb') as file:
            task_list = pickle.load(file)
            return task_list
    except FileNotFoundError:
        return []

def show_tasks(id_is_visible = False):
    global task_list

    if (not len(task_list)):
        print('Похоже, список задач пуст!')
        return
    else:
        for task_id in range(0, len(task_list)):
            if id_is_visible:
                print(f'({task_id}) {task_list[task_id]}')
            else:
                print(task_list[task_id])

def make_task():
    global task_list

    try:
        new_task_name = input('Введите название задачи: ')
    except EOFError:
        print('\nВыход из трекера задач')
        exit_the_app()
    except KeyboardInterrupt:
        print('\nТрекет задач принудительно закрыт!')
        exit_the_app()
    else:
        task_list.append(CreateTask(new_task_name))
        print(f'Задача добавлена (ID: {len(task_list) - 1})')

def make_task_is_completed():
    global task_list

    show_tasks(id_is_visible = True)
    task_id = get_prompt('Выберите номер задачи', len(task_list) - 1)
    task_list[task_id].is_completed = True

def delete_task():
    global task_list
    show_tasks(id_is_visible = True)
    task_id = get_prompt('Выберите номер задачи', len(task_list) - 1)

    task_name = task_list[task_id]
    del task_list[task_id]
    print(f'Задача \'{task_name}\' успешно удалена! ')

def run():
    welcome()
    show_actions()
    while True:
        prompt = get_prompt('Выберите действие', len(action_list) - 1)
        if prompt != None:
            action_list[prompt]()

if __name__ == '__main__':
    task_list_file_name = 'tasklist.data'
    task_list = load_data(task_list_file_name)

    action_list = (
        CreateAction('Показать все задачи', show_tasks),
        CreateAction('Добавить задачу', make_task),
        CreateAction('Отметить как выполненную', make_task_is_completed),
        CreateAction('Удалить задачу', delete_task),
        CreateAction('Выход', exit_the_app)
    )

    run()
