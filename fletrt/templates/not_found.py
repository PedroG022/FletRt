import flet as ft
from flet_core import Control

from fletrt import Route


class NotFound(Route):
    def body(self) -> Control:
        return ft.Text('Route not found!')