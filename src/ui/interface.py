'''Консольный интерфейс ввода/вывода.'''

from sys import exit
from .colors import Colors
from ..constants import PROGRAM_NAME, __version__

class Interface:
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
        cls.info(f'{Colors.BOLD}{Colors.BG_WHITE}{Colors.BRIGHT_BLACK}{welcome_string.center(len(welcome_string) + 6, '=')}{Colors.RESET}')

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