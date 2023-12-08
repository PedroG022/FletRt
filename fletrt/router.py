from flet import Page, View
from flet import RouteChangeEvent

from fletrt import Route
from fletrt.templates import NotFound


class Router:

    # Initialize the router
    def __init__(self, page: Page, routes: dict, starting_route: str = '/'):
        self.page: Page = page

        # Intercepts not found pages
        routes['/404'] = NotFound()

        # Sets variables that will be used
        self.routes_dict: dict = routes
        self.routes_path = [path for path in self.routes_dict.keys()]
        self.starting_route: str = starting_route

    # Sets the router to intercept the page changes
    def install(self):
        self.page.on_route_change = self.on_route_change
        self.page.route = self.starting_route
        self.page.go(self.page.route)

    # Initialize the route variables
    def initialize_route(self, route: Route, path: str):
        if not route.initialized:
            route.page = self.page
            route.path = path

            route.pop = self.pop_route

            route.initialized = True

    def pop_route(self):
        last_route = self.past_routes()[-2]
        self.page.go(last_route)

    def on_route_change(self, e: RouteChangeEvent):
        self.page.views.clear()

        if not self.validate_route():
            return

        target_route: Route = self.routes_dict.get(e.route)
        self.initialize_route(target_route, e.route)

        target_route_view: View = target_route.view()

        self.page.views.append(target_route_view)
        self.page.update()

    # Checks if the route that's being navigated to
    # exists. If not, return a 404 Not Found page.
    def validate_route(self):
        if self.page.route not in self.routes_path:
            self.page.go('/404')
            return False
        return True

    def past_routes(self):
        return [f'/{path}' for path in self.page.route.split('/')]

    def debug(self):
        print('> Debug')
        print(f'\troutesPath: {self.routes_path}')
        print(f'\troutesDict: {self.routes_dict}')
        print(f'\tstartingRoute: {self.starting_route}')
