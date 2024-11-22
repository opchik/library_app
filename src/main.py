from typing import List, Dict, Union

from .bl.library import Library
from .gateway.terminal_interface import *


def main():
    """Главная функция для работы с приложением"""
    library = Library()

    while True:
        show_commands()
        process_terminal_commands(library)
