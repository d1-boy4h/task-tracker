'''Менеджер задач (бизнес-логика).'''

from ..models import Task, NoNameTaskException
from ..ui import Interface

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
            self.storage.tasks.append(Task(new_task_name))
            self.storage.save(self.storage.tasks)
            Interface.success(f'Задача успешно добавлена.')

    def edit_task(self):
        '''Изменяет название задачи'''
        Interface.display_tasks(self.storage.tasks, id_is_visible=True)
        if not self.storage.tasks: return

        # TODO: Тут остановился
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
