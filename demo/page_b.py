import flet as ft

from fletrt import Route


class PageB(Route):
    def body(self):
        return ft.Column(
            controls=[
                ft.ElevatedButton('Page C', on_click=lambda _: self.go('/b/c')),
                ft.ElevatedButton('Page A', on_click=lambda _: self.pop())
            ]
        )

