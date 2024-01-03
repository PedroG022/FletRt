import flet as ft
from flet_core import NavigationBar

from fletrt import NavigationRoute


class Index(NavigationRoute):
    def __init__(self):
        super().__init__()

        self.destinations = [
            '/home',
            '/settings'
        ]

    def navigation_bar(self) -> NavigationBar:
        return ft.NavigationBar(
            destinations=[
                ft.NavigationDestination(label='Home Page', icon=ft.icons.HOME),
                ft.NavigationDestination(label='Program Settings', icon=ft.icons.SETTINGS)
            ]
        )
