import flet as ft
from flet_core import View

from fletrt import Route


class Home(Route):
    def body(self):
        return ft.Column(
            controls=[
                ft.Text('Home', size=100)
            ]
        )

    def view(self) -> View:
        view = super().view()

        view.vertical_alignment = ft.MainAxisAlignment.CENTER
        view.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        return view
