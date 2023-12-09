import flet as ft

from fletrt import Route


class PageA(Route):
    def body(self):
        return ft.Column(
            controls=[
                ft.ElevatedButton('Page B', on_click=lambda _: self.go('/b')),
                ft.ElevatedButton('Page C', on_click=lambda _: self.go('/b/c'))
            ]
        )
