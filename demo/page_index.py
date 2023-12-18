import flet as ft
from flet_core import NavigationBar

from fletrt import NavigationRoute


class Index(NavigationRoute):
    def navigation_bar(self) -> NavigationBar:
        return ft.NavigationBar(
            destinations=[
                ft.NavigationDestination(label='Home', icon=ft.icons.HOME),
                ft.NavigationDestination(label='Settings', icon=ft.icons.SETTINGS)
            ]
        )
