from flet import Page


class RoutingMiddleware:
    source_route: str

    def __init__(self, page: Page):
        self.__page = page

    def redirect(self, target_route):
        self.__page.go(target_route)
        return False

    def prevent(self):
        self.redirect(self.source_route)
        return False

    def before_route_change(self, source_route: str, target_route: str):
        pass
