from typing import Optional

from flet import Page, View, Control, Column, FloatingActionButton, AppBar


class Route:
    def __init__(self):
        self.page: Optional[Page] = None
        self.path: Optional[str] = None

        self.route_params: Optional[dict] = None

    def floating_action_button(self) -> FloatingActionButton:
        pass

    def app_bar(self) -> AppBar:
        pass

    def pop(self):
        pass

    def go(self, route_path: str, data: dict = None):
        pass

    def body(self) -> Control:
        return Column()

    def view(self) -> View:
        return View(
            self.path,
            controls=[
                self.body()
            ],
            floating_action_button=self.floating_action_button(),
            appbar=self.app_bar()
        )
