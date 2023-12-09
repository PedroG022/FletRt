from flet import Page, View, Control


class Route:
    def __init__(self):
        self.page: Page = None
        self.path: str = None
        self.initialized = False

    def pop(self):
        pass

    def go(self, route):
        pass

    def body(self) -> Control:
        pass

    def view(self) -> View:
        return View(self.path, controls=[
            self.body()
        ])
