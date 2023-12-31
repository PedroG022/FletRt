import flet as ft
from flet_core import View

from fletrt import Route


class Home(Route):
    def body(self):
        content = ft.TextField(hint_text='Type anything...')
        confirm = ft.ElevatedButton('Go to next page with url parameters',
                                    on_click=lambda _: self.go('/home/' + content.value))

        return ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                content,
                confirm
            ]
        )

    def view(self) -> View:
        view = super().view()

        view.vertical_alignment = ft.MainAxisAlignment.CENTER
        view.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        return view
