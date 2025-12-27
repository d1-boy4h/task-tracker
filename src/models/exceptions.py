'''Исключения программы.'''

class NoNameTaskException(Exception):
    '''Исключение создания задачи без имени'''
    def __init__(self):
        super()
        self.msg = 'задача не может быть пустой!'
