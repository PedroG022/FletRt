from flet import Page, View, Control, Column


class Route:
    def __init__(self):
        self.page: Page = None
        self.path: str = None

        self.route_params: dict = None
        self.route_data: dict = None

    def pop(self):
        pass

    def go(self, route_path: str, data: dict = None):
        pass

    def body(self) -> Control:
        return Column()

    def view(self) -> View:
        return View(self.path, controls=[
            self.body()
        ])
