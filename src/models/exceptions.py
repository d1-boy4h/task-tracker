'''Исключения программы.'''

class NoNameTaskException(Exception):
    '''Исключение создания задачи без имени'''
    def __init__(self):
        self.msg = 'задача не может быть пустой!'
