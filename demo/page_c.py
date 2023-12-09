import flet as ft

from fletrt import Route


class PageC(Route):

    def body(self):
        return ft.Column(
            controls=[
                ft.ElevatedButton('Page B', on_click=lambda _: self.pop()),
                ft.ElevatedButton('Page A', on_click=lambda _: self.go('/'))
            ]
        )

