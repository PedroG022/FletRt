import flet as ft
from fletrt import RouteView


class PageB(RouteView):
    def body(self) -> ft.Container:
        return ft.Container(
            ft.Column(
                controls=[
                    ft.Text("Hello World, from Page B!"),
                ]
            )
        )
