import flet as ft
from flet_core import Control

from fletrt import Route


class Content(Route):
    def body(self) -> Control:
        return ft.Text('Content received via url: ' + self.route_params['content'])
