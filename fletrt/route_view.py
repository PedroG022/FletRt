from flet import AppBar, NavigationBar, Container, Page


class RouteView:
    def __init__(self):
        self._page: Page = None

    def set_page(self, page: Page):
        self._page: Page = page

    def app_bar(self) -> AppBar:
        pass

    def navigation_bar(self) -> NavigationBar:
        pass

    def body(self) -> Container:
        pass
