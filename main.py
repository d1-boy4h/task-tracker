#!/usr/bin/python3

'''
Task Tracker - консольное приложение для управления задачами.
'''

# TODO: Добавить README

from src.core.tracker import TaskTracker

__version__ = '1.5'
__author__ = 'd1_boy4h'
PROGRAM_NAME = 'Task Tracker'

if __name__ == '__main__':
    tracker = TaskTracker()
    tracker.run()
