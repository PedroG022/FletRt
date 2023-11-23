import flet as ft
from fletrt import RouteView


class PageA(RouteView):
    def body(self) -> ft.Container:
        return ft.Container(
            ft.Column(
                controls=[
                    ft.Text("Hello World, from Page A!"),
                    ft.ElevatedButton("Go to Page B", on_click=lambda _: self._page.go('/page-b'))
                ]
            )
        )
