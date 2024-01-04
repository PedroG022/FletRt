from flet import Page, View, Control, Column, FloatingActionButton

from typing import Optional


class Route:
    def __init__(self):
        self.page: Optional[Page] = None
        self.path: Optional[str] = None

        self.route_params: Optional[dict] = None
        self.route_data: Optional[dict] = None

    def floating_action_button(self) -> FloatingActionButton:
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
            floating_action_button=self.floating_action_button()
        )
