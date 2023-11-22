from flet import Container, Page
from fletrt.route_view import RouteView


class Router:
    def __init__(self, page: Page, routes: dict, starting_route: str = '/'):
        self.page = page
        self.routes = routes

        self.page.on_route_change = self.on_route_change

        for route in routes:
            route_view: RouteView = routes.get(route)
            route_view.set_page(page)

        self.current_route: RouteView = self.routes[starting_route]
        self.init_components()

        self.body = Container(self.current_route.body())
        self.page.add(self.body)

    def on_route_change(self, route):
        self.current_route: RouteView = self.routes[route.route]

        self.reset_page()
        self.init_components()

        self.body.content = self.current_route.body()
        self.body.update()

    def init_components(self):
        navigation_bar = self.current_route.navigation_bar()
        appbar = self.current_route.app_bar()

        if navigation_bar is not None:
            self.page.navigation_bar = navigation_bar

        if appbar is not None:
            self.page.appbar = appbar

    def reset_page(self):
        self.page.navigation_bar = None
        self.page.window_progress_bar = None
        self.page.appbar = None
        self.page.splash = None
